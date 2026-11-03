"""Upload only the active app assets to a private Hugging Face dataset repo."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from huggingface_hub import HfApi

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from dinewise.config import load_config  # noqa: E402
from dinewise.deployment import asset_files  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", help="Hugging Face dataset repository, e.g. user/dinewise-assets")
    args = parser.parse_args()
    token = os.environ.get("HF_TOKEN")
    if not token:
        parser.error("HF_TOKEN must be set to a write-capable Hugging Face token")
    name = load_config()["chunking"]["active"]
    files = asset_files(name)
    for file in files:
        if not (ROOT / "data" / file).is_file():
            parser.error(f"Missing prepared asset: data/{file}. Run make rebuild first.")

    api = HfApi(token=token)
    api.create_repo(args.repo, repo_type="dataset", private=True, exist_ok=True)
    if not api.repo_info(args.repo, repo_type="dataset").private:
        parser.error("Destination dataset repository must be private")
    for file in files:
        print(f"Uploading {file}")
        api.upload_file(
            path_or_fileobj=str(ROOT / "data" / file),
            path_in_repo=file,
            repo_id=args.repo,
            repo_type="dataset",
        )
    print(f"Uploaded {len(files)} assets to private repository {args.repo}")


if __name__ == "__main__":
    main()
