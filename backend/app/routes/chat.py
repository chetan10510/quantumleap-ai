from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
import os
from groq import Groq

from app.rag.embed import embed_texts
from app.rag.retrieve import search
from app.utils.user import get_user_id

router = APIRouter(prefix="/chat", tags=["Chat"])


# ================= REQUEST MODEL =================
class ChatRequest(BaseModel):
    message: str


# ================= CHAT ENDPOINT =================
@router.post("/")
async def chat(data: ChatRequest, request: Request):

    try:
        message = data.message.strip()

        # ---------- USER WORKSPACE ----------
        user_id = get_user_id(request)
        vector_path = f"storage/vector_db/{user_id}"

        # ---------- EMBED QUERY ----------
        query_vector = embed_texts([message])

        # ---------- RETRIEVE DOCUMENT CHUNKS ----------
        results = search(
            query_vector,
            vector_path=vector_path,
            k=5   # IMPORTANT: more context improves grounding
        )

        if not results:
            return {
                "answer": "No relevant documents found.",
                "sources": [],
                "confidence": 0.2
            }

        # ---------- BUILD CONTEXT ----------
        context_blocks = []
        for i, r in enumerate(results):
            context_blocks.append(
                f"[Source {i+1}]\n{r['text']}"
            )

        context = "\n\n".join(context_blocks)

        # ---------- ENV ----------
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")

        if not GROQ_API_KEY:
            raise Exception("GROQ_API_KEY missing")

        client = Groq(api_key=GROQ_API_KEY)

        # ================= BETTER RAG PROMPT =================
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": """
You are a document analysis assistant.

Rules:
- Answer using ONLY the provided document excerpts.
- Extract information directly from the text.
- If information is partially present, infer carefully.
- NEVER say "I cannot find" unless context truly lacks information.
- Give concise factual answers.
"""
                },
                {
                    "role": "user",
                    "content": f"""
DOCUMENT EXCERPTS:
{context}

QUESTION:
{message}

Answer using the excerpts above.
"""
                }
            ],
        )

        answer = completion.choices[0].message.content.strip()

        # ---------- SIMPLE CONFIDENCE HEURISTIC ----------
        confidence = min(0.9, 0.4 + (len(results) * 0.1))

        return {
            "answer": answer,
            "sources": results,
            "confidence": confidence
        }

    except Exception as e:
        print("CHAT ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=f"Chat failed: {str(e)}"
        )
