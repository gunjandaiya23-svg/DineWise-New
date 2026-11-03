# The dataset and city coverage

Raw files live in `data/raw/`. `business.csv` contains restaurant identifiers and structured details; `review.csv` contains review text. Review and photo-summary files add text descriptions, and `photo.csv` supplies photo metadata.

`business_id` joins these sources. Photo descriptions are text supplied upstream; they are not image embeddings. The source has a misspelled `photo_summay.csv` filename, which the data loader handles.

The active corpus selects Philadelphia, Indianapolis, Tampa, New Orleans, and Tucson with no restaurant-count cap. After food-service selection and venue exclusion, the prepared corpus has 5,968 restaurants and 382,253 reviews. Read `data/processed/corpus.json` for the latest measured counts and quality audit.

These are static records. Dataset ratings, prices and open/closed fields do not establish current conditions. The source review schema lacks dates, so the project cannot make reliable recency comparisons.

The data derives from Yelp and is intended for educational, non-commercial research. The source is [the Hugging Face dataset](https://huggingface.co/datasets/wzehui/Yelp-Multimodal-Recommendation). Raw records and model artifacts stay out of git.

## How to read the corpus counts

`corpus.json` starts with 16,702 source businesses and 837,559 source reviews. Filtering the configured cities leaves 6,946 businesses; food-service selection and venue exclusion reduce this to 5,968 restaurants. The final review table has 382,253 reviews for those restaurants. These numbers are measured outputs of the current preparation run, so inspect the JSON after any configuration change.

City coverage is determined from `restaurants.parquet`, which is also what the app sidebar reads. The five-city configuration has no numeric restaurant cap. A query for a city outside the catalogue is refused rather than silently searching another city. A missing price or attribute means the dataset did not record it; it does not imply an inexpensive restaurant or an absent amenity.

[Documentation index](README.md)
