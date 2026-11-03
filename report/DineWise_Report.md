# DineWise technical report

DineWise recommends restaurants from a static research dataset. This report explains the implemented pipeline and distinguishes current five-city measurements from earlier pilot experiments.

## Corpus and source

The current prepared corpus covers Philadelphia, Indianapolis, Tampa, New Orleans, Tucson. It contains 5,968 restaurants and 382,253 reviews after food-service and venue selection. The configuration has no numeric restaurant cap. The [corpus audit](../results/tables/data_audit.json) records each selection step and missing-field rates.

Business, review, review-summary, photo-summary and photo-metadata CSV files are joined by business ID. Ratings, price buckets and open status are dataset values, not live facts. The source review records lack dates, so recency claims are unavailable.

## Data preparation

`make prep` writes `restaurants.parquet`, `reviews.parquet` and `corpus.json`. Structured fields drive exact filters; summaries and selected reviews provide descriptive evidence. `make docs` writes one marked TXT profile per restaurant. The chunker splits profiles independently, preventing a chunk from crossing restaurant boundaries.

## Search and generation

BGE-small-en-v1.5 embeds profile chunks for FAISS inner-product search. BM25 indexes words in the same chunks. A question is checked for unsupported live requests, then parsed into city, cuisine, budget and attribute constraints. The catalogue determines eligible IDs. Reciprocal Rank Fusion combines dense and BM25 positions, eligible chunks collapse to at most five restaurants, and Qwen2.5-1.5B-Instruct writes up to three recommendations. The app uses the base model with RAG. The LoRA adapter is evaluated by research scripts and is not loaded into the app.

## Validation and interface

The validator rejects cited IDs outside the retrieved candidates, certain live-information claims, and recorded price violations among cited restaurants. Names-only answers usually omit IDs, so the structured retrieval filter supplies the main price safeguard. Missing citations are soft failures. One failed generation may be retried with the same prompt and constraints; a repeated failure produces a fallback. The prompt asks for names; the chat strips leaked IDs while retaining them and excerpts in expandable evidence. A separate catalogue-backed summary shows price buckets and ratings for named recommendations.

## Five-city chunking comparison

Four configurations vary target window and overlap. C4 is active because its hybrid retrieval nDCG@5 was highest on the current silver labels: C1 0.375, C2 0.405, C3 0.400, C4 0.420. The embedding model reads at most 512 tokens, so longer chunks can be truncated during encoding. The `seconds` column in the reused-index run records embedding time from stored metadata, not the full rebuild duration.

| config | size | overlap | chunks | mean_tokens | chunks_with_multiple_markers | strict_success@k | strict_precision@k | strict_mrr | ndcg@k | index_bytes | seconds |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | 200 | 30 | 46576 | 211.802 | 0 | 0.333 | 0.067 | 0.138 | 0.375 | 71540781 | 146.340 |
| C2 | 400 | 60 | 24712 | 378.823 | 0 | 0.500 | 0.117 | 0.215 | 0.405 | 37957677 | 191.500 |
| C3 | 600 | 90 | 17567 | 520.682 | 0 | 0.417 | 0.100 | 0.200 | 0.400 | 26982957 | 191.910 |
| C4 | 800 | 120 | 12697 | 694.581 | 0 | 0.500 | 0.133 | 0.239 | 0.420 | 19502637 | 119.620 |

Selected: **C4** by nDCG@5.

## Five-city retrieval comparison

On the current C4 silver labels, hybrid has the highest strict Success@5 (0.500). BM25 has slightly higher nDCG@5 (0.429) than hybrid (0.420), while dense has 0.388. The metrics answer different questions: strict success asks whether a relevant result appears, while nDCG also rewards its ranking position and grade. These labels are automatically generated and await human review.

