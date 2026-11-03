# Run the app and prepare the environment

From the repository root, run:

```bash
make app
```

Open http://localhost:8501 and enter a query such as “Italian restaurants in Tampa under $$”. Stop the server with Ctrl+C. The existing data and indexes are ready; normal startup does not rebuild them.

The project requires Python 3.12. The current embedding configuration uses CUDA. For a new installation with uv available, run `make setup` and `make check`. Setup creates `.venv`, installs CUDA-enabled PyTorch and the app dependencies. It does not download and prepare the restaurant corpus.

If raw data is absent, run `make download`. Then `make rebuild` prepares all five cities and all four sets of indexes. This takes substantially longer than launching the app.

Training and quantization need additional packages:

```bash
uv pip install --python .venv/bin/python -e ".[tuning]"
```

Streamlit caches resources in the running process. Qwen loads lazily on the first supported recommendation. Restart the app after rebuilding indexes to clear cached assets.

[Documentation index](README.md)
