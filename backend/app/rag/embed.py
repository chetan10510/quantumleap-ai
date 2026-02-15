from sentence_transformers import SentenceTransformer
import numpy as np

# Global model holder
_model = None


def get_model():
    """
    Lazy-load embedding model.
    Loads ONLY when first query happens.
    Prevents Render startup OOM crash.
    """
    global _model

    if _model is None:
        print("Loading embedding model...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")

    return _model


def embed_texts(texts: list[str]) -> np.ndarray:
    model = get_model()
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )
    return embeddings.astype("float32")
