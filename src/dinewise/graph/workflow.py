"""Run the DineWise retrieval and validated generation workflow."""

from __future__ import annotations

from typing import Any

from .nodes import make_nodes, route_after_classify, route_after_retrieve, route_after_review


def build_graph(
    cfg: dict[str, Any],
    retriever: Any,
    bm25: Any,
    chunks: Any,
    restaurants: Any,
    generator: Any,
):
    nodes = make_nodes(cfg, retriever, bm25, chunks, restaurants, generator)

    class Workflow:
        def invoke(self, initial):
            state = dict(initial)
            def step(name):
                state.update(nodes[name](state))
            step("classify")
            if route_after_classify(state) == "fallback":
                step("fallback")
                return state
            step("retrieve")
            if route_after_retrieve(state) == "fallback":
                step("fallback")
                return state
            while True:
                step("generate")
                step("review")
                route = route_after_review(state, max_retries=int(cfg["workflow"]["max_retries"]))
                if route == "end":
                    return state
                if route == "fallback":
                    break
                step("retry")
            step("fallback")
            return state

    return Workflow()


def run_query(graph, query: str) -> dict[str, Any]:
    return graph.invoke({"query": query})
