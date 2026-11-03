# What DineWise does

DineWise recommends restaurants from a static dataset. A user describes what they want; the system finds relevant restaurant evidence and asks Qwen to write an answer from it.

The current corpus contains 5,968 restaurants and 382,253 reviews across Philadelphia, Indianapolis, Tampa, New Orleans, and Tucson. These counts describe the prepared corpus, not the entire source dataset.

The project studies three questions: which retrieval approach finds better evidence, how chunk size affects retrieval, and whether LoRA improves grounded responses. Quantization experiments measure memory and generation speed.

The app uses base Qwen with hybrid RAG. Training adapters and running comparisons are separate operations. It cannot book tables or provide live prices and availability. Start with the architecture chapter, then follow the data through chapters 04–11.

[Documentation index](README.md)
