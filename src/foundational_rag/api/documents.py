from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from foundational_rag.core.config import UPLOADS_DIR
from foundational_rag.core.container import ingestion_service

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)) -> dict[str, str | int]:
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

    file_path = UPLOADS_DIR / file.filename

    try:
        content = await file.read()
        file_path.write_bytes(content)

        chunks = ingestion_service.ingest(file_path)

        return {
            "filename": file.filename,
            "chunks": chunks,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc