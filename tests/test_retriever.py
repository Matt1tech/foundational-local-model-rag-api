from typing import Any

import pytest

from foundational_rag.retrieval.retriever import Retriever


class FakeEmbeddingService:
    def embed(self, text: str) -> list[float]:
        return [0.1, 0.2, 0.3]


class FakeSearchResult:
    def __init__(
        self,
        payload: dict[str, Any],
        score: float,
    ) -> None:
        self.payload = payload
        self.score = score


class FakeVectorStore:
    def search(
        self,
        query_embedding: list[float],
        limit: int,
    ) -> list[FakeSearchResult]:
        assert query_embedding == [0.1, 0.2, 0.3]
        assert limit == 2

        return [
            FakeSearchResult(
                payload={
                    "content": "A deadlock occurs when processes wait indefinitely.",
                    "source": "operating_systems.pdf",
                    "chunk_index": 4,
                },
                score=0.88,
            )
        ]


def test_retrieve_returns_relevant_chunks() -> None:
    retriever = Retriever(
        embedding_service=FakeEmbeddingService(),  # type: ignore[arg-type]
        vector_store=FakeVectorStore(),  # type: ignore[arg-type]
        top_k=2,
    )

    results = retriever.retrieve("What is a deadlock?")

    assert len(results) == 1
    assert results[0].source == "operating_systems.pdf"
    assert results[0].chunk_index == 4
    assert results[0].score == 0.88


def test_empty_query_raises_error() -> None:
    retriever = Retriever(
        embedding_service=FakeEmbeddingService(),  # type: ignore[arg-type]
        vector_store=FakeVectorStore(),  # type: ignore[arg-type]
    )

    with pytest.raises(ValueError, match="Query cannot be empty"):
        retriever.retrieve(" ")