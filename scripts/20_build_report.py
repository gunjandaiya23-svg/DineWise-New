#!/usr/bin/env python
"""Build a readable report from the current corpus and available result tables."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_table(name: str) -> str | None:
    path = ROOT / "results" / "tables" / name
    if not path.exists():
        return None
    lines = path.read_text(encoding="utf-8").splitlines()
    first_table = next((index for index, line in enumerate(lines) if line.startswith("|")), None)
    return "\n".join(lines[first_table:]).strip() if first_table is not None else None


def section(title: str, body: str, table: str | None = None) -> list[str]:
    lines = [f"## {title}", "", body.strip(), ""]
    if table:
        lines.extend([table, ""])
    return lines


def main() -> int:
    audit_path = ROOT / "data" / "processed" / "corpus.json"
    audit = json.loads(audit_path.read_text(encoding="utf-8")) if audit_path.exists() else None
    if audit:
        selection = audit["selection"]
        measured = audit["corpus"]
        corpus_text = (
            f"The current prepared corpus covers {', '.join(selection['cities'])}. "
            f"It contains {measured['restaurants']:,} restaurants and "
            f"{measured['reviews']:,} reviews after food-service and venue selection. "
            f"The configuration has no numeric restaurant cap. "
            f"The [corpus audit](../results/tables/data_audit.json) records each selection "
            f"step and missing-field rates."
        )
    else:
        corpus_text = "Run `make prep` to measure the current corpus before quoting counts."

    lines = ["# DineWise technical report", "",
             "DineWise recommends restaurants from a static research dataset. This report "
             "explains the implemented pipeline and distinguishes current five-city "
             "measurements from earlier pilot experiments.", ""]
    lines += section("Corpus and source", corpus_text + "\n\nBusiness, review, review-summary, "
                     "photo-summary and photo-metadata CSV files are joined by business ID. "
                     "Ratings, price buckets and open status are dataset values, not live facts. "
                     "The source review records lack dates, so recency claims are unavailable.")
    lines += section("Data preparation", "`make prep` writes `restaurants.parquet`, "
                     "`reviews.parquet` and `corpus.json`. Structured fields drive exact "
                     "filters; summaries and selected reviews provide descriptive evidence. "
                     "`make docs` writes one marked TXT profile per restaurant. The chunker "
                     "splits profiles independently, preventing a chunk from crossing "
                     "restaurant boundaries.")
    lines += section("Search and generation", "BGE-small-en-v1.5 embeds profile chunks for "
                     "FAISS inner-product search. BM25 indexes words in the same chunks. "
                     "A question is checked for unsupported live requests, then parsed "
                     "into city, cuisine, budget and attribute constraints. The catalogue "
                     "determines eligible IDs. Reciprocal Rank Fusion combines dense and "
                     "BM25 positions, eligible chunks collapse to at most five restaurants, "
                     "and Qwen2.5-1.5B-Instruct writes up to three recommendations. "
                     "The app uses the base model with RAG. The LoRA adapter is evaluated "
                     "by research scripts and is not loaded into the app.")
    lines += section("Validation and interface", "The validator rejects cited IDs outside "
                     "the retrieved candidates, certain live-information claims, and "
                     "recorded price violations among cited restaurants. Names-only answers "
                     "usually omit IDs, so the structured retrieval filter supplies the main "
                     "price safeguard. Missing citations are soft failures. One failed "
                     "generation may be retried with the same "
                     "prompt and constraints; a repeated failure produces a fallback. "
                     "The prompt asks for names; the chat strips leaked IDs while retaining them and "
                     "excerpts in expandable evidence. A separate catalogue-backed summary "
                     "shows price buckets and ratings for named recommendations.")

    chunk = read_table("chunking_E5_latest.md")
    lines += section("Five-city chunking comparison", "Four configurations vary target "
                     "window and overlap. C4 is active because its hybrid retrieval "
                     "nDCG@5 was highest on the current silver labels: C1 0.375, C2 0.405, "
                     "C3 0.400, C4 0.420. The embedding model reads at most 512 tokens, "
                     "so longer chunks can be truncated during encoding. The `seconds` "
                     "column in the reused-index run records embedding time from stored "
                     "metadata, not the full rebuild duration.", chunk)
    retrieval = read_table("retrieval_metrics_latest.md")
    lines += section("Five-city retrieval comparison", "On the current C4 silver labels, "
                     "hybrid has the highest strict Success@5 (0.500). BM25 has slightly "
                     "higher nDCG@5 (0.429) than hybrid (0.420), while dense has 0.388. "
                     "The metrics answer different questions: strict success asks whether "
                     "a relevant result appears, while nDCG also rewards its ranking "
                     "position and grade. These labels are automatically generated and "
                     "await human review.", retrieval)
    graph = read_table("graph_E9_latest.md")
    lines += section("Workflow query suite", "The fixed suite includes 12 intended "
                     "answerable queries and three refusal scenarios. The graph-named "
                     "script now runs a plain Python workflow. Its default template mode "
                     "checks the retrieval and validation path without measuring Qwen's "
                     "writing quality. Read the per-query artifact before interpreting "
                     "fallback and validation counts.", graph)
    lines += section("Historical model and efficiency studies", "The base/LoRA with and "
                     "without RAG comparison and FP16/INT8/INT4 measurements were produced "
                     "before the five-city expansion. They remain useful records of the "
                     "earlier conditions but are not current five-city model results. "
                     "A new comparison needs regenerated training examples, split review, "
                     "retraining and matched evaluation conditions. See the "
                     "[model table](../results/tables/models_E7_latest.md) and "
                     "[efficiency table](../results/tables/efficiency_E8_latest.md).")
    lines += section("Limitations and next work", "The dataset is static. Price symbols "
                     "are ordinal buckets, not exact amounts; review-based dietary claims "
                     "are not safety guarantees. The parser uses rules, and answer validation "
                     "does not establish that every sentence is true. The small query suite "
                     "and silver labels limit generalization. Next work is human review of "
                     "labels, new five-city LoRA and quantization runs, and a retry strategy "
                     "that responds to the actual validation failure. The "
                     "[documentation index](../docs/README.md) contains implementation "
                     "guides and runnable commands.")
    output = ROOT / "report" / "DineWise_Report.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
