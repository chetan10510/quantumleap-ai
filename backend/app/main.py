import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import chat, upload, documents, health

# ---------------- STORAGE ----------------
os.makedirs("storage/documents", exist_ok=True)
os.makedirs("storage/vector_db", exist_ok=True)

# ---------------- APP ----------------
app = FastAPI(
    title="QuantumLeap AI API",
    version="1.0.0"
)

# ---------------- CORS (CRITICAL FIX) ----------------
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",

    #  Vercel frontend URL - UPDATE THIS TO YOUR FRONTEND DEPLOYMENT URL
    "https://quantamleap-ai.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {"message": "QuantumLeap AI Backend running"}

# ---------------- ROUTERS ----------------
app.include_router(chat.router)
app.include_router(upload.router)
app.include_router(documents.router)
app.include_router(health.router)
