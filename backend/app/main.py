import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import chat, upload, documents, health

#  create storage folders (Railway containers start empty)
os.makedirs("storage/documents", exist_ok=True)
os.makedirs("storage/vector_db", exist_ok=True)

#  CREATE APP FIRST
app = FastAPI(
    title="Private Knowledge Workspace API",
    version="1.0.0"
)

#  CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  ROOT
@app.get("/")
def root():
    return {"message": "Backend running "}

#  ROUTERS
app.include_router(chat.router)
app.include_router(upload.router)
app.include_router(documents.router)
app.include_router(health.router)
