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
        message = data.message.strip()

        # ---------- USER WORKSPACE ----------
        user_id = get_user_id(request)
        vector_path = f"storage/vector_db/{user_id}"

        # ---------- EMBED QUERY ----------
        query_vector = embed_texts([message])

        # ---------- RETRIEVE ----------
        results = search(
            query_vector,
            vector_path=vector_path,
            k=3
        )

        # ---------- NO RESULTS ----------
        if not results:
            return {
                "role": "assistant",
                "content": "No relevant documents found.",
                "sources": [],
                "confidence": 0.2
            }

        # ---------- BUILD CONTEXT ----------
        context = "\n\n".join([r["text"] for r in results])

        # ---------- GROQ ----------
        api_key = os.getenv("GROQ_API_KEY")
        model = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")

        if not api_key:
            raise Exception("GROQ_API_KEY missing")

        client = Groq(api_key=api_key)

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Answer ONLY using the provided document context. "
                        "If answer not present, say it is not mentioned."
                    ),
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

        answer = completion.choices[0].message.content.strip()

        # ---------- FORMAT SOURCES ----------
        formatted_sources = [
            {
                "document": r.get("document", "Unknown"),
                "text": r.get("text", ""),
                "score": float(r.get("score", 0))
            }
            for r in results
        ]

        # ---------- CONFIDENCE ----------
        avg_score = sum(s["score"] for s in formatted_sources) / len(formatted_sources)
        confidence = max(0.3, min(0.9, avg_score))

        # ---------- FINAL RESPONSE ----------
        return {
            "role": "assistant",
            "content": answer,
            "sources": formatted_sources,
            "confidence": confidence
        }

    except Exception as e:
        print("CHAT ERROR:", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Chat failed: {str(e)}"
        )
