# How raw records become usable tables

Run `make prep` to execute the cleaning pipeline. The input is the downloaded CSV files; the outputs are restaurant and review Parquet tables in `data/processed/`.

The pipeline selects configured cities, keeps food-service records, excludes unsuitable venue categories, and sorts the selected catalogue. It normalizes cuisines using the taxonomy and parses nested attribute values into usable columns. Missing values remain unknown rather than becoming negative claims.

Restaurant records are joined with summaries and photo metadata using `business_id`. Reviews are restricted to selected business IDs and cleaned before aggregate review statistics are attached to the catalogue.

`restaurants.parquet` supports exact filtering by city, cuisine, price bucket, rating and attributes. `reviews.parquet` supplies review evidence. `corpus.json` records selection counts, missing prices, cuisine coverage, duplicate IDs and join coverage.

A price bucket is an ordinal category from 1 to 4. It is not a dollar price. A restaurant with unknown price cannot satisfy an explicit maximum-price filter. Keep structured fields for filtering; use review text as supporting evidence.

[Documentation index](README.md)
