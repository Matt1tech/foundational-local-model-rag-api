from ollama import Client

from foundational_rag.core.config import (
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    LLM_MODEL,
    TOP_K,
    VECTOR_SIZE,
)
from foundational_rag.generation.generator import ResponseGenerator
from foundational_rag.generation.prompt_builder import PromptBuilder
from foundational_rag.ingestion.chunker import TextChunker
from foundational_rag.ingestion.file_loader import FileLoader
from foundational_rag.retrieval.embeddings import EmbeddingService
from foundational_rag.retrieval.qdrant_client import create_qdrant_client
from foundational_rag.retrieval.retriever import Retriever
from foundational_rag.retrieval.vector_store import VectorStore
from foundational_rag.services.ingestion_service import IngestionService
from foundational_rag.services.rag_service import RagService
from foundational_rag.services.document_service import DocumentService

from foundational_rag.services.web_crawl_service import (
    WebCrawlService,
)


ollama_client = Client()

qdrant_client = create_qdrant_client()
document_service = DocumentService()

vector_store = VectorStore(
    client=qdrant_client,
    collection_name=COLLECTION_NAME,
    vector_size=VECTOR_SIZE,
)
vector_store.create_collection()

embedding_service = EmbeddingService(
    model_name=EMBEDDING_MODEL,
    client=ollama_client,
)

response_generator = ResponseGenerator(
    model_name=LLM_MODEL,
    client=ollama_client,
)

file_loader = FileLoader()

chunker = TextChunker()

retriever = Retriever(
    embedding_service=embedding_service,
    vector_store=vector_store,
    top_k=TOP_K,
)

prompt_builder = PromptBuilder()

ingestion_service = IngestionService(
    file_loader=file_loader,
    chunker=chunker,
    embedding_service=embedding_service,
    vector_store=vector_store,
)


web_crawl_service = WebCrawlService(
    ingestion_service=ingestion_service,
    document_service=document_service,
)

rag_service = RagService(
    retriever=retriever,
    prompt_builder=prompt_builder,
    generator=response_generator,
)


