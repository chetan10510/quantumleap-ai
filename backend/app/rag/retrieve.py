import faiss
import numpy as np
import os
import json


# =====================================================
# PATH HELPERS (PER USER)
# =====================================================

def get_index_path(vector_path: str):
    return os.path.join(vector_path, "index.faiss")


def get_metadata_path(vector_path: str):
    return os.path.join(vector_path, "metadata.json")


# =====================================================
# INDEX LOAD / SAVE
# =====================================================

def load_index(vector_path: str):
    index_file = get_index_path(vector_path)

    if os.path.exists(index_file):
        return faiss.read_index(index_file)

    # empty fallback index
    dimension = 384
    return faiss.IndexFlatL2(dimension)


def save_index(index, vector_path: str):
    os.makedirs(vector_path, exist_ok=True)
    faiss.write_index(index, get_index_path(vector_path))


# =====================================================
# METADATA LOAD / SAVE
# =====================================================

def load_metadata(vector_path: str):
    meta_file = get_metadata_path(vector_path)

    if not os.path.exists(meta_file):
        return []

    with open(meta_file, "r") as f:
        return json.load(f)


def save_metadata(data, vector_path: str):
    os.makedirs(vector_path, exist_ok=True)

    with open(get_metadata_path(vector_path), "w") as f:
        json.dump(data, f, indent=2)


# =====================================================
# ADD EMBEDDINGS
# =====================================================

def add_embeddings(vectors, metadatas, vector_path: str):

    index = load_index(vector_path)
    metadata_store = load_metadata(vector_path)

    faiss.normalize_L2(vectors)

    index.add(vectors.astype("float32"))
    metadata_store.extend(metadatas)

    save_index(index, vector_path)
    save_metadata(metadata_store, vector_path)


# =====================================================
# SEARCH
# =====================================================

def search(query_vector, vector_path: str, k=3):

    index = load_index(vector_path)
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
