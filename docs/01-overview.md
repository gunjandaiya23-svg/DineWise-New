# What DineWise does

DineWise recommends restaurants from a static dataset. A user describes what they want; the system finds relevant restaurant evidence and asks Qwen to write an answer from it.

The current corpus contains 5,968 restaurants and 382,253 reviews across Philadelphia, Indianapolis, Tampa, New Orleans, and Tucson. These counts describe the prepared corpus, not the entire source dataset.

The project studies three questions: which retrieval approach finds better evidence, how chunk size affects retrieval, and whether LoRA improves grounded responses. Quantization experiments measure memory and generation speed.

The app uses base Qwen with hybrid RAG. Training adapters and running comparisons are separate operations. It cannot book tables or provide live prices and availability. Start with the architecture chapter, then follow the data through chapters 04–11.

## Example and boundaries

Ask “Italian restaurants in Tampa under $$.” The parser uses Tampa as a city filter and interprets `$$` as maximum price bucket 2. Two search methods rank text about eligible restaurants; Qwen writes a response from the selected excerpts. The UI displays the answer and a separate catalogue-backed price and rating summary. It keeps source details in expandable panels.

This is a research assistant, not a live restaurant directory. A recommendation can be relevant to the historical dataset while the business's current menu, hours, price, or quality have changed. A request for a booking or current price is refused because no live service supplies that information. The dietary evidence is descriptive, not a safety check.

[Documentation index](README.md)
