import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from foundational_rag.core.config import DOCUMENTS_FILE


logger = logging.getLogger(__name__)


class DocumentService:
    def __init__(self, metadata_file: Path = DOCUMENTS_FILE) -> None:
        self.metadata_file = metadata_file
        self._initialize_store()

    def create_document(
        self,
        *,
        document_id: str,
        original_filename: str,
        stored_filename: str,
        mime_type: str | None,
        file_size: int,
        content_hash: str,
        chunk_count: int,
    ) -> dict[str, Any]:
        document = {
            "document_id": document_id,
            "original_filename": original_filename,
            "stored_filename": stored_filename,
            "mime_type": mime_type,
            "file_size": file_size,
            "content_hash": content_hash,
            "chunk_count": chunk_count,
            "uploaded_at": datetime.now(timezone.utc).isoformat(),
        }

        try:
            documents = self.list_documents()
            documents.append(document)

            self._write_documents(documents)

            logger.info(
                "Document metadata created: "
                "document_id=%s source=%s chunks=%d",
                document_id,
                original_filename,
                chunk_count,
            )

            return document

        except Exception:
            logger.exception(
                "Failed to create document metadata: document_id=%s",
                document_id,
            )
            raise

    def list_documents(self) -> list[dict[str, Any]]:
        return self._read_documents()

    def get_document(self, document_id: str) -> dict[str, Any] | None:
        documents = self.list_documents()

        return next(
            (
                document
                for document in documents
                if document["document_id"] == document_id
            ),
            None,
        )

    def get_document_by_hash(
        self,
        content_hash: str,
    ) -> dict[str, Any] | None:
        documents = self.list_documents()

        return next(
            (
                document
                for document in documents
                if document["content_hash"] == content_hash
            ),
            None,
        )

    def delete_document(self, document_id: str) -> dict[str, Any] | None:
        try:
            documents = self.list_documents()

            document = next(
                (
                    item
                    for item in documents
                    if item["document_id"] == document_id
                ),
                None,
            )

            if document is None:
                logger.warning(
                    "Document metadata not found: document_id=%s",
                    document_id,
                )
                return None

            remaining_documents = [
                item
                for item in documents
                if item["document_id"] != document_id
            ]

            self._write_documents(remaining_documents)

            logger.info(
                "Document metadata deleted: document_id=%s source=%s",
                document_id,
                document["original_filename"],
            )

            return document

        except Exception:
            logger.exception(
                "Failed to delete document metadata: document_id=%s",
                document_id,
            )
            raise

    def _initialize_store(self) -> None:
        self.metadata_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.metadata_file.exists():
            self._write_documents([])

            logger.info(
                "Document metadata store created: path=%s",
                self.metadata_file,
            )

    def _read_documents(self) -> list[dict[str, Any]]:
        try:
            with self.metadata_file.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

        except json.JSONDecodeError as exc:
            logger.exception(
                "Invalid document metadata JSON: path=%s",
                self.metadata_file,
            )

            raise RuntimeError(
                f"Invalid document metadata file: {self.metadata_file}"
            ) from exc

        except OSError:
            logger.exception(
                "Failed to read document metadata: path=%s",
                self.metadata_file,
            )
            raise

        if not isinstance(data, list):
            logger.error(
                "Document metadata is not a list: path=%s",
                self.metadata_file,
            )

            raise RuntimeError(
                "Document metadata must contain a JSON list."
            )

        return data

    def _write_documents(
        self,
        documents: list[dict[str, Any]],
    ) -> None:
        temporary_file = self.metadata_file.with_suffix(".tmp")

        try:
            with temporary_file.open(
                "w",
                encoding="utf-8",
            ) as file:
                json.dump(
                    documents,
                    file,
                    indent=2,
                    ensure_ascii=False,
                )

            temporary_file.replace(self.metadata_file)

        except Exception:
            logger.exception(
                "Failed to write document metadata: path=%s",
                self.metadata_file,
            )

            temporary_file.unlink(missing_ok=True)
            raise