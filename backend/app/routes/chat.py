from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.rag.embed import embed_texts
from app.rag.retrieve import search, load_metadata
from app.rag.generate import generate_answer

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    message: str

@router.post("/")
def chat(req: ChatRequest):

    if not req.message.strip():
        return {
            "answer": "Please enter a question.",
            "sources": [],
            "confidence": 0
        }

    query_vector = embed_texts([req.message])
    results = search(query_vector, k=3)

    if not results:
        return {
            "answer": "No documents uploaded or no relevant information found.",
            "sources": [],
            "confidence": 0
        }

    contexts = [r["text"] for r in results]

    answer = generate_answer(req.message, contexts)

    # ---------- CONFIDENCE ----------
# Convert FAISS L2 distance → confidence score
    avg_distance = sum(r["score"] for r in results) / len(results)

    confidence = 1 / (1 + avg_distance)
    confidence = round(confidence, 2)


    formatted_sources = [
        {
            "document": r["document"],
            "snippet": r["text"].strip(),
            "doc_id": r["doc_id"],
            "score": r["score"]
        }
        for r in results
    ]

    return {
        "answer": answer,
        "sources": formatted_sources,
        "confidence": round(confidence, 2)
    }
