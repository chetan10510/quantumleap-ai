import faiss
import numpy as np
import os
import json

VECTOR_PATH = "storage/vector_db/index.faiss"
META_PATH = "storage/vector_db/metadata.json"

dimension = 384  # embedding size for MiniLM


def load_or_create_index():
    if os.path.exists(VECTOR_PATH):
        return faiss.read_index(VECTOR_PATH)

    return faiss.IndexFlatL2(dimension)


def save_index(index):
    faiss.write_index(index, VECTOR_PATH)


def load_metadata():
    if not os.path.exists(META_PATH):
        return []

    with open(META_PATH, "r") as f:
        return json.load(f)


def save_metadata(data):
    with open(META_PATH, "w") as f:
        json.dump(data, f, indent=2)


def add_embeddings(vectors, metadatas):
    index = load_or_create_index()
    metadata_store = load_metadata()

    faiss.normalize_L2(vectors)

    index.add(vectors.astype("float32"))
    metadata_store.extend(metadatas)

    save_index(index)
    save_metadata(metadata_store)



def search(query_vector, k=3):
    index = load_or_create_index()
    metadata_store = load_metadata()

    if index.ntotal == 0:
        return []

    # normalize for cosine similarity
    faiss.normalize_L2(query_vector)

    D, I = index.search(query_vector.astype("float32"), k)

    results = []

    for score, idx in zip(D[0], I[0]):
        if idx < len(metadata_store):
            item = metadata_store[idx].copy()
            item["score"] = float(score)
            results.append(item)

    return results

