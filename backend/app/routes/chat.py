from fastapi import APIRouter, Request
from pydantic import BaseModel

from app.rag.embed import embed_texts
from app.rag.retrieve import search
from app.rag.generate import generate_answer
from app.utils.user import get_user_id

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    message: str


@router.post("/")
async def chat(body: ChatRequest, request: Request):

    question = body.message.strip()

    if not question:
        return {
            "answer": "Empty question.",
            "sources": [],
            "confidence": "Low"
        }

    # USER WORKSPACE
    user_id = get_user_id(request)
    vector_path = f"storage/vector_db/{user_id}"

    # embed query
    query_vector = embed_texts([question])

    # NEW SEARCH SIGNATURE
    results = search(query_vector, vector_path, k=3)

    if not results:
        return {
            "answer": "No relevant documents found.",
            "sources": [],
            "confidence": "Low"
        }

    # build context
    context = "\n\n".join([r["text"] for r in results])

    # generate LLM answer
    answer = generate_answer(context, question)

    return {
        "answer": answer,
        "sources": results,
        "confidence": "Medium"
    }
