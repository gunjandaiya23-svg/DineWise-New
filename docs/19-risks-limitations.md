# What the system cannot guarantee

The dataset is static. Prices, ratings, status and reviews do not establish current restaurant conditions. The app has no booking or live availability integration.

Retrieval finds evidence; it does not prove truth. Summaries may contain upstream model errors, and a relevant chunk can omit important context. BGE truncates inputs beyond 512 tokens even when chunk targets are larger.

The constraint parser uses lexicons and patterns, so unusual phrasing can be missed. Dietary terms are not currently hard filters. Unknown attributes should not be interpreted as false or safe.

Answer validation checks a limited set of IDs, language patterns and price constraints. It is not a full factuality evaluator. Missing citations are soft failures, and an unchanged deterministic retry may repeat an invalid answer.

Evaluation uses a small fixed query set and automatically generated labels. Training examples use deterministic target answers. Splits group the primary restaurant, not every restaurant appearing in evidence. These choices limit conclusions about generalization and fine-tuning quality.

Historical training and efficiency results belong to the earlier corpus. Report their original conditions and do not imply that the expanded system has been retrained or fully benchmarked.

## Practical consequence for a user

If the answer says a restaurant is affordable, read the displayed `$` bucket as relative historical data. Confirm current prices with the restaurant. If a review mentions a vegetarian option, verify the current menu and preparation practices before relying on it for a dietary requirement. The assistant cannot establish allergy safety. If a generated answer sounds more certain than the retrieved excerpt, open the evidence panel and check its wording.

A validation pass means only that the implemented checks found no hard failure. It does not mean that every adjective, dish, or atmosphere claim was verified. Price checks in generated text currently inspect cited IDs; the names-only prompt usually omits them, so structured retrieval filtering is the main price safeguard. The app's catalogue-backed price/rating summary is a separate view of recorded fields, not a proof of the model's prose.

[Documentation index](README.md)
