from qdrant_client import QdrantClient

from foundational_rag.core.config import QDRANT_DIR


def create_qdrant_client() -> QdrantClient:
    """Create a local persistent Qdrant client."""

    QDRANT_DIR.mkdir(parents=True, exist_ok=True)

    return QdrantClient(path=str(QDRANT_DIR))