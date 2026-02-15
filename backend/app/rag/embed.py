from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

_model = None


def get_model():
    """
    Lazy load embedding model ONLY when first used.
    Prevents Railway startup crash.
    """
    global _model

    if _model is None:
        print("Loading embedding model...")

        from sentence_transformers import SentenceTransformer

        _model = SentenceTransformer(
            "all-MiniLM-L6-v2",
            device="cpu"
        )

        print("Embedding model ready.")

    return _model


def embed_texts(texts: List[str]) -> np.ndarray:
    model = get_model()

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    return embeddings.astype("float32")
