<!-- DineWise result context -->
# Experiment result

Five-city corpus (5,968 restaurants), generated on 2026-11-03.  See [the run JSON](results.json) for per-query data and available provenance.

| config | size | overlap | chunks | mean_tokens | chunks_with_multiple_markers | strict_success@k | strict_precision@k | strict_mrr | ndcg@k | index_bytes | seconds |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | 200 | 30 | 46576 | 211.802 | 0 | 0.333 | 0.067 | 0.138 | 0.375 | 71540781 | 146.340 |
| C2 | 400 | 60 | 24712 | 378.823 | 0 | 0.500 | 0.117 | 0.215 | 0.405 | 37957677 | 191.500 |
| C3 | 600 | 90 | 17567 | 520.682 | 0 | 0.417 | 0.100 | 0.200 | 0.400 | 26982957 | 191.910 |
| C4 | 800 | 120 | 12697 | 694.581 | 0 | 0.500 | 0.133 | 0.239 | 0.420 | 19502637 | 119.620 |

Selected: **C4** by nDCG@5.
