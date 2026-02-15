from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from app.documents.manager import save_document
import os

router = APIRouter(prefix="/upload", tags=["Upload"])

# Allowed file types
ALLOWED_EXTENSIONS = (".pdf", ".docx", ".xlsx", ".txt", ".md")


@router.post("/")
async def upload_documents(files: List[UploadFile] = File(...)):
    """
    Upload one or multiple documents.
    Extraction + chunking + embeddings handled in manager.py
    """

    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    uploaded = []
    rejected = []

    for file in files:

        if not file.filename:
            continue

        ext = os.path.splitext(file.filename)[1].lower()

        # ---------- VALIDATION ----------
        if ext not in ALLOWED_EXTENSIONS:
            rejected.append(file.filename)
            continue

        try:
            saved = save_document(file)
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
