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

## Follow one constrained search

For “Italian in Tampa under $$”, filtering starts with all 5,968 restaurants, retains Tampa, then Italian cuisine, then recorded price buckets at most 2. The eligible business IDs are the final exact filter. Dense and BM25 ranking still search chunks, but the pipeline retains only chunks whose restaurant is eligible. A matching excerpt from a different city cannot enter the final answer.

RRF gives a chunk a contribution of `1/(60 + rank)` from each ranking in which it appears. A chunk ranked well by both methods gains more fused score than one seen only near the bottom of one list. After filtering, chunks collapse to distinct restaurants and the top five are sent to Qwen. If there are no eligible or retrieved restaurants, the workflow explains that the request could not be satisfied. Dietary terms currently do not impose this exact filtering behavior.

[Documentation index](README.md)
