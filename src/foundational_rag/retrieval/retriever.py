from dataclasses import dataclass

from foundational_rag.retrieval.embeddings import EmbeddingService
from foundational_rag.retrieval.vector_store import VectorStore


@dataclass
class RetrievedChunk:
    """Represents a retrieved document chunk."""

    content: str
    source: str
    chunk_index: int
    score: float


class Retriever:
    """Retrieves relevant chunks for a user query."""

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
        top_k: int = 3,
    ) -> None:
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.top_k = top_k

    def retrieve(self, query: str) -> list[RetrievedChunk]:
        """Retrieve the most relevant chunks for a query."""

        if not query.strip():
            raise ValueError("Query cannot be empty")

        query_embedding = self.embedding_service.embed(query)

        results = self.vector_store.search(
            query_embedding=query_embedding,
            limit=self.top_k,
        )

        return [
            RetrievedChunk(
                content=result.payload["content"],
                source=result.payload["source"],
                chunk_index=result.payload["chunk_index"],
                score=result.score,
            )
            for result in results
        ]