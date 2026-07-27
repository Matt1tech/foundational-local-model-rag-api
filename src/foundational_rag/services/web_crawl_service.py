import asyncio
import re
import sys
from typing import Any
from urllib.parse import urlparse
from uuid import uuid4

from crawl4ai import AsyncWebCrawler

from foundational_rag.core.config import UPLOADS_DIR
from foundational_rag.core.file_utils import calculate_file_hash
from foundational_rag.services.document_service import DocumentService
from foundational_rag.services.ingestion_service import IngestionService


class DuplicateWebDocumentError(Exception):
    """Raised when crawled content is already indexed."""

    def __init__(self, document: dict) -> None:
        self.document = document

        super().__init__(
            "Web content already exists as document "
            f"{document['document_id']}."
        )


class WebCrawlError(Exception):
    """Raised when a webpage cannot be crawled."""


class WebCrawlService:
    """Crawls webpages and indexes their Markdown content."""

    def __init__(
        self,
        ingestion_service: IngestionService,
        document_service: DocumentService,
    ) -> None:
        self.ingestion_service = ingestion_service
        self.document_service = document_service

    async def crawl_and_ingest(self, url: str) -> dict:
        """
        Crawl a webpage, save it as Markdown, ingest its chunks,
        and store its document metadata.
        """

        document_id = str(uuid4())

        stored_filename = self._create_filename(
            url=url,
            document_id=document_id,
        )

        UPLOADS_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path = UPLOADS_DIR / stored_filename

        try:
            markdown = await self._crawl(url)

            file_path.write_text(
                markdown,
                encoding="utf-8",
            )

            content_hash = calculate_file_hash(file_path)

            existing_document = (
                self.document_service.get_document_by_hash(
                    content_hash
                )
            )

            if existing_document is not None:
                raise DuplicateWebDocumentError(
                    existing_document
                )

            chunk_count = self.ingestion_service.ingest(
                file_path=file_path,
                document_id=document_id,
            )

            document = self.document_service.create_document(
                document_id=document_id,
                original_filename=url,
                stored_filename=stored_filename,
                mime_type="text/markdown",
                file_size=file_path.stat().st_size,
                content_hash=content_hash,
                chunk_count=chunk_count,
            )

            return document

        except Exception:
            file_path.unlink(missing_ok=True)
            raise

    async def _crawl(self, url: str) -> str:
        """
        Run Crawl4AI inside a separate thread.

        On Windows, Playwright needs a ProactorEventLoop because it
        launches a browser using asyncio subprocesses.
        """

        return await asyncio.to_thread(
            self._crawl_in_separate_loop,
            url,
        )

    def _crawl_in_separate_loop(self, url: str) -> str:
        """Create an isolated event loop for Crawl4AI."""

        if sys.platform == "win32":
            loop = asyncio.ProactorEventLoop()
        else:
            loop = asyncio.new_event_loop()

        try:
            asyncio.set_event_loop(loop)

            result = loop.run_until_complete(
                self._run_crawler(url)
            )

            if not result.success:
                raise WebCrawlError(
                    result.error_message
                    or "The webpage could not be crawled."
                )

            markdown = self._extract_markdown(
                result.markdown
            ).strip()

            if not markdown:
                raise WebCrawlError(
                    "The crawler returned empty Markdown."
                )

            return markdown

        finally:
            loop.run_until_complete(
                loop.shutdown_asyncgens()
            )

            loop.close()

            asyncio.set_event_loop(None)

    @staticmethod
    async def _run_crawler(url: str) -> Any:
        """Run Crawl4AI and return its crawl result."""

        async with AsyncWebCrawler() as crawler:
            return await crawler.arun(
                url=url,
            )

    @staticmethod
    def _extract_markdown(
        markdown_result: object,
    ) -> str:
        """
        Extract Markdown while supporting different Crawl4AI
        result representations.
        """

        raw_markdown = getattr(
            markdown_result,
            "raw_markdown",
            None,
        )

        if isinstance(raw_markdown, str):
            return raw_markdown

        if isinstance(markdown_result, str):
            return markdown_result

        return str(markdown_result)

    @staticmethod
    def _create_filename(
        url: str,
        document_id: str,
    ) -> str:
        """Create a safe and unique Markdown filename."""

        parsed_url = urlparse(url)

        name = (
            f"{parsed_url.netloc}"
            f"{parsed_url.path}"
        )

        name = name.strip("/") or "index"

        safe_name = re.sub(
            r"[^a-zA-Z0-9_-]+",
            "_",
            name,
        ).strip("_")

        safe_name = safe_name[:100] or "index"

        return f"{document_id}_{safe_name}.md"