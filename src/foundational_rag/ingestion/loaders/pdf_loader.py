from pathlib import Path

from pypdf import PdfReader

from foundational_rag.ingestion.loaders.base import BaseLoader


class PdfLoader(BaseLoader):
    """Loads PDF documents."""

    def load(self, file_path: Path) -> str:
        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text