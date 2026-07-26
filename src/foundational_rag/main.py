from fastapi import FastAPI

from foundational_rag.api.chat import router as chat_router
from foundational_rag.api.documents import router as documents_router
from foundational_rag.api.health import router as health_router

app = FastAPI(
    title="Foundational Local Model RAG API",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(documents_router)
app.include_router(chat_router)