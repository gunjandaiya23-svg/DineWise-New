# How prompts are assembled

The authoritative prompt definitions are in `src/dinewise/llm/prompts.py`. Scope checks and constraint extraction use rules; they do not send separate prompts to an LLM.

Generation receives a system message describing evidence-only answers, static data, citations and uncertainty. A user message contains the original question, up to five retrieved restaurant records, and the request for up to three recommendations.

Each record includes ID, name, city/state, cuisine, price bucket and the retrieved text excerpt. The prompt is passed through the Qwen tokenizer's chat template before generation.

The retry currently uses the same prompt and evidence with sampling disabled. It does not insert validation feedback or retrieve new records. Fallback responses are fixed Python strings. Training examples share the system prompt but use their own retrieved-record formatting and deterministic target answers.

[Documentation index](../README.md)
