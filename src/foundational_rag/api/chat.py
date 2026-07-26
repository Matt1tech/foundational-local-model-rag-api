from fastapi import APIRouter

from foundational_rag.api.schemas import (
    ChatRequest,
    ChatResponse,
    SourceResponse,
)
from foundational_rag.core.container import rag_service

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    result = rag_service.ask(request.question)

    return ChatResponse(
        answer=result.answer,
        sources=[
            SourceResponse(
                source=chunk.source,
                chunk_index=chunk.chunk_index,
                score=chunk.score,
            )
            for chunk in result.sources
        ],
    )