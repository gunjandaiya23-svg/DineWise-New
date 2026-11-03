# Quantization and speed comparisons

Run `make efficiency` after installing tuning dependencies and preparing the adapter. The script compares base FP16, base INT8, base INT4, LoRA FP16 and LoRA INT4.

Quantization stores model weights at lower precision to reduce memory. It can change speed and outputs; lower precision does not automatically mean faster generation. LoRA is a separate adapter and can be combined with quantized base weights.

The benchmark uses a fixed Philadelphia question and retrieved context so model configurations receive comparable work. This is a controlled prompt benchmark, not a workload covering all cities or concurrent users. Read the script and generated JSON for the exact timing and memory fields before quoting results.

Use the same hardware, corpus, prompt, token budget and adapter when comparing runs. Record the model configuration alongside memory and generation throughput. A low training loss or smaller model memory does not establish better recommendations.

Historical efficiency tables remain available. They were not rerun automatically when the corpus expanded. Keep them separate from new measurements and describe their original conditions in the report.

[Documentation index](README.md)
