from pathlib import Path
from typing import Any

from foundational_rag.ingestion.chunker import TextChunker
from foundational_rag.services.ingestion_service import IngestionService


class FakeFileLoader:
    def load(self, file_path: Path) -> str:
        return "abcdefghij"


class FakeEmbeddingService:
    def embed_many(self, texts: list[str]) -> list[list[float]]:
        return [[float(index)] for index, _ in enumerate(texts)]


class FakeVectorStore:
    def __init__(self) -> None:
        self.points: list[dict[str, Any]] = []

    def add(
        self,
        point_id: str,
        embedding: list[float],
        payload: dict[str, Any],
    ) -> None:
        self.points.append(
            {
                "point_id": point_id,
                "embedding": embedding,
                "payload": payload,
            }
        )


def test_ingest_processes_and_stores_chunks(tmp_path: Path) -> None:
    file_path = tmp_path / "lecture.txt"
    file_path.write_text("abcdefghij", encoding="utf-8")

    vector_store = FakeVectorStore()

    service = IngestionService(
        file_loader=FakeFileLoader(),  # type: ignore[arg-type]
        chunker=TextChunker(chunk_size=6, chunk_overlap=2),
        embedding_service=FakeEmbeddingService(),  # type: ignore[arg-type]
        vector_store=vector_store,  # type: ignore[arg-type]
    )

    chunk_count = service.ingest(file_path)

    assert chunk_count == 2
    assert len(vector_store.points) == 2

    assert vector_store.points[0]["payload"]["source"] == "lecture.txt"
    assert vector_store.points[0]["payload"]["chunk_index"] == 0
    assert vector_store.points[0]["payload"]["content"] == "abcdef"

    assert vector_store.points[0]["point_id"]
    assert (
        vector_store.points[0]["point_id"]
        != vector_store.points[1]["point_id"]
    )