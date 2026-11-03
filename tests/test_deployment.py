"""Deployment configuration and hosted inference contract."""

from __future__ import annotations

import sys
from types import SimpleNamespace

from dinewise.config import load_config
from dinewise.deployment import asset_files
from dinewise.llm.generator import Generator


def test_hosted_mode_uses_cpu_and_only_active_assets(monkeypatch):
    monkeypatch.setenv("DINEWISE_INFERENCE_MODE", "hf")
    cfg = load_config()
    assert cfg["embedding"]["device"] == "cpu"
    assert asset_files(cfg["chunking"]["active"]) == (
        "processed/restaurants.parquet",
        "indexes/faiss/C4/chunks.parquet",
        "indexes/faiss/C4/index.faiss",
        "indexes/faiss/C4/index_meta.json",
        "indexes/bm25/C4/bm25.pkl",
        "indexes/bm25/C4/bm25_meta.json",
    )


def test_hosted_generation_sends_grounded_messages(monkeypatch):
    monkeypatch.setenv("DINEWISE_INFERENCE_MODE", "hf")
    monkeypatch.setenv("HF_TOKEN", "test-token")
    sent = {}

    class FakeCompletions:
        def create(self, **kwargs):
            sent.update(kwargs)
            return SimpleNamespace(
                choices=[SimpleNamespace(message=SimpleNamespace(content="  Answer  "))]
            )

    class FakeClient:
        def __init__(self, api_key):
            assert api_key == "test-token"
            self.chat = SimpleNamespace(completions=FakeCompletions())

    monkeypatch.setitem(sys.modules, "huggingface_hub", SimpleNamespace(InferenceClient=FakeClient))
    cfg = load_config()
    hit = {"chunk": {
        "business_id": "abc", "restaurant_name": "Example Cafe", "city": "Tampa",
        "state": "FL", "cuisine_primary": "Italian", "price_range": 2,
        "stars": 4.5, "text": "Pasta and quiet seating.",
    }}
    assert Generator(cfg).generate("Quiet Italian in Tampa", [hit]) == "Answer"
    assert sent["model"] == "Qwen/Qwen2.5-72B-Instruct"
    assert "Example Cafe" in sent["messages"][1]["content"]
