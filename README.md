# 🍽️ DineWise

**DineWise** is an AI-powered restaurant recommendation system that helps users discover restaurants based on their preferences.

Users can search for restaurants by city, cuisine, price range, and other attributes. The application uses restaurant and review data to generate personalized recommendations with the help of a Qwen language model.

## ✨ Features

- Search restaurants based on city and cuisine.
- Filter restaurants by price range and preferences.
- AI-generated recommendations using Qwen.
- Hybrid search using FAISS (dense retrieval) and BM25.
- Combines search results using Reciprocal Rank Fusion (RRF).
- Provides restaurant ratings, price categories, and review evidence.
- Displays supporting restaurant records and review excerpts.

## 🌎 Supported Cities

DineWise currently supports five cities:

- Philadelphia
- Indianapolis
- Tampa
- New Orleans
- Tucson

## 🛠️ Tech Stack

- **Python** – Core development
- **Streamlit** – User interface
- **Qwen** – AI recommendation generation
- **FAISS** – Dense vector search
- **BM25** – Keyword-based search
- **BGE** – Text embeddings
- **RAG** – Retrieval-Augmented Generation

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd DineWise
```

### 2. Set up the environment

```bash
make setup
```

### 3. Check the environment

```bash
make check
```

### 4. Download the dataset

```bash
make download
```

### 5. Prepare the data and build indexes

```bash
make rebuild
```

### 6. Run the application

```bash
make app
```

Open your browser and visit:

```text
http://localhost:8501
```

**Example query:**

```text
Italian restaurants in Tampa under $$
```

The first request may take longer because the Qwen model needs to load.

## 🔍 How It Works

DineWise follows a Retrieval-Augmented Generation (RAG) pipeline:

1. **User Query:** The user enters restaurant preferences.
2. **Query Processing:** The system identifies the city, cuisine, price range, and other filters.
3. **Restaurant Filtering:** Relevant restaurants are selected from the dataset.
4. **Hybrid Retrieval:** FAISS and BM25 retrieve relevant restaurant and review information.
5. **Result Fusion:** Reciprocal Rank Fusion combines the search results.
6. **AI Generation:** Qwen generates recommendations using the retrieved evidence.
7. **Validation:** The generated response is checked before being displayed.

## 📊 Dataset

The project uses the [Yelp Multimodal Recommendation Dataset](https://huggingface.co/datasets/wzehui/Yelp-Multimodal-Recommendation).

The prepared dataset contains:

- **5,968 restaurants**
- **382,253 reviews**
- **5 supported cities**

The dataset is used for educational and non-commercial research.

## 📁 Project Structure

```text
DineWise/
│
├── app/             # Streamlit application
├── src/
│   └── dinewise/    # Core project implementation
├── scripts/         # Data processing and evaluation scripts
├── config/          # Project configurations
├── data/            # Dataset and processed files
├── results/         # Experiment results
├── docs/            # Project documentation
├── report/          # Technical report
│
├── Makefile
└── README.md
```

## 🧪 Testing and Evaluation

Run the following commands for testing and experiments:

```bash
make test
make lint
make retrieval-eval
make model-eval
make report
```

## ⚠️ Limitations

- Restaurant recommendations are based on a static dataset.
- Live restaurant availability and table booking are not supported.
- Real-time prices, menus, and opening hours are not available.
- Recommendation quality depends on the retrieved restaurant and review data.

## 📚 Documentation

For detailed information about the architecture, data processing, retrieval methods, experiments, and deployment, see the [Documentation](docs/README.md).

## 📄 License

The code license has not yet been selected.

The dataset is derived from Yelp data and is subject to its original source terms.

---

**DineWise – Smarter Restaurant Discovery with AI.**
