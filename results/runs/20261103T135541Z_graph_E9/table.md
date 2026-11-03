<!-- DineWise result context -->
# Experiment result

Five-city corpus (5,968 restaurants), generated on 2026-11-03.  See [the run JSON](results.json) for per-query data and available provenance.

| ID | Facet | Outcome | Passed | Retries | Hits | Seconds |
|---|---|---|---|---|---|---|
| Q01 | cuisine | answered | True | 0 | 5 | 1.35 |
| Q02 | budget | answered | True | 0 | 5 | 1.19 |
| Q03 | review_aspect | answered | True | 0 | 5 | 0.14 |
| Q04 | ambience | answered | True | 0 | 5 | 1.18 |
| Q05 | personalization | answered | True | 0 | 5 | 0.69 |
| Q06 | comparison | answered | True | 0 | 5 | 0.56 |
| Q07 | dessert | answered | True | 0 | 5 | 0.7 |
| Q08 | dietary | answered | True | 0 | 5 | 0.93 |
| Q09 | cuisine | answered | True | 0 | 5 | 0.6 |
| Q10 | cuisine | answered | True | 0 | 5 | 0.7 |
| Q11 | ranking | answered | True | 0 | 5 | 0.77 |
| Q12 | multi_constraint | answered | True | 0 | 5 | 0.55 |
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
  "mean_seconds": 0.62
}
