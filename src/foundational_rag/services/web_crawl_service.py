import asyncio
import logging
import re
import sys
from typing import Any
from urllib.parse import urlparse
from uuid import uuid4

from crawl4ai import (
    AsyncWebCrawler,
    CacheMode,
    CrawlerRunConfig,
)
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

from foundational_rag.core.config import UPLOADS_DIR
from foundational_rag.core.file_utils import calculate_file_hash
from foundational_rag.services.document_service import DocumentService
from foundational_rag.services.ingestion_service import IngestionService


logger = logging.getLogger(__name__)


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
    """Crawls webpages and indexes their cleaned Markdown content."""

    def __init__(
        self,
        ingestion_service: IngestionService,
        document_service: DocumentService,
    ) -> None:
        self.ingestion_service = ingestion_service
        self.document_service = document_service

    async def crawl_and_ingest(self, url: str) -> dict:
        """
        Crawl a webpage, save its cleaned Markdown, ingest its
        chunks, and store its document metadata.
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

        logger.info(
            "Starting web crawl: document_id=%s url=%s",
            document_id,
            url,
        )

        try:
            markdown = await self._crawl(url)

            logger.info(
                "Web crawl completed: document_id=%s characters=%d",
                document_id,
                len(markdown),
            )

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
                logger.warning(
                    "Duplicate web content detected: "
                    "document_id=%s existing_document_id=%s url=%s",
                    document_id,
                    existing_document["document_id"],
                    url,
                )

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

            logger.info(
                "Web document indexed successfully: "
                "document_id=%s chunks=%d url=%s",
                document_id,
                chunk_count,
                url,
            )

            return document

        except DuplicateWebDocumentError:
            file_path.unlink(missing_ok=True)
            raise

        except Exception:
            file_path.unlink(missing_ok=True)

            logger.exception(
                "Web crawl ingestion failed: "
                "document_id=%s url=%s",
                document_id,
                url,
            )

            raise

    async def _crawl(self, url: str) -> str:
        """
        Run Crawl4AI inside a separate thread.

        On Windows, Playwright needs a ProactorEventLoop because it
        launches a browser using asyncio subprocesses.
        """

        logger.debug("Starting Crawl4AI thread: url=%s", url)

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
                logger.error(
                    "Crawler returned unsuccessful result: url=%s error=%s",
                    url,
                    result.error_message,
                )

                raise WebCrawlError(
                    result.error_message
                    or "The webpage could not be crawled."
                )

            markdown = self._extract_markdown(
                result.markdown
            ).strip()

            if not markdown:
                logger.warning(
                    "Crawler returned empty Markdown: url=%s",
                    url,
                )

                raise WebCrawlError(
                    "The crawler returned no useful Markdown."
                )

            return markdown

        finally:
            loop.run_until_complete(
                loop.shutdown_asyncgens()
            )

            loop.close()

            asyncio.set_event_loop(None)

    @staticmethod
    def _create_crawler_config() -> CrawlerRunConfig:
        """
        Configure Crawl4AI to remove common webpage noise and
        generate filtered Markdown for RAG ingestion.
        """

        content_filter = PruningContentFilter(
            threshold=0.48,
            threshold_type="dynamic",
            min_word_threshold=10,
        )

        markdown_generator = DefaultMarkdownGenerator(
            content_filter=content_filter,
            options={
                "ignore_images": True,
                "body_width": 0,
            },
        )

        return CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            markdown_generator=markdown_generator,
            excluded_tags=[
                "nav",
                "footer",
                "aside",
                "script",
                "style",
                "noscript",
                "form",
            ],
            word_count_threshold=10,
            remove_overlay_elements=True,
            exclude_social_media_links=True,
        )

    @staticmethod
    async def _run_crawler(url: str) -> Any:
        """Run Crawl4AI and return its configured crawl result."""

        crawler_config = WebCrawlService._create_crawler_config()

        async with AsyncWebCrawler() as crawler:
            return await crawler.arun(
                url=url,
                config=crawler_config,
            )

    @staticmethod
    def _extract_markdown(
        markdown_result: object,
    ) -> str:
        """
        Prefer Crawl4AI's filtered Markdown and fall back to
        raw Markdown when filtered content is unavailable.
        """

        fit_markdown = getattr(
            markdown_result,
            "fit_markdown",
            None,
        )

        if isinstance(fit_markdown, str) and fit_markdown.strip():
            return fit_markdown

        raw_markdown = getattr(
            markdown_result,
            "raw_markdown",
            None,
        )

        if isinstance(raw_markdown, str) and raw_markdown.strip():
            return raw_markdown

        if isinstance(markdown_result, str):
            return markdown_result

        return ""

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