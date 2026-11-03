#!/usr/bin/env python
"""Summarize the current corpus and link measured experiment results."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    corpus_path = ROOT / "data/processed/corpus.json"
    corpus = json.loads(corpus_path.read_text()) if corpus_path.exists() else None
    lines = ["# DineWise research report", "",
             "Restaurant recommendations using structured filters, hybrid retrieval, "
             "and grounded generation.", "", "## Current corpus", ""]
    if corpus:
        lines.extend([
            "Cities: " + ", ".join(corpus["selection"]["cities"]), "",
            f"Restaurants: {corpus['corpus']['restaurants']:,}; "
            f"reviews: {corpus['corpus']['reviews']:,}.", "",
        ])
    else:
        lines.extend(["Run `make prep` to measure the corpus.", ""])
    lines.extend([
        "## Implementation", "",
        "Restaurant records and selected review evidence produce TXT profiles. "
        "Restaurant-aware token chunks feed BGE/FAISS and BM25 indexes. "
        "The Python workflow checks scope, retrieves evidence, generates an answer, "
        "and validates it. Retries preserve the user's constraints.", "",
        "## Comparisons", "",
        "- Retrieval: BM25, dense, and hybrid RRF.",
        "- Chunking: C1 (200/30), C2 (400/60), C3 (600/90), C4 (800/120).",
        "- Fine-tuning: base generation versus LoRA, with and without retrieval.",
        "- Quantization: FP16, INT4, INT8, and LoRA INT4.", "",
        "## Experiment artifacts", "",
        "Historical tables may use the earlier 500-restaurant pilot. "
        "Check each run's provenance before comparing scores; corpus expansion "
        "does not automatically rerun model or efficiency benchmarks.", "",
    ])
    for path in sorted((ROOT / "results/tables").glob('*latest.md')):
        lines.append(f"- [{path.stem}]({path.relative_to(ROOT).as_posix().replace('results/', '../results/', 1)})")
    lines.extend(["", "## Limitations", "",
                  "Static dataset; no live availability or current prices. "
                  "Dietary evidence is not a safety guarantee. Relevance labels are "
                  "silver rubric judgments pending manual review.", ""])
    output = ROOT / "report/DineWise_Report.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {output}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
