from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(
    title="RAG Regulasi API",
    description="API Chatbot RAG untuk Regulasi Perguruan Tinggi menggunakan Gemini",
    version="1.0.0"
)

# CORS configuration (agar bisa diakses frontend / browser)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint (penting untuk Jenkins / Docker healthcheck)
@app.get("/")
def health_check():
    return {
        "status": "running",
        "service": "RAG Regulasi API"
    }

# Include router dari app/api/routes.py
app.include_router(router)