# Design decisions and source references

The current design favors a short local pipeline with explicit research comparisons.

| Decision | Reason |
|---|---|
| Five configured cities, no pilot cap | Broader coverage than the original Philadelphia pilot |
| TXT evidence profiles | One evidence format used by the actual chunking pipeline |
| BGE + FAISS and BM25 | Compare semantic retrieval with word matching and their combination |
| C1–C4 retained | Measure chunking effects under fixed queries and labels |
| C4 active | Highest silver nDCG@5 in the expanded-corpus comparison |
| Plain Python workflow | Fixed sequence does not require a graph framework |
| Base Qwen in the app | LoRA remains a separately evaluated research capability |
| Limited validation described explicitly | Passing checks is not proof of every factual claim |

Primary source identifiers are `wzehui/Yelp-Multimodal-Recommendation`, `BAAI/bge-small-en-v1.5` and `Qwen/Qwen2.5-1.5B-Instruct`. Inspect their model/dataset cards when changing usage or citing external model properties. Local code and run manifests are the source of truth for this project's behavior and measurements.

When changing a decision, update this guide, the relevant technical chapter and any affected run instructions in the same commit.

[Documentation index](README.md)
