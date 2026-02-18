import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.middleware import RequestLoggingMiddleware
from app.routes import chat, upload, documents, health
from app.middleware.error_handler import GlobalErrorHandlerMiddleware
from app.middleware.request_id import RequestIDMiddleware

#  create storage folders (Railway containers start empty)
os.makedirs("storage/documents", exist_ok=True)
os.makedirs("storage/vector_db", exist_ok=True)

#  CREATE APP FIRST
app = FastAPI(
    title="QuantumLeap AI API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://quantumleap-ai.vercel.app",  # your frontend URL
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request tracing
app.add_middleware(RequestIDMiddleware)

# Global error handler
app.add_middleware(GlobalErrorHandlerMiddleware)

# Request logging middleware
app.add_middleware(RequestLoggingMiddleware)

#  ROOT
@app.get("/")
def root():
    return {"message": "QuantumLeap AI Backend running"}

#  ROUTERS
app.include_router(chat.router)
app.include_router(upload.router)
app.include_router(documents.router)
app.include_router(health.router)
