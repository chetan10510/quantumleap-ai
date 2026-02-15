import os
import faiss
import uuid

from app.documents.parser import parse_file
from app.utils.chunking import chunk_text
from app.rag.retrieve import (
    load_metadata,
    save_metadata,
    save_index,
    add_embeddings,
)
from app.rag.embed import embed_texts


# ===============================
# LIST DOCUMENTS
# ===============================
def list_documents(vector_path: str):

    metadata = load_metadata(vector_path)

    docs = {}
    for m in metadata:
        docs[m["doc_id"]] = m["document"]

    return [
        {"doc_id": k, "filename": v}
        for k, v in docs.items()
    ]


# ===============================
# FAST DELETE (NO VECTOR LOAD)
# ===============================
def delete_document(doc_id: str, documents_path: str, vector_path: str):

    metadata = load_metadata(vector_path)

    remaining = [
        m for m in metadata
        if m["doc_id"] != doc_id
    ]

    if len(remaining) == len(metadata):
        return False

    # delete stored file
    if os.path.exists(documents_path):
        for f in os.listdir(documents_path):
            if f.startswith(doc_id):
                try:
                    os.remove(os.path.join(documents_path, f))
                except:
                    pass

    # recreate EMPTY index (FAST + SAFE)
    index = faiss.IndexFlatL2(384)
    save_index(index, vector_path)

    save_metadata(remaining, vector_path)

    return True


# ===============================
# SAVE DOCUMENT
# ===============================
async def save_document(upload_file, documents_path: str, vector_path: str):

    os.makedirs(documents_path, exist_ok=True)
    os.makedirs(vector_path, exist_ok=True)

    doc_id = str(uuid.uuid4())
    filename = upload_file.filename

    filepath = os.path.join(
        documents_path,
        f"{doc_id}_{filename}"
    )

    # STREAM WRITE (NO RAM SPIKE)
    with open(filepath, "wb") as buffer:
        while True:
            chunk = await upload_file.read(1024 * 1024)
            if not chunk:
                break
            buffer.write(chunk)

    # ---------- PARSE ----------
    extracted_text = parse_file(filepath)

    if not extracted_text.strip():
        raise ValueError("Empty document")

    # ---------- CHUNK ----------
    chunks = chunk_text(extracted_text)

    # HARD LIMIT (Render safety)
    chunks = chunks[:200]

    if not chunks:
        raise ValueError("No chunks")

    # ---------- EMBED ----------
    vectors = embed_texts(chunks)

    metadatas = [
        {
            "document": filename,
            "text": c,
            "doc_id": doc_id,
        }
        for c in chunks
    ]

    add_embeddings(
        vectors,
        metadatas,
        vector_path=vector_path
    )

    return {
        "id": doc_id,
        "name": filename,
        "chunks": len(chunks),
    }
