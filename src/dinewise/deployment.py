"""Fetch the minimal prepared corpus needed by the public app."""

from __future__ import annotations

import os
from pathlib import Path

from .config import ROOT


def asset_files(name: str) -> tuple[str, ...]:
    return (
        "processed/restaurants.parquet",
        f"indexes/faiss/{name}/chunks.parquet",
        f"indexes/faiss/{name}/index.faiss",
        f"indexes/faiss/{name}/index_meta.json",
        f"indexes/bm25/{name}/bm25.pkl",
        f"indexes/bm25/{name}/bm25_meta.json",
    )


def ensure_assets(name: str) -> None:
    """Download missing app assets from a private Hugging Face dataset repo."""
    paths = asset_files(name)
    data_dir = ROOT / "data"
    missing = [path for path in paths if not (data_dir / path).is_file()]
    if not missing:
        return

    repo = os.environ.get("DINEWISE_ASSET_REPO")
    token = os.environ.get("HF_TOKEN")
    if not repo or not token:
        raise RuntimeError(
            "Prepared assets are missing. Set DINEWISE_ASSET_REPO and HF_TOKEN "
            "for deployment, or run the local data preparation steps."
        )
    from huggingface_hub import snapshot_download

    snapshot_download(
        repo_id=repo,
        repo_type="dataset",
        token=token,
        allow_patterns=missing,
        local_dir=Path(data_dir),
    )
    still_missing = [path for path in paths if not (data_dir / path).is_file()]
    if still_missing:
        raise FileNotFoundError(f"Deployment assets missing from {repo}: {still_missing}")
