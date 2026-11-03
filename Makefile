PY := .venv/bin/python
PIP := uv pip install --python $(PY)

.PHONY: rebuild setup check download prep docs chunks index bm25 queries experiments goldset retrieval-eval chunking-eval graph lora-data lora-train model-eval efficiency report app test lint clean

setup:
	UV_HTTP_TIMEOUT=600 uv venv --python 3.12 .venv
	UV_HTTP_TIMEOUT=600 $(PIP) torch --index-url https://download.pytorch.org/whl/cu128
	UV_HTTP_TIMEOUT=600 $(PIP) -e ".[dev,app]"

check:
	$(PY) scripts/00_setup_check.py

download:
	$(PY) scripts/01_download_data.py

prep:
	$(PY) scripts/02_prepare_data.py

docs:
	$(PY) scripts/03_build_documents.py

chunks:
	$(PY) scripts/04_build_chunks.py

index: chunks
	$(PY) scripts/05_build_index.py

rebuild:
	$(PY) scripts/02_prepare_data.py
	$(PY) scripts/03_build_documents.py
	for name in C1 C2 C3 C4; do $(PY) scripts/04_build_chunks.py --config-name $$name && $(PY) scripts/05_build_index.py --config-name $$name && $(PY) scripts/09_build_bm25.py --config-name $$name || exit 1; done
	$(PY) scripts/11_build_goldset.py

bm25:
	$(PY) scripts/09_build_bm25.py

queries:
	$(PY) scripts/08_run_queries.py

experiments:
	$(PY) scripts/10_retrieval_experiments.py

goldset:
	$(PY) scripts/11_build_goldset.py

retrieval-eval:
	$(PY) scripts/12_retrieval_metrics.py

chunking-eval:
	$(PY) scripts/13_chunking_experiments.py

graph:
	$(PY) scripts/14_run_graph.py

lora-data:
	$(PY) scripts/16_build_lora_data.py

lora-train:
	$(PY) scripts/17_train_lora.py

model-eval:
	$(PY) scripts/18_eval_models.py

efficiency:
	$(PY) scripts/19_efficiency.py

report:
	$(PY) scripts/20_build_report.py

app:
	$(PY) -m streamlit run app/streamlit_app.py

test:
	$(PY) -m pytest

lint:
	$(PY) -m ruff check src scripts tests

clean:
	rm -rf data/processed data/indexes data/docs/*.pdf data/docs/*.docx data/docs/*.txt
