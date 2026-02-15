from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

from app.rag.embed import embed_texts
from app.rag.retrieve import search
from app.rag.generate import generate_answer
from app.utils.user import get_user_id

router = APIRouter(prefix="/chat", tags=["Chat"])


# ---------------- REQUEST MODEL ----------------
class ChatRequest(BaseModel):
    message: str


# ---------------- CHAT ENDPOINT ----------------
@router.post("/")
async def chat(data: ChatRequest, request: Request):

    if not data.message.strip():
        raise HTTPException(status_code=400, detail="Empty message")

    # ✅ identify user workspace
    user_id = get_user_id(request)
    vector_path = f"storage/vector_db/{user_id}"

    # ---------- EMBED QUERY ----------
    query_vector = embed_texts([data.message])

    # ✅ FIX: pass vector_path
    results = search(
        query_vector,
        k=3,
        vector_path=vector_path
    )

    if not results:
        return {
            "answer": "No relevant documents found.",
            "sources": []
        }

    # ---------- GENERATE ANSWER ----------
    answer = generate_answer(data.message, results)

    return {
        "answer": answer,
        "sources": results
    }
