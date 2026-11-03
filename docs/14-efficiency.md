# Quantization and speed comparisons

Run `make efficiency` after installing tuning dependencies and preparing the adapter. The script compares base FP16, base INT8, base INT4, LoRA FP16 and LoRA INT4.

Quantization stores model weights at lower precision to reduce memory. It can change speed and outputs; lower precision does not automatically mean faster generation. LoRA is a separate adapter and can be combined with quantized base weights.

The benchmark uses a fixed Philadelphia question and retrieved context so model configurations receive comparable work. This is a controlled prompt benchmark, not a workload covering all cities or concurrent users. Read the script and generated JSON for the exact timing and memory fields before quoting results.

Use the same hardware, corpus, prompt, token budget and adapter when comparing runs. Record the model configuration alongside memory and generation throughput. A low training loss or smaller model memory does not establish better recommendations.

Historical efficiency tables remain available. They were not rerun automatically when the corpus expanded. Keep them separate from new measurements and describe their original conditions in the report.

## Interpret the measurements

The benchmark's table distinguishes model load time, time until the first output token, time per later token, tokens per second, peak GPU memory and approximate loaded weight size. These measure different costs. A model may load quickly but decode slowly, or reduce memory while doing more work per token. Compare one column at a time under the same device and prompt.

The old pilot measurement, for example, recorded about 43 tokens/s for base FP16 and about 13 tokens/s for INT8 on that hardware; this is an observation from that run, not a general property of INT8. The LoRA adapter can add latency even when it is small. The fixed Philadelphia prompt makes the modes comparable but does not measure workload variation across all five cities.

[Documentation index](README.md)
