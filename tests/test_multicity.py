"""Regression checks for constrained retrieval across an expanded corpus."""
import pandas as pd

from dinewise.rag.constraints import extract_constraints
from dinewise.rag.pipeline import retrieve_with_config


def test_city_filter_does_not_lose_candidates_outside_global_top_pool():
    chunks = pd.DataFrame([
        {"chunk_id": str(i), "business_id": str(i), "city": "Tampa" if i == 39 else "Philadelphia"}
        for i in range(40)
    ])
    catalogue = chunks[["business_id", "city"]]

    class Dense:
        def search(self, query, k):
            return [{"chunk": row, "score": 1.0} for row in chunks.head(k).to_dict("records")]

    result = retrieve_with_config(Dense(), None, chunks, catalogue,
                                  "Restaurants in Tampa", mode="dense", pool=30)
    assert [hit["chunk"]["business_id"] for hit in result["hits"]] == ["39"]


def test_all_configured_cities_are_recognized():
    cities = ["Philadelphia", "Indianapolis", "Tampa", "New Orleans", "Tucson"]
    for city in cities:
        constraints = extract_constraints(f"Find restaurants in {city}.", known_cities=cities)
        assert constraints.city == city
        assert constraints.unknown_city is None


def test_missing_price_is_unknown_in_template_and_silver_labels():
    from dinewise.eval.goldset import _sort_key
    from dinewise.llm.generator import Generator

    row = {"business_id": "unknown-price", "price_range": pd.NA,
           "restaurant_name": "Example", "stars": 4.0, "review_count": 10}
    assert "price unknown" in Generator._template("recommend", [{"chunk": row}])
    assert _sort_key(pd.Series(row), "ranking")


def test_retry_preserves_budget_and_required_attributes():
    from dinewise.graph.nodes import make_nodes
    from dinewise.rag.constraints import Constraints

    constraints = Constraints(max_price_bucket=2, required_attributes=["outdoor_seating"])
    nodes = make_nodes({}, None, None, pd.DataFrame(),
                       pd.DataFrame({"city": ["Tampa"]}), None)
    state = {"constraints": constraints}
    state.update(nodes["retry"](state))
    assert state["constraints"] is constraints
    assert state["constraints"].max_price_bucket == 2
    assert state["constraints"].required_attributes == ["outdoor_seating"]