| Mode | Strict Success@5 | Strict P@5 | Strict MRR | nDCG@5 | Any Success@5 |
|---|---|---|---|---|---|
| bm25 | 0.333 | 0.133 | 0.236 | 0.429 | 1.000 |
| dense | 0.250 | 0.083 | 0.153 | 0.388 | 1.000 |
| hybrid | 0.500 | 0.133 | 0.239 | 0.420 | 1.000 |

## Workflow query suite

The fixed suite includes 12 intended answerable queries and three refusal scenarios. The graph-named script now runs a plain Python workflow. Its default template mode checks the retrieval and validation path without measuring Qwen's writing quality. Read the per-query artifact before interpreting fallback and validation counts.

| ID | Facet | Outcome | Passed | Retries | Hits | Seconds |
|---|---|---|---|---|---|---|
| Q01 | cuisine | answered | True | 0 | 5 | 0.83 |
| Q02 | budget | answered | True | 0 | 5 | 0.71 |
| Q03 | review_aspect | answered | True | 0 | 5 | 0.1 |
| Q04 | ambience | answered | True | 0 | 5 | 0.71 |
| Q05 | personalization | answered | True | 0 | 5 | 0.46 |
| Q06 | comparison | answered | True | 0 | 5 | 0.42 |
| Q07 | dessert | answered | True | 0 | 5 | 0.54 |
| Q08 | dietary | answered | True | 0 | 5 | 0.71 |
| Q09 | cuisine | answered | True | 0 | 5 | 0.4 |
| Q10 | cuisine | answered | True | 0 | 5 | 0.33 |
| Q11 | ranking | answered | True | 0 | 5 | 0.47 |
| Q12 | multi_constraint | answered | True | 0 | 5 | 0.51 |
| Q13 | out_of_scope | refused | False | 0 | 0 | 0.0 |
| Q14 | out_of_scope | fallback | False | 0 | 0 | 0.0 |
| Q15 | unsupported | fallback | False | 0 | 0 | 0.0 |

{
  "corpus": {
    "raw": {
      "businesses": 16702,
      "reviews": 837559,
      "review_summaries": 16702,
      "photo_summaries": 13289,
      "photos": 118951
    },
    "selection": {
      "cities": [
        "Philadelphia",
        "Indianapolis",
        "Tampa",
        "New Orleans",
        "Tucson"
      ],
      "limit": null,
      "after_city_filter": 6946,
      "after_food_service_filter": 6034,
      "venue_excluded": 66,
      "selected": 5968
    },
    "corpus": {
      "restaurants": 5968,
      "reviews": 382253,
      "with_review_summary": 5968,
      "with_photo_summary": 5364,
      "with_price": 5748,
      "cuisine_covered": 5759
    },
    "quality": {
      "duplicate_business_ids": 0,
      "duplicate_review_ids": 0,
      "attribute_parse_rate": 1.0,
      "missing_price_pct": 3.69,
      "cuisine_coverage_pct": 96.5,
      "review_join_coverage_pct": 100.0
    }
  },
  "mode": "template",
  "queries": 15,
  "answered": 12,
  "refused": 1,
  "fallbacks": 3,
  "validation_passed": 12,
  "retries": 0,
  "mean_seconds": 0.41
}

## Historical model and efficiency studies

The base/LoRA with and without RAG comparison and FP16/INT8/INT4 measurements were produced before the five-city expansion. They remain useful records of the earlier conditions but are not current five-city model results. A new comparison needs regenerated training examples, split review, retraining and matched evaluation conditions. See the [model table](../results/tables/models_E7_latest.md) and [efficiency table](../results/tables/efficiency_E8_latest.md).

## Limitations and next work

The dataset is static. Price symbols are ordinal buckets, not exact amounts; review-based dietary claims are not safety guarantees. The parser uses rules, and answer validation does not establish that every sentence is true. The small query suite and silver labels limit generalization. Next work is human review of labels, new five-city LoRA and quantization runs, and a retry strategy that responds to the actual validation failure. The [documentation index](../docs/README.md) contains implementation guides and runnable commands.
