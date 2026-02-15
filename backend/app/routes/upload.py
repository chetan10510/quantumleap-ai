from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from typing import List
from app.documents.manager import save_document
from app.utils.user import get_user_id
import os

router = APIRouter(prefix="/upload", tags=["Upload"])

ALLOWED_EXTENSIONS = (".pdf", ".docx", ".xlsx", ".txt", ".md")


@router.post("/")
async def upload_documents(
    request: Request,
    files: List[UploadFile] = File(...)
):
    """
    Upload documents scoped per user workspace.
    """

    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    user_id = get_user_id(request)

    # USER-SPECIFIC STORAGE
    user_doc_dir = f"storage/documents/{user_id}"
    user_vector_dir = f"storage/vector_db/{user_id}"

    os.makedirs(user_doc_dir, exist_ok=True)
    os.makedirs(user_vector_dir, exist_ok=True)

    uploaded = []
    rejected = []

    for file in files:

        if not file.filename:
            continue

        ext = os.path.splitext(file.filename)[1].lower()

        if ext not in ALLOWED_EXTENSIONS:
            rejected.append(file.filename)
            continue

        try:
            saved = await save_document(
                file,
                documents_path=user_doc_dir,
                vector_path=user_vector_dir,
            )
            uploaded.append(saved)

        except Exception as e:
            print("Upload failed:", e)
            rejected.append(file.filename)

    if not uploaded:
        raise HTTPException(
            status_code=400,
            detail="No valid files uploaded"
        )

    return {
        "message": f"{len(uploaded)} file(s) uploaded successfully",
        "uploaded": uploaded,
        "rejected_files": rejected
    }
