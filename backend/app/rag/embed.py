from sentence_transformers import SentenceTransformer
import numpy as np

# load model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts):
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=False
    )

    return embeddings.astype("float32")
