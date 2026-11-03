<!-- DineWise result context -->
# Base/lora generation comparison

Historical pilot experiment. Its counts and scores describe the earlier run, not the current five-city app.  This is a latest-table pointer; use a timestamped `results/runs/` artifact for exact provenance.

| System | Format valid | Grounded | Hard pass | Live claims | Abstention | Seconds |
|---|---|---|---|---|---|---|
| base_no_rag | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 3.79 |
| base_rag | 1.0 | 0.8 | 1.0 | 0.0 | 0.0 | 4.92 |
| lora_rag | 1.0 | 0.8 | 1.0 | 0.0 | 0.0 | 4.94 |
| lora_no_rag | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 3.86 |
