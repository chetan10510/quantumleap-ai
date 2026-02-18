# QuantumLeap AI — Private Knowledge Workspace

QuantumLeap AI is a private knowledge Q&A web application that allows users to upload documents and ask questions grounded strictly in their own data.

## Features

- Upload documents (PDF, DOCX, TXT, MD)
- Per-user isolated workspace
- Semantic search using embeddings
- AI grounded answers
- Source highlighting showing evidence used
- System health status page

## Tech Stack

Frontend:
- React + Vercel

Backend:
- FastAPI
- FAISS vector database
- SentenceTransformers embeddings
- Groq LLM API (Llama 3.1)

Hosting:
- Railway (backend) + Render(backend - backup)
- Vercel (frontend)

## How to Run Locally

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```
