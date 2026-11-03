# Evidence metadata

A chunk is a row in the chunk Parquet table, not a standalone restaurant record.

| Field | Meaning |
|---|---|
| `chunk_id` | Business ID plus profile section and chunk number |
| `business_id` | Join key back to the restaurant catalogue |
| `text` | Original excerpt with a restaurant marker |
| `restaurant_name`, `city`, `state` | Display and location metadata |
| `cuisine_primary`, `cuisine_tags` | Normalized cuisine fields |
| `price_range`, `stars`, `review_count` | Dataset values used in filtering and ranking |
| `source_file`, `document_type`, `section` | Evidence provenance |
| `token_count`, `char_count`, `chunk_config` | Chunk measurements and configuration |

`page` is present for compatibility but TXT profiles do not have page numbers. Missing metadata remains unknown. FAISS vector position must match the corresponding saved chunk-table row; BM25 uses chunk IDs to refer to the same evidence.

The profile manifest records file path, size information and SHA-256 checksum. Index manifests record model and chunk details. Inspect the actual generated manifest before relying on an optional field.

[Documentation index](../README.md)
