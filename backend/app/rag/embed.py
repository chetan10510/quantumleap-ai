from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

# --------------------------------------------------
# Global model holder (lazy loaded)
# --------------------------------------------------
_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    """
    Lazy-load embedding model.

    ✔ Loads ONLY when first embedding request happens
    ✔ Prevents Render startup OOM
    ✔ Faster deployment boot time
    """
    global _model

    if _model is None:
        print("🔄 Loading embedding model (first request only)...")

        _model = SentenceTransformer(
            "all-MiniLM-L6-v2",
            device="cpu"   # IMPORTANT for Render (no GPU)
        )

        print("✅ Embedding model loaded.")

    return _model


# --------------------------------------------------
# Embedding function
# --------------------------------------------------
def embed_texts(texts: List[str]) -> np.ndarray:
    """
    Generate normalized embeddings for a list of texts.
    Returns float32 numpy array (FAISS compatible).
    """

    model = get_model()

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    return embeddings.astype("float32")
