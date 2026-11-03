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

The app uses a warm light chat layout with supported cities in the sidebar.
Session history keeps questions, answers, restaurant records and evidence excerpts.
Each question is searched independently; earlier messages are not passed to Qwen.
Clear conversation resets the session history. Profiles, raw ranking tables, model
toggles and developer traces are not exposed as controls.
