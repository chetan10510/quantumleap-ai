from fastapi import APIRouter
import os
import faiss

router = APIRouter(prefix="/status", tags=["Status"])


@router.get("/")
def system_status():

    # -------------------
    # Backend health
    # -------------------
    backend_status = "ok"

    # -------------------
    # Database (FAISS) health
    # -------------------
    try:
        index_path = "storage/vector_db/index.faiss"
        if os.path.exists(index_path):
            faiss.read_index(index_path)
        database_status = "ok"
    except Exception:
        database_status = "unavailable"

    # -------------------
    # LLM connection check
    # -------------------
    try:
        # simple environment check
        llm_key = os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY")

        if llm_key:
            llm_status = "ok"
        else:
            llm_status = "unavailable"

    except Exception:
        llm_status = "unavailable"

    return {
        "backend": backend_status,
        "database": database_status,
        "llm": llm_status
    }
