from fastapi import APIRouter, Request, HTTPException
from app.documents.manager import list_documents, delete_document
from app.utils.user import get_user_id
import os

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("/")
def get_documents(request: Request):

    user_id = get_user_id(request)

    vector_path = f"storage/vector_db/{user_id}"

    docs = list_documents(vector_path)

    return {"documents": docs}


@router.delete("/{doc_id}")
def remove_document(doc_id: str, request: Request):

    if not doc_id:
        raise HTTPException(status_code=400, detail="Invalid document id")

    user_id = get_user_id(request)

    documents_path = f"storage/documents/{user_id}"
    vector_path = f"storage/vector_db/{user_id}"

    success = delete_document(
        doc_id,
        documents_path,
        vector_path
    )

    if not success:
        raise HTTPException(status_code=404, detail="Document not found")

    return {"message": "Document deleted successfully"}
