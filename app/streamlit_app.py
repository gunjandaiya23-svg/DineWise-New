"""DineWise Streamlit interface."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from dinewise.config import data_path, load_config  # noqa: E402
from dinewise.graph.workflow import build_graph, run_query  # noqa: E402
from dinewise.llm.generator import Generator  # noqa: E402
from dinewise.rag.bm25_index import load_bm25  # noqa: E402
from dinewise.rag.search import load_retriever  # noqa: E402


@st.cache_resource(show_spinner="Loading retrieval stack ...")
def load_assets():
    cfg = load_config()
    name = cfg["chunking"]["active"]
    restaurants = pd.read_parquet(data_path(cfg, "processed_dir", "restaurants.parquet"))
    chunks = pd.read_parquet(data_path(cfg, "index_dir", "faiss", name, "chunks.parquet"))
    retriever = load_retriever(cfg, name)
    bm25 = load_bm25(cfg, name)
    return cfg, restaurants, chunks, retriever, bm25


@st.cache_resource(show_spinner="Building workflow ...")
def load_graph():
    cfg, restaurants, chunks, retriever, bm25 = load_assets()
    generator = Generator(cfg)
    return build_graph(cfg, retriever, bm25, chunks, restaurants, generator)


def render_result(state: dict) -> None:
    answer = state.get("answer", "")
    st.markdown(answer)


def main() -> None:
    st.set_page_config(page_title="DineWise", page_icon="🍽️", layout="wide")
    st.title("DineWise")
    st.caption(
        "Retrieval-augmented restaurant recommendations over a static dataset. "
        "Ratings and prices are dataset values, not live information."
    )

    _, restaurants, _, _, _ = load_assets()
    cities = sorted(restaurants["city"].dropna().unique())
    st.caption("Available cities: " + ", ".join(cities))

    tab_recommend, tab_about = st.tabs(["Recommend", "About"])

    with tab_recommend:
        query = st.text_input(
            "What are you looking for?",
            placeholder="Try: Italian restaurants in Tampa under $$",
        )
        if st.button("Recommend", type="primary") and query.strip():
            graph = load_graph()
            with st.spinner("Searching the dataset ..."):
                state = run_query(graph, query)
            render_result(state)

    with tab_about:
        st.markdown(
            """
DineWise is a laboratory prototype, not a booking service.

**What it can do**
- Recommend restaurants by cuisine, city, budget bucket, rating, and attributes.
- Quote review evidence for each result.
- Refuse live-availability, unknown-city, and unrecorded-amenity questions.

**What it cannot do**
- Provide live availability, reservations, current prices, or wait times.
- Guarantee dietary safety.
"""
        )


if __name__ == "__main__":
    main()
