# LoRA training and its role

RAG supplies restaurant facts at query time. LoRA trains a small adapter to change response behavior. The app currently uses base Qwen with RAG; it does not load the trained adapter.

Run these commands after building the corpus and installing the tuning dependencies:

```bash
make lora-data
make lora-train
make model-eval
```

The data builder retrieves restaurant evidence and creates instruction examples with deterministic target answers. It includes supported recommendation tasks and scope refusals. It defaults to 400 examples. Train/validation/test groups are separated by the primary restaurant used to construct a query; this does not guarantee that other retrieved restaurants never cross splits.

Training uses 4-bit NF4 QLoRA with double quantization and bfloat16 computation. LoRA rank is 8, alpha 16 and dropout 0.05, targeting attention and feed-forward projection layers. Defaults are two epochs, batch size 1, accumulation 4, learning rate 0.0002 and maximum sequence length 1024.

Examples live in `data/tuning/`; the default adapter output is `models/lora-qwen`. Model evaluation compares base without RAG, base with RAG, LoRA without RAG and LoRA with RAG. Existing weights were trained before city expansion; rebuild examples and retrain before claiming a five-city fine-tuning result.

[Documentation index](README.md)
