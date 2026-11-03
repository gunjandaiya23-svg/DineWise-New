# Current state and next work

The five-city corpus and C1–C4 FAISS/BM25 indexes are built. The app uses C4 hybrid retrieval and base Qwen generation. The simplified workflow, data processing, LoRA training commands and quantization comparisons are implemented.

The documentation describes current behavior. This list separates remaining work from implemented capabilities:

1. Review the silver relevance labels manually and record corrections separately from old runs. Success means the evaluation set has documented human judgments.
2. Regenerate fine-tuning examples for the expanded corpus, inspect split overlap among all retrieved restaurants, and train a new adapter. Preserve the old adapter for historical comparisons.
3. Rerun base/LoRA and quantization comparisons under the same five-city conditions. Store corpus, model, adapter and prompt provenance.
4. Strengthen answer validation and design a retry that can actually correct identified failures. The current deterministic retry reuses the same prompt and evidence.
5. Decide whether the app should offer LoRA inference and implement explicit dietary-evidence behavior. Neither capability is currently wired into the UI.

For each change, update the affected guide, run relevant checks and make a focused commit. Do not silently replace historical benchmark claims with new corpus counts.

## Acceptance for the next milestone

For the five-city fine-tuning comparison, first regenerate examples from the current C4 index and record the corpus and adapter path. Check for restaurant overlap across every retrieved evidence set, not only the query's primary restaurant. Train a new adapter and evaluate all four base/LoRA plus RAG/no-RAG modes on one fixed query suite. Report the exact labels and model settings. A successful run does not require LoRA to win; it requires a reproducible, honestly interpreted comparison.

For app quality, test a supported query in each city, an unsupported city, a live-data refusal, an unknown price and an answer that fails validation. The current workflow can return a fallback; a useful future retry should change something in response to the failure reason rather than submitting the same deterministic prompt again.

[Documentation index](README.md)
