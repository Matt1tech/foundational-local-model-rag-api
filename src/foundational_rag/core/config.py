from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_DIR = PROJECT_ROOT / "data"

UPLOADS_DIR = DATA_DIR / "uploads"

QDRANT_DIR = DATA_DIR / "qdrant"

COLLECTION_NAME = "lecture_chunks"

EMBEDDING_MODEL = "embeddinggemma"

LLM_MODEL = "qwen2.5:3b"

VECTOR_SIZE = 768

TOP_K = 3