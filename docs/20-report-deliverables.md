# Build and explain the report

Run `make report` to generate `report/DineWise_Report.md`. The generator reads the prepared corpus audit and links the available result tables. It does not rerun experiments.

A useful report explains the problem, follows raw data through retrieval and generation, describes controlled comparisons, then discusses results and limitations. Define metrics before quoting scores. Separate retrieval relevance, generated-answer validation and runtime efficiency.

For each result, record corpus, query suite, label source, chunk configuration, model and adapter where applicable. Use timestamped `results/runs/` artifacts as evidence; latest tables are convenient pointers that later runs can overwrite.

Keep old pilot measurements separate from five-city results. State that labels are silver and that trained adapters and quantization measurements were not automatically refreshed by rebuilding indexes.

The deliverables are runnable source, an app launch guide, reproducible build and experiment commands, measured result artifacts and a report whose claims match those artifacts. The model weights and raw dataset are local artifacts, not normal git deliverables.

[Documentation index](README.md)
