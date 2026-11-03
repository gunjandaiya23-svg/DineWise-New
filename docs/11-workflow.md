# Query workflow

The workflow in `src/dinewise/graph/workflow.py` uses ordinary Python and has no
LangGraph dependency. The historical module and build function names remain so
existing scripts can keep using the same entry point.

Scope checks reject live information, unsupported amenities, and cities outside
the current corpus. Retrieval combines lexical and semantic rankings and applies
structured constraints. Generation uses only the retrieved evidence.

Validation checks grounding and constraint compliance. A failed answer can be
regenerated once. Budget and attribute requirements remain unchanged. Empty
retrieval and repeated validation failures produce an explanatory fallback.

The app shows the query, supported cities, and resulting answer. Profiles, raw
ranking tables, model toggles, and developer traces are no longer UI controls.
