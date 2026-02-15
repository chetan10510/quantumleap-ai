import os
import faiss
import uuid
import numpy as np

from app.documents.parser import parse_file
from app.utils.chunking import chunk_text
from app.rag.retrieve import (
    load_metadata,
    save_metadata,
    save_index,
    load_index,
    add_embeddings,
)
from app.rag.embed import embed_texts


# =====================================================
# LIST DOCUMENTS (PER USER)
# =====================================================
def list_documents(vector_path: str):
    """
    Returns unique documents uploaded by this user.
    """

    metadata = load_metadata(vector_path)

    docs = []
    seen = set()

    for item in metadata:
        doc_id = item.get("doc_id")
        filename = item.get("document")

        if doc_id and doc_id not in seen:
            docs.append({
                "doc_id": doc_id,
                "filename": filename
            })
            seen.add(doc_id)

    return docs


# =====================================================
# DELETE DOCUMENT (FAST VERSION — NO RE-EMBEDDING)
# =====================================================
def delete_document(doc_id: str, documents_path: str, vector_path: str):
    """
    Deletes a document and rebuilds FAISS index
    WITHOUT recomputing embeddings.
    """

    metadata = load_metadata(vector_path)

    print("Deleting doc_id:", doc_id)

    # remove chunks belonging to this document
    remaining = [
        m for m in metadata
        if m.get("doc_id") != doc_id
    ]

    # nothing removed
    if len(remaining) == len(metadata):
        print("Document not found")
        return False

    # ---------- DELETE FILE FROM STORAGE ----------
    if os.path.exists(documents_path):
        for file in os.listdir(documents_path):
            if file.startswith(doc_id):
                try:
                    os.remove(os.path.join(documents_path, file))
                except Exception:
                    pass

    # ---------- FAST FAISS REBUILD ----------
    try:
        old_index = load_index(vector_path)

        dimension = old_index.d
        new_index = faiss.IndexFlatL2(dimension)

        if remaining and old_index.ntotal > 0:

            # get all stored vectors
            all_vectors = old_index.reconstruct_n(
                0, old_index.ntotal
            )

            # keep vectors NOT belonging to deleted doc
            keep_ids = [
                i for i, m in enumerate(metadata)
                if m.get("doc_id") != doc_id
            ]

            filtered_vectors = all_vectors[keep_ids]

            if len(filtered_vectors) > 0:
                new_index.add(
                    np.array(filtered_vectors).astype("float32")
                )

        save_index(new_index, vector_path)

    except Exception as e:
        print("Index rebuild fallback:", e)

        # fallback empty index
        dimension = 384
        new_index = faiss.IndexFlatL2(dimension)
        save_index(new_index, vector_path)

    # ---------- SAVE CLEAN METADATA ----------
    save_metadata(remaining, vector_path)

    print("Document deleted successfully")

    return True


# =====================================================
# SAVE DOCUMENT (UPLOAD PIPELINE — PER USER)
# =====================================================
async def save_document(
    upload_file,
    documents_path: str,
    vector_path: str,
):
    """
    Full ingestion pipeline:
    save -> parse -> chunk -> embed -> store vectors
    """

    os.makedirs(documents_path, exist_ok=True)
    os.makedirs(vector_path, exist_ok=True)

    doc_id = str(uuid.uuid4())
    filename = upload_file.filename

    filepath = os.path.join(
        documents_path,
        f"{doc_id}_{filename}"
    )

    # ---------- SAVE FILE ----------
    with open(filepath, "wb") as buffer:
        buffer.write(await upload_file.read())

    # ---------- EXTRACT TEXT ----------
    extracted_text = parse_file(filepath)

    if not extracted_text or not extracted_text.strip():
        raise ValueError("No readable text found")

    # ---------- CHUNK TEXT ----------
    chunks = chunk_text(extracted_text)

    if not chunks:
        raise ValueError("No valid chunks produced")

    # ---------- EMBEDDINGS ----------
    vectors = embed_texts(chunks)

    # metadata per chunk
    metadatas = [
        {
            "document": filename,
            "text": chunk,
            "doc_id": doc_id,
        }
        for chunk in chunks
    ]

    # ---------- STORE IN VECTOR DB ----------
    add_embeddings(
        vectors,
        metadatas,
        vector_path=vector_path
    )

    return {
        "id": doc_id,
        "name": filename,
        "chunks": len(chunks),
        "text_length": len(extracted_text),
    }
