import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import chat, upload, documents, health
from app.middleware.request_logger import RequestLoggingMiddleware


# ---------------- STORAGE ----------------
# Railway containers start empty → create folders at boot
os.makedirs("storage/documents", exist_ok=True)
os.makedirs("storage/vector_db", exist_ok=True)


# ---------------- APP ----------------
app = FastAPI(
    title="QuantumLeap AI API",
    version="1.0.0"
)


# ---------------- CORS (MUST BE FIRST) ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://quantamleap-ai.vercel.app",   # live frontend
        "https://quantumleap-ai.vercel.app",   # backup domain
        "http://localhost:5173",               # local dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- REQUEST LOGGING ----------------
app.add_middleware(RequestLoggingMiddleware)


# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {"message": "QuantumLeap AI Backend running"}


# ---------------- ROUTERS ----------------
app.include_router(chat.router)
app.include_router(upload.router)
app.include_router(documents.router)
app.include_router(health.router)
