from fastapi import APIRouter, Request, HTTPException
from app.rag.embed import embed_texts
from app.rag.retrieve import search
from app.rag.generate import generate_answer
from app.utils.user import get_user_id

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/")
async def chat(request: Request):

    body = await request.json()
    message = body.get("message")

    if not message:
        raise HTTPException(status_code=400, detail="Message required")

    #  user workspace isolation
    user_id = get_user_id(request)
    vector_path = f"storage/vector_db/{user_id}"

    # embed query
    query_vector = embed_texts([message])

    #  IMPORTANT FIX — pass vector_path
    results = search(
        query_vector,
        vector_path=user_vector_dir,
        k=3
    )

    if not results:
        return {
            "answer": "No relevant documents found.",
            "sources": [],
            "confidence": "Low"
        }

    context = "\n\n".join([r["text"] for r in results])

    #  call LLM
    answer = generate_answer(message, context)

    return {
        "answer": answer,
        "sources": results,
        "confidence": "Medium"
    }
