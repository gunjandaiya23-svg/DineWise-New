# How hybrid retrieval chooses restaurants

The app always uses hybrid retrieval. Research scripts also run BM25-only and dense-only modes through the same pipeline.

First, parsed constraints determine eligible business IDs from the structured catalogue. Unknown cities and unsupported amenities produce a refusal. City, cuisine, budget, rating and supported attributes are hard filters. Dietary terms are extracted but are not currently hard catalogue filters.

Next, dense retrieval ranks chunks by semantic similarity and BM25 ranks them by word matching. The default pool is 30; when constraints restrict the catalogue, the pipeline expands the pool to the chunk count so other cities cannot crowd eligible records out of a global shortlist.

Reciprocal Rank Fusion combines ranking positions:

```text
fused score = sum(1 / (60 + rank in each list))
```

Filtering removes chunks outside the eligible IDs after fusion. The system collapses remaining chunks to distinct restaurants, keeping the best evidence chunk for each. Score ties use rating, review count and ID for deterministic ordering. Up to five restaurants reach generation.

The output contains hits, constraints, filter counts and timing diagnostics. No hits leads to a fallback instead of an invented recommendation. Cross-encoder reranking and rating-prior reranking have been removed.

[Documentation index](README.md)
