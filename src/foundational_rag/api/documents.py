from pathlib import Path
from shutil import copyfileobj
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from foundational_rag.core.config import UPLOADS_DIR
from foundational_rag.core.container import (
    document_service,
    ingestion_service,
    vector_store,
    web_crawl_service,
)

from foundational_rag.api.schemas import (
    CrawlDocumentRequest,
)
from foundational_rag.services.web_crawl_service import (
    DuplicateWebDocumentError,
    WebCrawlError,
)
from foundational_rag.core.file_utils import calculate_file_hash


router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)




@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
)
def upload_document(
    file: UploadFile = File(...),
) -> dict:
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must have a filename.",
        )

    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

    document_id = str(uuid4())
    file_extension = Path(file.filename).suffix.lower()
    stored_filename = f"{document_id}{file_extension}"
    file_path = UPLOADS_DIR / stored_filename

    try:
        with file_path.open("wb") as destination:
            copyfileobj(file.file, destination)

        content_hash = calculate_file_hash(file_path)

        existing_document = document_service.get_document_by_hash(
            content_hash
        )

        if existing_document is not None:
            file_path.unlink(missing_ok=True)

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "message": "Document already exists.",
                    "document_id": existing_document["document_id"],
                    "filename": existing_document["original_filename"],
                },
            )

        chunk_count = ingestion_service.ingest(
            file_path=file_path,
            document_id=document_id,
        )

        document = document_service.create_document(
            document_id=document_id,
            original_filename=file.filename,
            stored_filename=stored_filename,
            mime_type=file.content_type,
            file_size=file_path.stat().st_size,
            content_hash=content_hash,
            chunk_count=chunk_count,
        )

        return document

    except HTTPException:
        raise

    except Exception:
        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Document upload failed.",
        )

    finally:
        file.file.close()
        
        
@router.post(
    "/crawl",
    status_code=status.HTTP_201_CREATED,
)
async def crawl_document(
        request: CrawlDocumentRequest,
    ) -> dict:
        try:
            document = await web_crawl_service.crawl_and_ingest(
                str(request.url)
            )

            return document

        except DuplicateWebDocumentError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "message": "Web content already exists.",
                    "document_id": exc.document["document_id"],
                    "source": exc.document["original_filename"],
                },
            ) from exc

        except WebCrawlError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(exc),
            ) from exc

        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Web crawling failed: {exc}",
            ) from exc
        
        
        
@router.get(
    "/{document_id}",
    status_code=status.HTTP_200_OK,
)
def get_document(document_id: str) -> dict:
    document = document_service.get_document(document_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    return document



@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_document(document_id: str) -> None:
    document = document_service.get_document(document_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    file_path = UPLOADS_DIR / document["stored_filename"]

    try:
        vector_store.delete_by_document_id(document_id)

        file_path.unlink(missing_ok=True)

        deleted_document = document_service.delete_document(
            document_id
        )

        if deleted_document is None:
            raise RuntimeError(
                "Document metadata could not be deleted."
            )

    except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Document deletion failed.",
            ) from exc
    
    # except Exception as exc:
    #  raise HTTPException(
    #     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #     detail=f"Document deletion failed: {exc}",
    # ) from exc
    
    
    
