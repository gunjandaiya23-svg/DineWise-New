# How Qwen turns evidence into an answer

The generator receives the original question and up to five restaurant records. Prompt construction adds each restaurant’s name, ID, location, cuisine, price bucket and retrieved excerpt.

The system prompt instructs Qwen to use only this evidence, avoid live claims, use bold restaurant names and admit missing information. The task asks for up to three recommendations. The output is free-text Markdown; JSON generation is not implemented.

The app loads Qwen2.5-1.5B-Instruct lazily in FP16 with automatic device placement. It generates at most 768 new tokens with sampling disabled. A deterministic template mode exists for workflow tests and command-line evaluation, but the app uses Qwen.

Validation rejects IDs outside the retrieved candidates, flags live-information language, and checks cited restaurants against the maximum price constraint. Missing IDs and unmatched bold-formatted names are soft failures. Because the prompt asks the model to omit IDs, the text-level price check normally has no cited ID to inspect; the structured price filter still restricts retrieved restaurants before generation. Only hard failures block an answer.

These checks do not prove every sentence is supported. A response with no IDs can pass because the prompt now requests names; the missing-ID check remains a soft warning. The app displays the answer and expandable evidence without exposing validation diagnostics. See the limitations chapter before interpreting validation-pass rates as factual accuracy.

## What the model sees and what the UI shows

A model input contains the user's exact question and up to five selected records. Each record identifies its business, city, cuisine, recorded price bucket, dataset rating and evidence excerpt. Qwen is asked for up to three concise recommendations. The current generation limit is 768 new tokens, and sampling is disabled; the model can still repeat weak evidence or omit a requested detail.

The prompt includes business IDs internally but asks Qwen to use names only. The validator still flags unknown IDs if the model leaks them and rejects leaked `[RESTAURANT ...]` markers. The chat UI strips leaked IDs and shows a separate price/rating table for names it recognizes in the answer. It keeps IDs in expandable source records. That table reads retrieved metadata, so it can show “Unknown” when price is missing even if the model uses vague price language. Hard validation failures trigger one regeneration attempt, but the same prompt and deterministic settings make a repeated answer possible.

[Documentation index](README.md)
