import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import chat, upload, documents, health

# Ensure storage folders exist
os.makedirs("storage/documents", exist_ok=True)
os.makedirs("storage/vector_db", exist_ok=True)

app = FastAPI(
    title="Private Knowledge Workspace API",
    version="1.0.0"
)

# -------------------------
# CORS (Frontend connection)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Root endpoint (Render check)
# -------------------------
@app.get("/")
def root():
    return {"status": "Aggroso AI backend running 🚀"}

# -------------------------
# Explicit health endpoint
# (important for Render)
# -------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}

# -------------------------
# Register API routers
# -------------------------
app.include_router(chat.router)
app.include_router(upload.router)
app.include_router(documents.router)
app.include_router(health.router)
