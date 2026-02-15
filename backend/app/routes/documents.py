from fastapi import APIRouter, HTTPException
from app.documents.manager import list_documents, delete_document

router = APIRouter(prefix="/documents", tags=["Documents"])


# ---------- LIST DOCUMENTS ----------
@router.get("/")
def get_documents():
    return {
        "documents": list_documents()
    }


# ---------- DELETE DOCUMENT ----------
@router.delete("/{doc_id}")
def remove_document(doc_id: str):

    success = delete_document(doc_id)

    if not success:
        raise HTTPException(status_code=404, detail="Document not found")

    return {"message": "Document deleted successfully"}
