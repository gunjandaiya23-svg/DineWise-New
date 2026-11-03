# How profiles become searchable chunks

Run `make chunks` for the active configuration or `make rebuild` for all four. Input is the restaurant profile TXT file; output is `data/processed/chunks_C*.parquet`.

The chunker first separates restaurant blocks by their markers. It tokenizes each block independently and creates overlapping windows. No chunk should contain evidence from two restaurants. Offset mappings preserve the original text and casing; a tokenizer-decode fallback is available.

| Configuration | Target tokens | Overlap |
|---|---:|---:|
| C1 | 200 | 30 |
| C2 | 400 | 60 |
| C3 | 600 | 90 |
| C4 | 800 | 120 |

Short tails can be merged and restaurant headers are added, so final token counts can exceed the target. Each chunk carries its business ID, restaurant metadata, source and configuration.

C4 is active after the five-city comparison and produces 12,697 chunks. The embedding model reads at most 512 tokens: longer chunks are truncated during embedding. This matters when interpreting the size comparison; the full excerpt remains available for generation.

Contamination checks count chunks containing multiple restaurant markers. Evaluate all sizes against the same queries and labels.

[Documentation index](README.md)
