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

## Why the marker and overlap matter

A restaurant profile can exceed one model input window. The chunker starts a new token window before the previous one ends, so a phrase near a boundary can appear in both chunks. Its restaurant marker is repeated on each output chunk; retrieval can therefore map a matching excerpt back to its business. The contamination report verifies that a chunk does not contain multiple restaurant markers.

For the five-city corpus, C1/C2/C3/C4 produced 46,576 / 24,712 / 17,567 / 12,697 chunks. Larger targets usually produce fewer chunks and smaller indexes, but they can contain more unrelated text and exceed BGE's 512-token input limit. The latest silver-label comparison chose C4 by hybrid nDCG@5; that result is specific to this corpus, query set, and metric. Rebuild indexes after changing window settings.

[Documentation index](README.md)
