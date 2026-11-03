# DineWise documentation

Start with [Run the app](03-environment.md), then [Architecture](02-architecture.md). Read the remaining chapters when you need that part of the pipeline. Each guide describes current code; planned work is listed explicitly in the roadmap.

| Guide | Topic |
|---|---|
| [What DineWise does](01-overview.md) | Chapter 01 |
| [Architecture](02-architecture.md) | Chapter 02 |
| [Run the app and prepare the environment](03-environment.md) | Chapter 03 |
| [The dataset and city coverage](04-dataset.md) | Chapter 04 |
| [How raw records become usable tables](05-data-engineering.md) | Chapter 05 |
| [Evidence profiles](06-documents.md) | Chapter 06 |
| [How profiles become searchable chunks](07-chunking.md) | Chapter 07 |
| [Two indexes over the same evidence](08-embeddings-indexing.md) | Chapter 08 |
| [How hybrid retrieval chooses restaurants](09-retrieval.md) | Chapter 09 |
| [How Qwen turns evidence into an answer](10-generation.md) | Chapter 10 |
| [Query workflow](11-workflow.md) | Chapter 11 |
| [Preferences and current boundaries](12-personalization.md) | Chapter 12 |
| [LoRA training and its role](13-finetuning.md) | Chapter 13 |
| [Quantization and speed comparisons](14-efficiency.md) | Chapter 14 |
| [How quality is measured](15-evaluation.md) | Chapter 15 |
| [Run comparisons in a useful order](16-experiments.md) | Chapter 16 |
| [Where the code and artifacts live](17-engineering.md) | Chapter 17 |
| [Current state and next work](18-roadmap.md) | Chapter 18 |
| [What the system cannot guarantee](19-risks-limitations.md) | Chapter 19 |
| [Build and explain the report](20-report-deliverables.md) | Chapter 20 |
| [Design decisions and source references](21-decisions-references.md) | Chapter 21 |

## Choose a reading path

- To **run the app**, read chapters 03, 02 and 11.
- To **follow the data**, read chapters 04–09 in order.
- To **understand an answer**, read chapters 10, 11 and appendix B.
- To **evaluate RAG and fine-tuning**, read chapters 13–16, then the technical report.
- To **change the implementation**, read chapters 17–19 and the decision log.

Each chapter begins with the behavior it explains and points to its inputs and outputs. Result tables are measurements, not implementation instructions.

## References

Appendices describe metadata, workflow outputs, prompts, evaluation queries, result artifacts and terminology.

- [Evidence metadata](appendices/a-metadata-schema.md)
- [What the workflow returns](appendices/b-output-schema.md)
- [How prompts are assembled](appendices/c-prompts.md)
- [Fixed evaluation queries](appendices/d-test-queries.md)
- [Read result artifacts correctly](appendices/e-result-tables.md)
- [Terms used in the guides](appendices/f-glossary.md)

## How to maintain these guides

Explain purpose first, then inputs, processing, outputs and runnable commands. Define technical terms where they first appear. Use code as the source of truth and result manifests for measured claims. Keep future work separate from implemented behavior. Update the relevant chapter and decision log when behavior changes.
