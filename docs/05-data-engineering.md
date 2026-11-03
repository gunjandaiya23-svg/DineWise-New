# How raw records become usable tables

Run `make prep` to execute the cleaning pipeline. The input is the downloaded CSV files; the outputs are restaurant and review Parquet tables in `data/processed/`.

The pipeline selects configured cities, keeps food-service records, excludes unsuitable venue categories, and sorts the selected catalogue. It normalizes cuisines using the taxonomy and parses nested attribute values into usable columns. Missing values remain unknown rather than becoming negative claims.

Restaurant records are joined with summaries and photo metadata using `business_id`. Reviews are restricted to selected business IDs and cleaned before aggregate review statistics are attached to the catalogue.

`restaurants.parquet` supports exact filtering by city, cuisine, price bucket, rating and attributes. `reviews.parquet` supplies review evidence. `corpus.json` records selection counts, missing prices, cuisine coverage, duplicate IDs and join coverage.

A price bucket is an ordinal category from 1 to 4. It is not a dollar price. A restaurant with unknown price cannot satisfy an explicit maximum-price filter. Keep structured fields for filtering; use review text as supporting evidence.

## Worked join and filter example

If a business row has `business_id=abc123`, the summary and photo rows with that same ID add descriptive fields, and review rows with that ID become evidence for its profile. Normalized cuisine tags make “Italian” usable as a filter even when source categories have varied wording. Parsed price bucket 2 is displayed as `$$`; it never becomes an invented amount in dollars.

The preparation audit records row counts after city selection and food-service filtering, as well as missing-price and cuisine-coverage rates. A query with `max_price_bucket=2` keeps businesses with recorded bucket 1 or 2 and excludes unknown prices. Review summaries and photo descriptions can help explain a result, but the structured fields control these exact filters. This prevents a review mentioning “cheap” from overriding a recorded higher price bucket.

[Documentation index](README.md)
