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

## Compare training with retrieval

A LoRA adapter modifies a small set of model weights while the base Qwen weights remain fixed. The project uses 4-bit loading during training to fit the model on available GPU memory. The 400 default examples teach answer format, evidence use and refusals from retrieved records; they are not a new source of restaurant facts. When evaluating, use the same query suite for `base_no_rag`, `base_rag`, `lora_no_rag`, and `lora_rag` so the effect of retrieval and the adapter can be compared separately.

Rebuilding the restaurant corpus does not retrain an adapter. The saved adapter and its historical results should retain their original training-data provenance. A new five-city fine-tuning claim needs fresh examples, split inspection, training, and evaluation. The current app still loads base Qwen, so its answers should not be called LoRA outputs.

[Documentation index](README.md)
