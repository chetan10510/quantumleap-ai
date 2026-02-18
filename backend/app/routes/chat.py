import os
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from groq import Groq

from app.rag.embed import embed_texts
from app.rag.retrieve import search
from app.utils.user import get_user_id
from app.core.logger import get_logger
from app.core.guardrails import validate_user_message

logger = get_logger("chat")

router = APIRouter(prefix="/chat", tags=["Chat"])


# =====================================================
# REQUEST MODEL
# =====================================================
class ChatRequest(BaseModel):
    message: str


# =====================================================
# CHAT ENDPOINT
# =====================================================
@router.post("/")
async def chat(data: ChatRequest, request: Request):

    req_id = getattr(request.state, "request_id", "unknown")

    try:
        logger.info(f"[REQ {req_id}] Chat request received")

        # ---------- VALIDATE INPUT ----------
        message = validate_user_message(data.message)

        # ---------- USER WORKSPACE ----------
        user_id = get_user_id(request)
        vector_path = f"storage/vector_db/{user_id}"

        # ---------- EMBED QUERY ----------
        query_vector = embed_texts([message])

        # ---------- RETRIEVE DOCUMENT CHUNKS ----------
        results = search(
            query_vector,
            vector_path=vector_path,
            k=5
        )

        if not results:
            logger.info(f"[REQ {req_id}] No documents matched")

            return {
                "success": True,
                "answer": "No relevant documents found.",
                "sources": [],
                "confidence": 0.2
            }

        # ---------- BUILD CONTEXT ----------
        context_blocks = [
            f"[Source {i+1}]\n{r['text']}"
            for i, r in enumerate(results)
        ]

        context = "\n\n".join(context_blocks)

        # ---------- ENV VARIABLES ----------
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")

        if not GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY missing")

        client = Groq(api_key=GROQ_API_KEY)

        logger.info(f"[REQ {req_id}] Calling LLM")

        # =====================================================
        # LLM CALL (RAG PROMPT)
        # =====================================================
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": """
You are a document analysis assistant.

Rules:
- Answer ONLY using provided excerpts.
- Extract facts directly from text.
- If partially present, infer carefully.
- Do not hallucinate information.
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

        # ---------- CONFIDENCE HEURISTIC ----------
        confidence = min(0.9, 0.4 + (len(results) * 0.1))

        logger.info(f"[REQ {req_id}] Chat completed successfully")

        return {
            "success": True,
            "answer": answer,
            "sources": results,
            "confidence": confidence
        }

    except Exception as e:
        #  structured logging with traceback
        logger.exception(f"[REQ {req_id}] Chat endpoint failed")

        raise HTTPException(
            status_code=500,
            detail="Internal AI processing error"
        )
