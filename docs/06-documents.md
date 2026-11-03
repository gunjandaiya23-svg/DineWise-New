# Evidence profiles

The profile builder turns the cleaned tables into text that a search model can read. Run `make prep` first, then `make docs`. The input is `data/processed/restaurants.parquet` plus `reviews.parquet`; the output is `data/docs/restaurant_profiles.txt` and `doc_manifest.json`.

## What one profile contains

A profile begins with `[RESTAURANT <business_id>]`. The next lines hold the name, city, normalized cuisine, price bucket, dataset rating, attribute values, review summary, photo description when present, and selected customer review excerpts. The source line identifies the source CSV families. An abbreviated example looks like this:

```text
[RESTAURANT abc123]
Name: Example Bistro
City: Tampa, FL
Cuisine: Italian
Price: $$ (dataset bucket 2 of 4)
Rating: 4.5 out of 5 (dataset average, 289 reviews)
Review summary: Guests praise the pasta and service.
Customer review evidence:
[review-7] 5 stars: The pasta was excellent.
```

This is an illustration of the format, not a real restaurant record. The marker is important: the chunker uses it to find restaurant boundaries, and adds the marker to each chunk it produces. A review remains evidence attached to its restaurant; it does not become a separate search document.

## How evidence is chosen

The builder selects up to eight reviews per restaurant by combining highly rated, low rated, and long reviews, then removes duplicate review IDs. This creates a repeatable mix. Each excerpt is shortened, so the full `reviews.parquet` table remains the source when someone needs more context. Review summaries come from the source dataset and can be wrong; they should not be treated as verified facts.

The manifest records the restaurant count, file path, character count, build time, and SHA-256 checksum. Check that manifest when comparing two builds. PDF and DOCX exports from the earlier prototype are no longer part of the pipeline. The TXT profile is the actual input to chunking.

Continue with [chunking](07-chunking.md) to see how these blocks become searchable records.
