from fastapi import APIRouter
import os
import faiss

from groq import Groq

router = APIRouter(prefix="/status", tags=["Status"])


@router.get("/")
def system_status():

    # -------------------
    # Backend health
    # -------------------
    backend_status = "ok"

    # -------------------
    # Vector DB health
    # -------------------
    try:
        index_path = "storage/vector_db/index.faiss"

        if os.path.exists(index_path):
            faiss.read_index(index_path)

        database_status = "ok"

    except Exception as e:
        print("DB HEALTH ERROR:", e)
        database_status = "unavailable"

    # -------------------
    # LLM REAL HEALTH CHECK
    # -------------------
    llm_status = "unavailable"

    try:
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")

        if GROQ_API_KEY:

            client = Groq(api_key=GROQ_API_KEY)

            # VERY SMALL TEST REQUEST
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "user", "content": "ping"}
                ],
                max_tokens=2,
                temperature=0,
            )

            if completion:
                llm_status = "ok"

    except Exception as e:
        print("LLM HEALTH ERROR:", e)
        llm_status = "unavailable"

    # -------------------
    # FINAL STATUS
    # -------------------
    return {
        "backend": backend_status,
        "database": database_status,
        "llm": llm_status
    }
