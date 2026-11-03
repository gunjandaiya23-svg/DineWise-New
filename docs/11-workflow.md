# Query workflow

The app calls `run_query(graph, query)` in `src/dinewise/graph/workflow.py`. Despite the historical `graph` function and folder names, this is a plain Python workflow. It passes a state dictionary between steps; each step returns fields that are merged into that dictionary.

## One query, step by step

For `Italian restaurants in Tampa under $$`, the workflow does the following:

1. **Classify.** Rule-based scope checks look for requests for booking, live availability, wait times, or current prices. If the request is supported, the constraint parser identifies `city=Tampa`, `cuisines=[Italian]`, and `max_price_bucket=2`.
2. **Retrieve.** Structured fields first determine eligible restaurant IDs. BGE/FAISS and BM25 rank evidence chunks, Reciprocal Rank Fusion combines their positions, and the pipeline collapses chunks to at most five distinct restaurants.
3. **Generate.** Qwen receives the original question and retrieved excerpts. The prompt asks for up to three short recommendations with bold names, price buckets, ratings, and a reason supported by the records. IDs are supplied internally but should not appear in the answer.
4. **Review.** The validator checks for unknown cited IDs, forbidden live claims, leaked internal markers, and price violations among cited restaurants. Missing IDs and some name mismatches are soft warnings. With names-only answers, price compliance primarily comes from the structured retrieval filter because the text validator requires a cited ID for that check.
5. **Finish or fall back.** A hard failure leads to one regeneration attempt. The retry keeps the same constraints, evidence, prompt, and deterministic generation settings, so it may repeat the same answer. A second failure produces a fixed explanation.

Unknown cities and unsupported amenities are refused before generation. If filtering or retrieval produces no hits, the workflow returns an explanation instead of calling Qwen. The state contains `query`, `constraints`, `hits`, `answer`, `validation`, `retry_count`, flags, and a diagnostic trace; see [the output reference](appendices/b-output-schema.md).

## What the chat interface does

Streamlit shows a warm light chat view. The sidebar lists the five supported cities and explains `$` through `$$$$` as relative price buckets. It also shows a reminder about static values and dietary uncertainty. The chat stores messages and their result state for the current browser session. Each submitted question is searched independently: earlier chat messages are displayed but are not sent to Qwen as context.

The main answer hides business IDs for readability. The workflow still uses IDs to connect evidence to catalogue records and detect leaked IDs. A catalogue-backed summary shows price buckets and dataset ratings for restaurants named in the answer. Expand the restaurant records or evidence excerpts to inspect IDs and source text. **Clear conversation** removes the browser session's displayed history; it does not change the indexes.

The UI catches request errors and shows a short message while recording the details in the server log. It does not expose raw validation diagnostics. The current app loads the base Qwen model; LoRA adapters are used by separate research scripts.
