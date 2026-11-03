# DineWise research report

Restaurant recommendations using structured filters, hybrid retrieval, and grounded generation.

## Current corpus

Cities: Philadelphia, Indianapolis, Tampa, New Orleans, Tucson

Restaurants: 5,968; reviews: 382,253.

## Implementation

Restaurant records and selected review evidence produce TXT profiles. Restaurant-aware token chunks feed BGE/FAISS and BM25 indexes. The Python workflow checks scope, retrieves evidence, generates an answer, and validates it. Retries preserve the user's constraints.

## Comparisons

- Retrieval: BM25, dense, and hybrid RRF.
- Chunking: C1 (200/30), C2 (400/60), C3 (600/90), C4 (800/120).
- Fine-tuning: base generation versus LoRA, with and without retrieval.
- Quantization: FP16, INT4, INT8, and LoRA INT4.

## Experiment artifacts

Historical tables may use the earlier 500-restaurant pilot. Check each run's provenance before comparing scores; corpus expansion does not automatically rerun model or efficiency benchmarks.

- [chunking_E5_latest](../results/tables/chunking_E5_latest.md)
- [efficiency_E8_latest](../results/tables/efficiency_E8_latest.md)
- [graph_E9_latest](../results/tables/graph_E9_latest.md)
- [models_E7_latest](../results/tables/models_E7_latest.md)
- [query15_latest](../results/tables/query15_latest.md)
- [retrieval_E1E2E3_latest](../results/tables/retrieval_E1E2E3_latest.md)
- [retrieval_metrics_latest](../results/tables/retrieval_metrics_latest.md)

## Limitations

Static dataset; no live availability or current prices. Dietary evidence is not a safety guarantee. Relevance labels are silver rubric judgments pending manual review.
