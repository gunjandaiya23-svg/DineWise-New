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

## Reproducible comparison checklist

1. Record the corpus audit and active chunk configuration. Rebuild indexes after corpus or chunk changes.
2. Build or review the gold set for the same corpus and fixed queries. Mark whether labels are silver or manually judged.
3. Change one variable per comparison: retrieval mode for retrieval evaluation, chunk configuration for C1–C4, or model/adapter for generation evaluation.
4. Read the timestamped run JSON and table together. Note the input corpus and label source before comparing with an older run.

The C4 five-city retrieval evaluation shows different winners depending on metric: hybrid strict Success@5 is 0.500, while BM25 nDCG@5 is 0.429 versus hybrid 0.420. The C4 selection comes from the separate chunking experiment in hybrid mode. Training and quantization tables come from older conditions until they are rerun.

[Documentation index](README.md)
