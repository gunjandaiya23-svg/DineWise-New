# DineWise

DineWise is a local restaurant recommendation research project. It searches a static dataset, retrieves restaurant and review evidence, and asks Qwen to write recommendations grounded in that evidence. The Streamlit app supports Philadelphia, Indianapolis, Tampa, New Orleans, and Tucson. It cannot book a table or provide live prices, menus, hours or availability.

## Run the app

From the repository root, with the prepared data and indexes already present:

```bash
make app
```

Open `http://localhost:8501` if a browser does not open automatically. Ask, for example, **“Italian restaurants in Tampa under $$.”** The chat shows a response, a catalogue-backed price and rating summary, and expandable restaurant records and evidence excerpts. The sidebar explains `$` through `$$$$` as relative price buckets; they are not exact meal prices. The first supported request loads Qwen and can be slower. Stop the server with Ctrl+C.

If you have a fresh checkout without `.venv` or local data, follow [the environment guide](docs/03-environment.md). The short sequence is:

```bash
make setup       # Python 3.12 environment and app dependencies
make check       # Verify packages, CUDA and paths
make download    # Fetch source CSV files if absent
make rebuild     # Prepare five cities and build C1–C4 FAISS/BM25 indexes
make app
```

For a public CPU demo using Hugging Face inference, follow the [deployment guide](docs/22-deployment.md).

`make rebuild` can take several minutes. Restart Streamlit after a rebuild because it caches loaded resources.

## What happens to a question

```text
Question → scope check → parse city/cuisine/price/attributes
         → filter restaurant catalogue → BGE/FAISS + BM25 search
         → RRF fusion → up to five distinct restaurant records
         → Qwen answer → validation → answer or fallback
```

A query is searched independently; displayed earlier chat messages are not passed to the next search. Business IDs stay in internal validation and source panels but are hidden from the main answer. A hard validation failure triggers one deterministic regeneration attempt, which can repeat the same text. [Architecture](docs/02-architecture.md) and [query workflow](docs/11-workflow.md) explain each step with examples.

## Current data and comparisons

The prepared corpus contains **5,968 restaurants and 382,253 reviews** across the five configured cities, with no 500-restaurant cap. C4 is the active chunk configuration; its five-city hybrid retrieval nDCG@5 was 0.420 on automatically generated silver labels. In the current C4 retrieval comparison, hybrid has higher strict Success@5 (0.500), while BM25 has slightly higher nDCG@5 (0.429 versus 0.420). These are different measures, and labels still need human review.

The project preserves research comparisons for BM25/dense/hybrid retrieval, C1–C4 chunking, base versus LoRA generation with and without RAG, and FP16/INT8/INT4 performance. The app uses **base Qwen with RAG**; it does not load the trained LoRA adapter. Existing adapter and quantization results predate the five-city expansion and have not been rerun on the new corpus. The [technical report](report/DineWise_Report.md) distinguishes current and historical measurements.

Useful commands:

```bash
make test             # Unit and regression tests
make lint             # Static code checks
make goldset          # Rebuild silver labels for the prepared corpus
make retrieval-eval   # BM25, dense and hybrid metrics
make graph            # Fixed query suite in template mode
make model-eval       # Base/LoRA, with and without retrieval
make efficiency       # Precision and adapter benchmarks
make report           # Regenerate the technical report from current artifacts
```

`make chunking-eval` rebuilds configurations during evaluation. To compare already built indexes, run `.venv/bin/python scripts/13_chunking_experiments.py --reuse-indexes`. LoRA and quantization commands need the `[tuning]` extras described in [fine-tuning](docs/13-finetuning.md).

## Repository map

| Location | Purpose |
|---|---|
| `app/` and `.streamlit/` | Chat interface and theme |
| `src/dinewise/data/` | Cleaning and evidence profile construction |
| `src/dinewise/rag/` | Chunking, constraints, indexes and retrieval |
| `src/dinewise/llm/` | Prompts, Qwen generation and validation |
| `src/dinewise/graph/` | Plain Python workflow, under a historical folder name |
| `scripts/` | Build, training, evaluation and reporting commands |
| `config/` | Corpus, model, chunking and retrieval settings |
| `data/` | Local source files and generated data; large inputs are gitignored |
| `results/` | Timestamped experiment artifacts and latest tables |

Start with [the documentation index](docs/README.md) for the complete technical guides, output references, limitations and current roadmap. The dataset is [Yelp Multimodal Recommendation](https://huggingface.co/datasets/wzehui/Yelp-Multimodal-Recommendation), derived from Yelp data for educational, non-commercial research. Raw data is not redistributed here. The code license has not yet been chosen; dataset usage is governed by its source terms.
