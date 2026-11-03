# How prompts are assembled

The authoritative prompt definitions are in `src/dinewise/llm/prompts.py`. Scope checks and constraint extraction use rules; they do not send separate prompts to an LLM.

Generation receives a system message describing evidence-only answers, static data, citations and uncertainty. A user message contains the original question, up to five retrieved restaurant records, and the request for up to three recommendations.

Each record is shown as `Record N: <name>` with city/state, cuisine, an explainable price (`$ — Budget-friendly (dataset bucket 1 of 4)`), an explainable rating (`4.5 out of 5 stars (dataset value)`), and the retrieved text excerpt. The business ID is supplied on a line marked internal-only and never printed. The task asks for a numbered list of up to 3 connected paragraphs: bold name, cuisine/city, explained price and rating, then 1-2 grounded sentences on why it matches. It explicitly forbids `[RESTAURANT ...]` tags, business IDs, and bare values like `$, 4.5`. The prompt is passed through the Qwen tokenizer's chat template before generation.

The retry currently uses the same prompt and evidence with sampling disabled. It does not insert validation feedback or retrieve new records. Fallback responses are fixed Python strings. Training examples share the system prompt but use their own retrieved-record formatting and deterministic target answers.

[Documentation index](../README.md)
