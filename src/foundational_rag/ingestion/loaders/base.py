from abc import ABC, abstractmethod
from pathlib import Path


class BaseLoader(ABC):
    """Base class for all document loaders."""

    @abstractmethod
    def load(self, file_path: Path) -> str:
        """Extract and return the document text."""
        pass