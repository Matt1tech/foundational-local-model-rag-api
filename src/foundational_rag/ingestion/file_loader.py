from pathlib import Path

from foundational_rag.ingestion.loaders import (
    BaseLoader,
    DocxLoader,
    PdfLoader,
    TxtLoader,
)


class FileLoader:
    """Selects the appropriate loader based on the file extension."""

    def __init__(self) -> None:
        self._loaders: dict[str, BaseLoader] = {
            ".txt": TxtLoader(),
            ".md": TxtLoader(),  # Markdown is plain text
            ".pdf": PdfLoader(),
            ".docx": DocxLoader(),
        }

    def load(self, file_path: Path) -> str:
        extension = file_path.suffix.lower()
        loader = self._loaders.get(extension)

        if loader is None:
            raise ValueError(f"Unsupported file type: {extension}")

        return loader.load(file_path)