# How Qwen turns evidence into an answer

The generator receives the original question and up to five restaurant records. Prompt construction adds each restaurant’s name, ID, location, cuisine, price bucket and retrieved excerpt.

The system prompt instructs Qwen to use only this evidence, avoid live claims, cite restaurant names or IDs and admit missing information. The task asks for up to three recommendations. The output is free-text Markdown; JSON generation is not implemented.

The app loads Qwen2.5-1.5B-Instruct lazily in FP16 with automatic device placement. It generates at most 256 new tokens with sampling disabled. A deterministic template mode exists for workflow tests and command-line evaluation, but the app uses Qwen.

Validation rejects IDs outside the retrieved candidates, flags live-information language, and checks cited restaurants against the maximum price constraint. Missing IDs and unmatched bold-formatted names are soft failures. Only hard failures block an answer.

These checks do not prove every sentence is supported. A response with no IDs can pass with a soft warning. The app currently displays the answer without exposing those diagnostics. See the limitations chapter before interpreting validation-pass rates as factual accuracy.

[Documentation index](README.md)
