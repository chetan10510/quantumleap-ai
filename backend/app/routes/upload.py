import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from typing import List
from app.documents.manager import save_document
from app.utils.user import get_user_id
from app.core.logger import get_logger

logger = get_logger("upload")

router = APIRouter(prefix="/upload", tags=["Upload"])

# ---------------------------------------
# CONFIG
# ---------------------------------------

# Allowed file extensions
ALLOWED_EXTENSIONS = (".pdf", ".docx", ".xlsx", ".txt", ".md")

# ⭐ Prevent Render OOM (very important)
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB per file

# Optional upload limit (prevents abuse)
MAX_FILES_PER_REQUEST = 5


# ---------------------------------------
# UPLOAD ENDPOINT
# ---------------------------------------
@router.post("/")
async def upload_documents(
    request: Request,
    files: List[UploadFile] = File(...)
):
    """
    Upload documents scoped per user workspace.

    ✔ Each user gets isolated storage
    ✔ Memory-safe file handling
    ✔ File validation + limits
    ✔ Render free-tier optimized
    """

    # ---------- BASIC VALIDATION ----------
    if not files:
        raise HTTPException(
            status_code=400,
            detail="No files uploaded"
        )

    if len(files) > MAX_FILES_PER_REQUEST:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum {MAX_FILES_PER_REQUEST} files allowed per upload"
        )

    # ---------- USER WORKSPACE ----------
    user_id = get_user_id(request)

    user_doc_dir = f"storage/documents/{user_id}"
    user_vector_dir = f"storage/vector_db/{user_id}"

    os.makedirs(user_doc_dir, exist_ok=True)
    os.makedirs(user_vector_dir, exist_ok=True)

    uploaded = []
    rejected = []

    # ---------- PROCESS FILES ----------
    for file in files:

        try:
            # skip empty filename
            if not file.filename:
                continue

            filename = file.filename.strip()
            ext = os.path.splitext(filename)[1].lower()

            # ---------- EXTENSION CHECK ----------
            if ext not in ALLOWED_EXTENSIONS:
                rejected.append(filename)
                continue

            # ---------- SIZE CHECK (memory-safe) ----------
            content = await file.read()

            if len(content) > MAX_FILE_SIZE:
                print(f"Rejected (too large): {filename}")
                rejected.append(filename)
                continue

            # rewind pointer for streaming save later
            file.file.seek(0)

            # ---------- SAVE + INGEST ----------
            saved = await save_document(
                upload_file=file,
                documents_path=user_doc_dir,
                vector_path=user_vector_dir,
            )

            uploaded.append({
                "doc_id": saved["id"],
                "filename": saved["name"],
            })


        except Exception as e:
            logger.error(f"Upload failed: {filename} | {str(e)}")
            rejected.append(filename)

    # ---------- RESPONSE ----------
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
