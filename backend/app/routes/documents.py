from fastapi import APIRouter, HTTPException, Request
from app.documents.manager import list_documents, delete_document
from app.utils.user import get_user_id
import os

router = APIRouter(prefix="/documents", tags=["Documents"])


# ---------- LIST DOCUMENTS ----------
@router.get("/")
def get_documents():
    return {
        "documents": list_documents()
    }


# ---------- DELETE DOCUMENT ----------
@router.delete("/{doc_id}")
def delete_document(doc_id: str, request: Request):

    user_id = get_user_id(request)
    user_dir = f"storage/documents/{user_id}"

    file_path = os.path.join(user_dir, doc_id)

    if not os.path.exists(file_path):
        return {"message": "File not found"}

    os.remove(file_path)

    return {"message": "Document deleted"}

@router.get("/")
def list_documents(request: Request):
    user_id = get_user_id(request)

    user_dir = f"storage/documents/{user_id}"

    if not os.path.exists(user_dir):
        return []

    return os.listdir(user_dir)