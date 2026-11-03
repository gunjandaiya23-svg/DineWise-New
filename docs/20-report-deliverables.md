# Build and explain the report

Run `make report` to generate `report/DineWise_Report.md`. The generator reads the prepared corpus audit and links the available result tables. It does not rerun experiments.

A useful report explains the problem, follows raw data through retrieval and generation, describes controlled comparisons, then discusses results and limitations. Define metrics before quoting scores. Separate retrieval relevance, generated-answer validation and runtime efficiency.

For each result, record corpus, query suite, label source, chunk configuration, model and adapter where applicable. Use timestamped `results/runs/` artifacts as evidence; latest tables are convenient pointers that later runs can overwrite.

Keep old pilot measurements separate from five-city results. State that labels are silver and that trained adapters and quantization measurements were not automatically refreshed by rebuilding indexes.

The deliverables are runnable source, an app launch guide, reproducible build and experiment commands, measured result artifacts and a report whose claims match those artifacts. The model weights and raw dataset are local artifacts, not normal git deliverables.

## Minimum evidence for a claim

For a sentence such as “C4 led the chunking comparison,” cite the five-city C1–C4 run, state that the labels are silver, identify hybrid nDCG@5 as the selection metric, and include the four scores. For “hybrid retrieval is better,” name the metric: it leads strict Success@5 in the current run, while BM25 has slightly higher nDCG@5. A report should not present one metric as a universal winner.

The generated report links result artifacts and explains their scope. A reader should be able to find the exact timestamped run behind a number and distinguish old pilot results from current five-city experiments. The adapter and quantization tables remain historical until a new training/benchmark run records the expanded corpus and model configuration.

[Documentation index](README.md)
