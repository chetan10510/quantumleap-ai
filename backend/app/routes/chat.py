from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
import os

from groq import Groq

from app.rag.embed import embed_texts
from app.rag.retrieve import search
from app.utils.user import get_user_id

router = APIRouter(prefix="/chat", tags=["Chat"])


# ---------------- REQUEST MODEL ----------------
class ChatRequest(BaseModel):
    message: str


# ---------------- CHAT ENDPOINT ----------------
@router.post("/")
async def chat(data: ChatRequest, request: Request):

    try:
        message = data.message

        # ---------- USER WORKSPACE ----------
        user_id = get_user_id(request)
        vector_path = f"storage/vector_db/{user_id}"

        # ---------- EMBED QUERY ----------
        query_vector = embed_texts([message])

        # ---------- RETRIEVE CONTEXT ----------
        results = search(
            query_vector,
            vector_path=vector_path,
            k=3
        )

        if not results:
            return {
                "answer": "No relevant documents found.",
                "sources": [],
                "confidence": "Low"
            }

        context = "\n\n".join([r["text"] for r in results])

        # ---------- LOAD ENV (Railway-safe) ----------
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")

        if not GROQ_API_KEY:
            raise Exception("GROQ_API_KEY missing in environment")

        # ---------- GROQ CLIENT ----------
        client = Groq(api_key=GROQ_API_KEY)

        # ---------- LLM CALL ----------
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "Answer ONLY using provided document context."
                },
                {
                    "role": "user",
                    "content": f"""
Context:
{context}

Question:
{message}
"""
                }
            ],
            temperature=0.2,
        )

        answer = completion.choices[0].message.content

        # ---------- FORMAT SOURCES FOR FRONTEND ----------
        sources = []

        for r in results:
            sources.append({
                "document": r.get("document", "Unknown"),
                "text": r.get("text", ""),   #  evidence snippet
                "score": float(r.get("score", 0))
            })

        # ---------- RESPONSE (FRONTEND FORMAT) ----------
        return {
            "role": "assistant",
            "content": answer,        #  frontend expects content
            "sources": sources,
            "confidence": 0.55        # numeric → enables label logic
        }


    except Exception as e:
        #  CRITICAL: print REAL ERROR to Railway logs
        print("CHAT ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=f"Chat failed: {str(e)}"
        )
