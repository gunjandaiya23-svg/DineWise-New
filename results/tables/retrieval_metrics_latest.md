<!-- DineWise result context -->
# Bm25, dense and hybrid retrieval metrics against silver labels

Five-city corpus (5,968 restaurants), generated on 2026-11-03. Labels are automatically generated silver judgments; manual review is pending. This is a latest-table pointer; use a timestamped `results/runs/` artifact for exact provenance.

| Mode | Strict Success@5 | Strict P@5 | Strict MRR | nDCG@5 | Any Success@5 |
|---|---|---|---|---|---|
| bm25 | 0.333 | 0.133 | 0.236 | 0.429 | 1.000 |
| dense | 0.250 | 0.083 | 0.153 | 0.388 | 1.000 |
| hybrid | 0.500 | 0.133 | 0.239 | 0.420 | 1.000 |
