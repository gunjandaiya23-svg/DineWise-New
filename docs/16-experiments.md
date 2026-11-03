# Run comparisons in a useful order

Build the corpus once, then compare one factor at a time.

| Command | What changes | What it tells you |
|---|---|---|
| `make experiments` | BM25, dense, hybrid | Retrieval agreement, compliance and timing |
| `make retrieval-eval` | Retrieval mode | Ranking quality against silver labels |
| `make chunking-eval` | C1–C4 | Effect of chunk size and overlap |
| `make graph` | Fixed query suite | Workflow answers and fallbacks using templates by default |
| `make model-eval` | Base/LoRA, with/without RAG | Generation comparison |
| `make efficiency` | Precision and adapter | Memory and generation efficiency |

Chunking evaluation normally rebuilds indexes. To evaluate existing indexes without rebuilding:

```bash
.venv/bin/python scripts/13_chunking_experiments.py --reuse-indexes
```

The latest five-city comparison selected C4 by silver nDCG@5. The active configuration is explicit in the YAML; printing a best configuration does not automatically change it.

Keep query sets, labels and corpus fixed within a comparison. Historical experiment IDs remain in output names for traceability. Removed visual retrieval and reranking experiments are not part of the current supported pipeline.

[Documentation index](README.md)
