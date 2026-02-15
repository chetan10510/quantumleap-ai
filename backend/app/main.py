import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat, upload, documents, health
os.makedirs("storage/documents", exist_ok=True)
os.makedirs("storage/vector_db", exist_ok=True)

app = FastAPI(
    title="Private Knowledge Workspace API",
    version="1.0.0"
)

# CORS (frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root test
@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}

# Register routes
app.include_router(chat.router)
app.include_router(upload.router)
app.include_router(documents.router)
app.include_router(health.router)


# Root test route
@app.get("/")
def root():
    return {"message": "Backend is running"}
