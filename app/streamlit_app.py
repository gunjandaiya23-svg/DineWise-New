"""DineWise Streamlit interface."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from dinewise.config import data_path, load_config  # noqa: E402
from dinewise.deployment import ensure_assets  # noqa: E402
from dinewise.graph.workflow import build_graph, run_query  # noqa: E402
from dinewise.llm.generator import Generator  # noqa: E402
from dinewise.rag.bm25_index import load_bm25  # noqa: E402
from dinewise.rag.search import load_retriever  # noqa: E402


@st.cache_resource(show_spinner="Loading retrieval stack ...")
def load_assets():
    cfg = load_config()
    name = cfg["chunking"]["active"]
    ensure_assets(name)
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
    hits = state.get("hits", [])
    # Keep IDs in workflow state for validation and provenance, but hide them in prose.
    display = "\n".join(line for line in answer.splitlines()
                        if "business id" not in line.lower())
    # Strip internal retrieval markers that older prompts asked the model to echo,
    # e.g. "[RESTAURANT abc123]" or leftover "[RESTAURANT ]" after ID removal.
    display = re.sub(r"\[RESTAURANT[^\]]*\]", "", display, flags=re.IGNORECASE)
    display = re.sub(r"\(\s*ID:\s*[A-Za-z0-9_\-]{10,}\s*\)", "", display)
    for hit in hits:
        identifier = re.escape(str(hit["chunk"]["business_id"]))
        display = re.sub(r"\s*\((?:ID:\s*)?" + identifier + r"\)", "", display)
        display = re.sub(identifier, "", display)
    # Collapse artefacts left by stripping ("Name  ,", "Name  .", double spaces).
    display = re.sub(r"[ \t]{2,}", " ", display)
    display = re.sub(r"\s+,", ",", display)
    display = re.sub(r"\(\s*\)", "", display)
    display = re.sub(r"\n{3,}", "\n\n", display).strip()
    st.markdown(display.replace("$", r"\$"))
    recommended = []
    if not state.get("fallback_used"):
        for hit in hits:
            row = hit["chunk"]
            name = str(row.get("restaurant_name", ""))
            if name and name.casefold() in answer.casefold():
                price = row.get("price_range")
                recommended.append({"Restaurant": name,
                                    "Price": "$" * int(price) if pd.notna(price) else "Unknown",
                                    "Rating (dataset)": row.get("stars")})
    if recommended:
        st.dataframe(pd.DataFrame(recommended), hide_index=True, width="stretch")
        st.caption("Prices are relative dataset buckets; ratings are out of 5.")
    if hits:
        with st.expander("Restaurant records used"):
            for hit in hits:
                row = hit["chunk"]
                price = row.get("price_range")
                label = "$" * int(price) if pd.notna(price) else "unknown"
                st.markdown(f"**{row.get('restaurant_name', 'Restaurant')}** — "
                            f"{row.get('city', '')} · {row.get('cuisine_primary', '')} · "
                            f"Price: {label} · Dataset rating: {row.get('stars', 'unknown')}")
                st.caption(f"Business ID: {row['business_id']}")
        with st.expander("Retrieved evidence excerpts"):
            st.caption("Profile excerpts may include summaries and selected customer reviews.")
            for hit in hits:
                row = hit["chunk"]
                st.markdown(f"**{row.get('restaurant_name', 'Restaurant')}**")
                st.text(str(row.get("text", "")))


def main() -> None:
    st.set_page_config(page_title="DineWise", page_icon="🍽️", layout="wide")
    css = (Path(__file__).with_name("style.css")).read_text()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    st.markdown("""
<section class="hero">
<div class="hero-copy"><p class="hero-kicker">Your table, your taste</p>
<h1>DineWise</h1><p>Find your next favorite bite, backed by the stories people share about their meals.</p></div>
<div class="hero-art" aria-hidden="true">🍝</div>
</section>
""", unsafe_allow_html=True)

    try:
        _, restaurants, _, _, _ = load_assets()
        graph = load_graph()
    except Exception:
        st.error("DineWise could not load its local data or models. Check the terminal for details.")
        st.code("make setup\nmake download\nmake rebuild\nmake app", language="bash")
        import logging
        logging.getLogger(__name__).exception("Could not initialize DineWise")
        st.stop()

    with st.sidebar:
        st.subheader("🥄 A little about DineWise")
        st.caption("Local restaurant discovery, made for curious appetites.")
        st.divider()
        st.markdown("**Explore five cities**")
        for city in sorted(restaurants["city"].dropna().unique()):
            st.write(f"📍 {city}")
        st.caption(f"{len(restaurants):,} restaurants in the dataset")
        st.markdown("**Price guide**")
        st.markdown("$ — Budget-friendly  \n$$ — Moderate  \n$$$ — Higher-priced  \n$$$$ — Most expensive".replace("$", r"\$"))
        st.caption("Relative price categories, not exact meal prices. Unknown means no price is recorded.")
        st.markdown("**A quick note**")
        st.caption("Ratings and prices are static dataset values. Price buckets are not exact prices. "
                   "Review-based dietary claims are not guarantees.")
        st.caption("Each question is searched independently. Include your city and preferences each time.")
        if st.button("Clear conversation"):
            st.session_state.messages = []
            st.rerun()

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if not st.session_state.messages:
        st.markdown("""
<div class="welcome-card"><h3>What sounds good today?</h3>
<p>Tell me your city, what you're craving, your budget, or the atmosphere you're after.</p>
<p class="prompt-chips">🍝 Italian in Tampa · 🕯️ Quiet dinner in Tucson · 💸 Philadelphia under $$</p></div>
""", unsafe_allow_html=True)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                render_result(message["state"])
            else:
                st.markdown(message["content"])

    query = st.chat_input("e.g. Italian restaurants in Tampa under $$")
    if query and query.strip():
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
        with st.chat_message("assistant"):
            with st.spinner("Finding restaurants and reading the evidence…"):
                try:
                    state = run_query(graph, query)
                except Exception:
                    import logging
                    logging.getLogger(__name__).exception("Recommendation failed")
                    state = {"answer": "The recommendation service is temporarily unavailable. "
                             "Please try again later."}
                render_result(state)
                st.session_state.messages.append({"role": "assistant", "state": state})


if __name__ == "__main__":
    main()
