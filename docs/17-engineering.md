# Where the code and artifacts live

The repository separates reusable library code from commands and generated artifacts.

| Location | Responsibility |
|---|---|
| `app/` | Streamlit interface |
| `src/dinewise/data/` | Cleaning and profile construction |
| `src/dinewise/rag/` | Chunking, indexes, constraints and retrieval |
| `src/dinewise/llm/` | Prompts, generation and validation |
| `src/dinewise/graph/` | Plain Python workflow; historical folder name |
| `scripts/` | Build, training and evaluation commands |
| `config/` | Runtime settings and taxonomy |
| `results/` | Evaluation runs and summary tables |

`config/config.yaml` chooses corpus cities, active chunking, models, retrieval limits and retry count. Changes to embedding or chunking settings require matching index rebuilds. Cached app resources require a server restart afterward.

Use `make test` and `make lint` after code changes. Add regression tests for behavior changes rather than testing only internal implementation details. Keep raw data, model weights and runtime logs out of commits.

Each experiment should preserve its configuration, corpus and label provenance. Some historical manifests contain less detail; do not infer missing provenance from the current config.

[Documentation index](README.md)
