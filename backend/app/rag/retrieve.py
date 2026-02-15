import faiss
import numpy as np
import os
import json

# embedding dimension (MiniLM)
DIMENSION = 384


# =====================================================
# PATH HELPERS (PER USER WORKSPACE)
# =====================================================
def get_index_path(vector_path: str):
    return os.path.join(vector_path, "index.faiss")


def get_meta_path(vector_path: str):
    return os.path.join(vector_path, "metadata.json")


# =====================================================
# INDEX HANDLING
# =====================================================
def load_index(vector_path: str):
    """
    Load FAISS index if exists.
    Otherwise create empty index.
    """

    os.makedirs(vector_path, exist_ok=True)
    index_path = get_index_path(vector_path)

    if os.path.exists(index_path):
        return faiss.read_index(index_path)

    return faiss.IndexFlatL2(DIMENSION)


def save_index(index, vector_path: str):
    os.makedirs(vector_path, exist_ok=True)
    faiss.write_index(index, get_index_path(vector_path))


# =====================================================
# METADATA HANDLING
# =====================================================
def load_metadata(vector_path: str):
    meta_path = get_meta_path(vector_path)

    if not os.path.exists(meta_path):
        return []

    with open(meta_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_metadata(data, vector_path: str):
    os.makedirs(vector_path, exist_ok=True)

    with open(get_meta_path(vector_path), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# =====================================================
# ADD EMBEDDINGS
# =====================================================
def add_embeddings(vectors, metadatas, vector_path: str):
    """
    Adds vectors + metadata into FAISS.
    """

    index = load_index(vector_path)
    metadata_store = load_metadata(vector_path)

    # cosine similarity normalization
    faiss.normalize_L2(vectors)

    index.add(vectors.astype("float32"))
    metadata_store.extend(metadatas)

    save_index(index, vector_path)
    save_metadata(metadata_store, vector_path)


# =====================================================
# SEARCH
# =====================================================
def search(query_vector, vector_path: str, k=3):

    index = load_or_create_index(vector_path)
    metadata_store = load_metadata(vector_path)

    if index.ntotal == 0:
        return []

    faiss.normalize_L2(query_vector)

    D, I = index.search(query_vector.astype("float32"), k)

    results = []

    for score, idx in zip(D[0], I[0]):
        if idx < len(metadata_store):
            item = metadata_store[idx].copy()
            item["score"] = float(score)
            results.append(item)

    return results

