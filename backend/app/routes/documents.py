from fastapi import APIRouter, HTTPException, Request
from app.documents.manager import list_documents, delete_document
from app.utils.user import get_user_id
import os

router = APIRouter(prefix="/documents", tags=["Documents"])


# ---------- LIST DOCUMENTS ----------

@router.get("/")
def get_documents(request: Request):
    return {
        "documents": list_documents(request)
    }

# ---------- DELETE DOCUMENT ----------
@router.delete("/{doc_id}")
def remove_document(doc_id: str, request: Request):

    success = delete_document(doc_id, request)

    if not success:
        raise HTTPException(status_code=404, detail="Document not found")

    return {"message": "Document deleted"}


@router.get("/")
def list_documents(request: Request):
    user_id = get_user_id(request)

    user_dir = f"storage/documents/{user_id}"

    if not os.path.exists(user_dir):
        return []

    return os.listdir(user_dir)