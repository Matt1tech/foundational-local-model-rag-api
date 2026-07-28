from pathlib import Path
from uuid import uuid4
import logging

from foundational_rag.ingestion.chunker import TextChunker
from foundational_rag.ingestion.file_loader import FileLoader
from foundational_rag.retrieval.embeddings import EmbeddingService
from foundational_rag.retrieval.vector_store import VectorStore


logger = logging.getLogger(__name__)


class IngestionService:
    """Processes documents and stores them in the vector database."""

    def __init__(
        self,
        file_loader: FileLoader,
        chunker: TextChunker,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ) -> None:
        self.file_loader = file_loader
        self.chunker = chunker
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def ingest(
        self,
        file_path: Path,
        document_id: str,
    ) -> int:
        """Load, chunk, embed, and store a document."""

        logger.info(
            "Starting document ingestion: document_id=%s source=%s",
            document_id,
            file_path.name,
        )

        try:
            text = self.file_loader.load(file_path)
            chunks = self.chunker.split(text)

            embeddings = self.embedding_service.embed_many(
                [chunk.content for chunk in chunks]
            )

            for chunk, embedding in zip(chunks, embeddings):
                self.vector_store.add(
                    point_id=str(uuid4()),
                    embedding=embedding,
                    payload={
                        "document_id": document_id,
                        "source": file_path.name,
                        "chunk_index": chunk.chunk_index,
                        "content": chunk.content,
                    },
                )

            logger.info(
                "Document indexed successfully: document_id=%s chunks=%d",
                document_id,
                len(chunks),
            )

            return len(chunks)

        except Exception:
            logger.exception(
                "Document ingestion failed: document_id=%s source=%s",
                document_id,
                file_path.name,
            )
            raise