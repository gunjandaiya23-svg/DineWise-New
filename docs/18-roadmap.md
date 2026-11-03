# Current state and next work

The five-city corpus and C1–C4 FAISS/BM25 indexes are built. The app uses C4 hybrid retrieval and base Qwen generation. The simplified workflow, data processing, LoRA training commands and quantization comparisons are implemented.

The documentation describes current behavior. This list separates remaining work from implemented capabilities:

1. Review the silver relevance labels manually and record corrections separately from old runs. Success means the evaluation set has documented human judgments.
2. Regenerate fine-tuning examples for the expanded corpus, inspect split overlap among all retrieved restaurants, and train a new adapter. Preserve the old adapter for historical comparisons.
3. Rerun base/LoRA and quantization comparisons under the same five-city conditions. Store corpus, model, adapter and prompt provenance.
4. Strengthen answer validation and design a retry that can actually correct identified failures. The current deterministic retry reuses the same prompt and evidence.
5. Decide whether the app should offer LoRA inference and implement explicit dietary-evidence behavior. Neither capability is currently wired into the UI.

For each change, update the affected guide, run relevant checks and make a focused commit. Do not silently replace historical benchmark claims with new corpus counts.

[Documentation index](README.md)
