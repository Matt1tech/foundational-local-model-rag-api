from pydantic import BaseModel, HttpUrl


class ChatRequest(BaseModel):
    question: str


class SourceResponse(BaseModel):
    source: str
    chunk_index: int
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]
    
class CrawlDocumentRequest(BaseModel):
    url: HttpUrl