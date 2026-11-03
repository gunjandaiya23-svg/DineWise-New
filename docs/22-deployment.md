# Deploy a free CPU demo

The public app runs on Streamlit Community Cloud. It performs retrieval locally on CPU and sends only the selected restaurant evidence and the visitor's question to Hugging Face Inference Providers for Qwen answer generation. Your Hugging Face inference credits fund those requests; the app reports an error when inference is unavailable or credits are exhausted. The free Streamlit instance may sleep when idle.

## 1. Upload the prepared assets

The app needs only the active C4 FAISS and BM25 indexes and `restaurants.parquet`. Raw reviews and the other research indexes are not uploaded. The uploader refuses an existing public dataset repository.

Create a Hugging Face token with permission to create and write a private dataset repository, then run from the project root:

```bash
export HF_TOKEN='your-token'
.venv/bin/python scripts/21_upload_deployment_assets.py YOUR_USERNAME/dinewise-assets
```

Keep the repository private. The deployment token needs read access to it and permission to use Inference Providers. Never commit a token or put it in the app UI.

## 2. Deploy the app

Push this code to GitHub. In Streamlit Community Cloud, create an app from that repository with entrypoint `app/streamlit_app.py` and Python 3.12. The root `requirements.txt` installs CPU PyTorch and the app package.

Set these root-level entries under the app's **Advanced settings → Secrets**:

```toml
HF_TOKEN = "your-token"
DINEWISE_ASSET_REPO = "YOUR_USERNAME/dinewise-assets"
DINEWISE_INFERENCE_MODE = "hf"
DINEWISE_HF_MODEL = "Qwen/Qwen2.5-72B-Instruct"
```

The Qwen model must be available for chat completion through your Hugging Face Inference Providers account. If its availability changes, set `DINEWISE_HF_MODEL` to another supported Qwen chat model. The app downloads missing private assets at startup and caches its retrieval stack until restart. After changing the active chunking configuration, upload the corresponding assets and reboot the app.

## 3. Check the live app

Ask for “Italian restaurants in Tampa under $$” and confirm that it returns a grounded answer and evidence. Ask an out-of-scope question and confirm it is refused without calling inference. If startup fails, inspect the Streamlit logs for missing assets, dependency issues, or Hugging Face access errors. Free hosting and inference quotas can change; check the current [Streamlit limits](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app) and [Hugging Face credit policy](https://huggingface.co/docs/inference-providers/pricing).
