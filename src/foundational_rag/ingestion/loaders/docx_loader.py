from pathlib import Path

from docx import Document

from foundational_rag.ingestion.loaders.base import BaseLoader


class DocxLoader(BaseLoader):
    """Loads Microsoft Word documents."""

    def load(self, file_path: Path) -> str:
        document = Document(file_path)

        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )