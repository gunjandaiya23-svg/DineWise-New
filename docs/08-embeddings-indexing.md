# Two indexes over the same evidence

`make index` builds the active FAISS index after chunking. `make bm25` builds its lexical counterpart. `make rebuild` builds both for C1–C4.

BGE-small-en-v1.5 converts each chunk into a 384-dimensional vector. Vectors are normalized, allowing FAISS inner-product scores to act as cosine similarity. The index is `IndexFlatIP`, an exact search over the stored vectors. No vector database service is needed.

Dense artifacts live under `data/indexes/faiss/C*/`: `index.faiss`, `chunks.parquet`, and `index_meta.json`. FAISS row positions map to rows in the saved chunk table. Keep these files together when rebuilding or copying an index.

BM25 tokenizes words, lowercases them, removes a fixed stopword list and builds a lexical index under `data/indexes/bm25/C*/`. It finds word matches rather than semantic similarity.

At query time, BGE embeds the question with a retrieval prefix; FAISS compares that vector with chunk vectors. BM25 independently scores the query words. Both rankings refer to the same chunk IDs. Model name, sequence limit, corpus and chunk configuration must remain consistent between building and querying.

[Documentation index](README.md)
