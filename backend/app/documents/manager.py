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


STORAGE_DIR = "storage/documents"


# =====================================================
# LIST DOCUMENTS
# =====================================================
def list_documents():
    metadata = load_metadata()

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
# DELETE DOCUMENT
# =====================================================
def delete_document(doc_id: str):

    metadata = load_metadata()

    print("Deleting doc_id:", doc_id)

    # remove all chunks belonging to document
    remaining = [
        m for m in metadata
        if m.get("doc_id") != doc_id
    ]

    # nothing removed → document not found
    if len(remaining) == len(metadata):
        print("Document not found in metadata")
        return False

    # -------- rebuild FAISS index ----------
    if remaining:
        texts = [m["text"] for m in remaining]

        vectors = embed_texts(texts)

        dimension = vectors.shape[1]
        index = faiss.IndexFlatL2(dimension)

        faiss.normalize_L2(vectors)
        index.add(vectors.astype("float32"))

        save_index(index)
    else:
        # create empty index
        dimension = 384
        index = faiss.IndexFlatL2(dimension)
        save_index(index)

    # save cleaned metadata
    save_metadata(remaining)

    print("Document deleted successfully")

    return True


# =====================================================
# SAVE DOCUMENT (UPLOAD PIPELINE)
# =====================================================
def save_document(upload_file):

    os.makedirs(STORAGE_DIR, exist_ok=True)

    doc_id = str(uuid.uuid4())
    filename = upload_file.filename
    filepath = os.path.join(STORAGE_DIR, f"{doc_id}_{filename}")

    # ---------- SAVE FILE ----------
    with open(filepath, "wb") as buffer:
        buffer.write(upload_file.file.read())

    # ---------- EXTRACT TEXT ----------
    extracted_text = parse_file(filepath)

    if not extracted_text or not extracted_text.strip():
        raise ValueError("No readable text found in document")

    # ---------- CHUNK TEXT ----------
    chunks = chunk_text(extracted_text)

    if not chunks:
        raise ValueError("Document produced no valid chunks")

    # ---------- EMBEDDINGS ----------
    vectors = embed_texts(chunks)

    # metadata per chunk (THIS is your only metadata system now)
    metadatas = [
        {
            "document": filename,
            "text": chunk,
            "doc_id": doc_id
        }
        for chunk in chunks
    ]

    # ---------- STORE IN VECTOR DB ----------
    add_embeddings(vectors, metadatas)

    # IMPORTANT:
    # NO extra metadata saving anymore.
    # vector_db/metadata.json is already updated.

    return {
        "id": doc_id,
        "name": filename,
        "chunks": len(chunks),
        "text_length": len(extracted_text),
    }
