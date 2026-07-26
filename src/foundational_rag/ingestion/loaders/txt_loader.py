from pathlib import Path

from foundational_rag.ingestion.loaders.base import BaseLoader


class TxtLoader(BaseLoader):
    """Loads plain text files."""

    def load(self, file_path: Path) -> str:
        return file_path.read_text(encoding="utf-8")