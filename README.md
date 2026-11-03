# DineWise

A retrieval-augmented restaurant recommendation assistant, built as a controlled laboratory project.

The system answers questions such as *"Find Italian restaurants with vegetarian options under $$ in Philadelphia"* by retrieving restaurant records and review evidence, then generating a grounded recommendation with sources.

This is a research prototype over a static dataset. It is **not** a booking system and does not provide live availability or prices.

## Current corpus and comparisons

The default corpus covers **Philadelphia, Indianapolis, Tampa, New Orleans, and
Tucson**, with no 500-restaurant pilot cap. The prepared corpus contains 5,968
restaurants and 382,253 reviews.

Supported comparisons: BM25 / dense / hybrid RAG, C1–C4 chunking, base versus
LoRA generation, and FP16 / INT4 / INT8 quantization benchmarks.
Historical results under `results/` and the report describe the earlier pilot;
they are not measurements of the expanded corpus. Rerun evaluations after a rebuild.
C4 is the active chunk configuration after the five-city comparison (silver nDCG@5: 0.420).
Labels are automatically generated silver judgments; manual review remains needed.

## Quickstart

```bash
make setup        # create .venv (Python 3.12) and install dependencies
make check        # verify GPU, packages, and paths
make download     # fetch the dataset into data/raw with checksum verification
make prep         # clean the data and build data/processed/restaurants.parquet
make docs         # generate TXT restaurant evidence profiles
make chunks       # restaurant-aware token chunking
make index        # BGE embeddings + FAISS index
make bm25         # BM25 lexical index over the same chunks
make queries      # 15-query suite (12 answered + 3 refusals)
make experiments  # E1/E2/E3: BM25 vs dense vs hybrid comparison
```

To rebuild all four configurations for the five-city corpus, run `make rebuild`.
Use `make chunking-eval` to compare them (or add `--reuse-indexes` to
`scripts/13_chunking_experiments.py` to evaluate existing indexes).
Install training dependencies with `uv pip install --python .venv/bin/python -e ".[tuning]"`
before running `make lora-train` or quantization benchmarks.

Then:

```bash
make app          # launch the app
make test         # run unit tests
make lint         # ruff
```

## Repository layout

```
config/          configuration and taxonomy
data/            raw downloads, processed tables, documents, indexes (gitignored)
docs/            the project plan, one file per concern
scripts/         numbered pipeline steps
src/dinewise/    library code
tests/           unit tests for the data and validation layers
app/             simple Streamlit query interface
results/         run manifests and result tables
```

## Documentation

Start at [`docs/README.md`](docs/README.md). The plan is intentionally split by concern:

- [Overview and research questions](docs/01-overview.md)
- [Dataset and study corpus](docs/04-dataset.md)
- [Data engineering](docs/05-data-engineering.md)
- [Evaluation framework](docs/15-evaluation.md)
- [Roadmap](docs/18-roadmap.md)

## Data

The project uses the [Yelp Multimodal Recommendation dataset](https://huggingface.co/datasets/wzehui/Yelp-Multimodal-Recommendation), derived from the [Yelp Open Dataset](https://www.yelp.com/dataset). It is intended for educational, non-commercial research only. Raw data is not redistributed with this repository.

## License

Code: to be decided. Data: Yelp Open Dataset terms, non-commercial research use only.
