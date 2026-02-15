from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

_model = None


def get_model():
    global _model

    if _model is None:
        print("Loading embedding model...")
        _model = SentenceTransformer(
            "all-MiniLM-L6-v2",
            device="cpu"
        )
        print("Model ready")

    return _model


def embed_texts(texts: List[str]) -> np.ndarray:
    """
    Memory-safe embedding generation.
    Processes chunks in SMALL batches.
    """

    model = get_model()

    all_embeddings = []

    BATCH_SIZE = 8  

    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i:i + BATCH_SIZE]

        emb = model.encode(
            batch,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        all_embeddings.append(emb)

    embeddings = np.vstack(all_embeddings)

    return embeddings.astype("float32")
