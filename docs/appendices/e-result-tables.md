# Read result artifacts correctly

Timestamped directories under `results/runs/` preserve individual experiment outputs. Tables under `results/tables/` point to recent summaries and can be overwritten by later runs.

Read the JSON beside a table to identify the corpus, label source, model settings and per-query details available for that run. Some historical artifacts lack complete provenance. Do not substitute current settings for missing historical metadata.

Chunking tables compare sizes, overlap, chunk count, contamination and retrieval metrics. Retrieval tables compare BM25, dense and hybrid ranking. Model tables compare base/LoRA with and without RAG. Efficiency tables compare numerical precision and adapter use.

When indexes are reused in chunking evaluation, the `seconds` column comes from stored embedding time; it is not total end-to-end rebuilding time. In a normal fresh chunking evaluation it measures the build operation. Avoid comparing those timing columns across the two execution modes.

Silver relevance metrics and validation-pass rates are different measurements. Include their definitions and limitations with any exported chart or report.

[Documentation index](../README.md)
