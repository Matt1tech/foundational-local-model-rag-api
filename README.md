# Foundational Local Model RAG API

A lightweight, framework-light Retrieval-Augmented Generation system that runs locally using FastAPI, Ollama, and Qdrant.

Foundational RAG lets users upload documents or crawl web pages, convert them into searchable knowledge, and ask questions grounded in the indexed content. The system includes a REST API and a responsive browser interface for document ingestion, website crawling, document management, semantic retrieval, source inspection, and local AI answer generation.

The core RAG pipeline is implemented directly from focused components rather than hidden behind a large orchestration framework. Document loading, text chunking, embedding generation, vector storage, retrieval, prompt construction, and answer generation remain explicit and inspectable throughout the codebase.

---

## Why This Project Exists

Many RAG systems begin with high-level orchestration frameworks that combine ingestion, retrieval, prompting, and generation behind abstractions.

Those tools can accelerate development, but they can also make the underlying system difficult to inspect, debug, optimize, or replace.

Foundational RAG takes a framework-light approach:

- No LangChain
- No LlamaIndex
- No cloud AI dependency
- No external hosted vector database required
- No frontend build framework required
- Minimal infrastructure for local execution
- Explicit and replaceable AI components

This keeps the complete retrieval and generation lifecycle visible while maintaining clear architectural boundaries between the API, ingestion pipeline, retrieval system, document management, and local model runtime.

---

## Lightweight by Design

Foundational RAG is designed to demonstrate that a useful local AI knowledge system does not require a large cloud stack or heavy orchestration layer.

The system can run on consumer hardware using compact local models and persistent local storage.

Its lightweight design includes:

- A small FastAPI application
- A static HTML, CSS, and JavaScript interface
- Local inference through Ollama
- Local vector persistence through Qdrant
- Focused Python libraries for file extraction
- Direct service orchestration
- No Node.js frontend toolchain
- No mandatory Docker environment
- No hosted AI API keys
- No managed cloud services

The default `Qwen 2.5 3B` generation model is suitable for machines with limited resources compared with larger local language models.

Actual memory use and response speed depend on:

- The selected Ollama models
- Available CPU or GPU resources
- Document size
- Number of indexed chunks
- Retrieval configuration
- Prompt and response length

The architecture also allows larger generation or embedding models to be introduced without redesigning the complete application.

---

## System Capabilities

### Local AI

- Local language-model inference with Ollama
- Local embedding generation
- Context-grounded answer generation
- Prompt construction using retrieved document context
- Source-aware responses
- No cloud-model dependency

### Document Ingestion

- PDF document ingestion
- DOCX document ingestion
- TXT document ingestion
- Markdown ingestion
- Original file persistence
- File-type validation
- Text extraction through dedicated loaders
- Configurable overlapping text chunks
- One-time document embedding during ingestion

### Web Knowledge Ingestion

- Crawl a web page directly from a URL
- Convert crawled content into Markdown
- Save the generated Markdown locally
- Process crawled pages through the same ingestion pipeline as uploaded files
- Embed crawled content into Qdrant
- Use crawled web content as retrieval context
- Preserve the original URL as document metadata

### Document Management

- Unique document identifiers
- Persistent document metadata
- SHA-256 content hashing
- Duplicate-content detection
- Duplicate upload protection
- Duplicate crawled-page protection
- Document metadata retrieval
- Document deletion
- Associated vector cleanup
- Local source-file cleanup

### Retrieval-Augmented Generation

- Query embedding
- Semantic similarity search
- Configurable top-k retrieval
- Retrieved-context assembly
- Grounded prompt generation
- Local answer generation
- Source filenames or URLs
- Source chunk indexes
- Similarity scores

### REST API

- FastAPI-based HTTP interface
- Pydantic request validation
- Swagger API documentation
- Health monitoring
- Document upload endpoint
- Web crawling endpoint
- Document metadata endpoint
- Document deletion endpoint
- Document-grounded chat endpoint

### Browser Interface

- Responsive local AI dashboard
- Backend connection indicator
- Drag-and-drop file uploads
- File validation
- Website crawling by URL
- Indexed-document session view
- Document deletion controls
- System activity visualization
- Document-grounded chat
- Answer-generation timer
- Progressive answer rendering
- Source inspection cards
- Similarity-score display
- Accessible keyboard interactions
- Responsive desktop and mobile layouts

The frontend is implemented as a single static HTML file with embedded CSS and JavaScript, so it does not require React, Node.js, npm, or a frontend build process.

---

## RAG Processing Flow

The system supports two knowledge-entry paths.

### Uploaded documents

```text
PDF, DOCX, TXT, or Markdown file
                ↓
        File validation
                ↓
       Persistent file storage
                ↓
        SHA-256 content hash
                ↓
       Duplicate-content check
                ↓
          Text extraction
                ↓
       Overlapping text chunks
                ↓
        Embedding generation
                ↓
      Vector storage in Qdrant
                ↓
       Document metadata storage
```

### Crawled web pages

```text
Web page URL
      ↓
Crawl4AI browser crawler
      ↓
Markdown extraction
      ↓
Local .md file storage
      ↓
SHA-256 content hash
      ↓
Duplicate-content check
      ↓
Text chunking
      ↓
Embedding generation
      ↓
Vector storage in Qdrant
      ↓
Document metadata storage
```

### Question answering

```text
User question
      ↓
Question validation
      ↓
Query embedding
      ↓
Semantic search in Qdrant
      ↓
Relevant document chunks
      ↓
Context assembly
      ↓
Grounded prompt construction
      ↓
Local language model
      ↓
Answer with source metadata
```

Documents are processed and embedded once during ingestion. For each new question, the system generates only a query embedding and searches the existing vectors.

The original files are not extracted, chunked, or embedded again for every question.

---

## Architecture Principles

- Keep retrieval and generation responsibilities independent.
- Separate HTTP routing from application services.
- Keep ingestion independent from API transport concerns.
- Process uploaded files and crawled pages through one ingestion pipeline.
- Keep model and vector-database integrations replaceable.
- Use explicit Python code for the core RAG workflow.
- Store document content and metadata alongside vectors.
- Generate document embeddings only during ingestion.
- Generate only one query embedding per question.
- Validate data at application boundaries.
- Detect duplicate content before vector ingestion.
- Clean up partially created resources when operations fail.
- Keep retrieval behavior observable and testable.
- Add abstractions only when they solve a demonstrated need.
- Avoid coupling the application to a high-level AI framework.

---

## Framework-Light RAG

The core pipeline does not depend on orchestration frameworks such as LangChain or LlamaIndex.

The application directly coordinates:

1. Uploaded-file persistence
2. Web-page crawling
3. Markdown generation
4. File-type detection
5. Text extraction
6. Content hashing
7. Duplicate detection
8. Chunk creation
9. Embedding generation
10. Vector persistence
11. Document metadata persistence
12. Query embedding
13. Similarity search
14. Context assembly
15. Prompt construction
16. Local-model generation
17. Source attribution
18. Document and vector deletion

Focused libraries are still used for specific infrastructure responsibilities:

- **FastAPI** exposes the HTTP application.
- **Pydantic** validates request and response data.
- **Ollama** runs local embedding and generation models.
- **Qdrant** stores vectors and performs similarity search.
- **Crawl4AI** retrieves web content and produces Markdown.
- **pypdf** extracts text from PDF files.
- **python-docx** extracts text from Word documents.
- **Pytest** verifies core behavior.

This separation keeps the RAG workflow visible and makes each integration easier to test, replace, profile, or extend.

---

## Technology Stack

| Component           | Technology            |
| ------------------- | --------------------- |
| Language            | Python 3.12+          |
| API framework       | FastAPI               |
| ASGI server         | Uvicorn               |
| Validation          | Pydantic              |
| Local model runtime | Ollama                |
| Generation model    | Qwen 2.5 3B           |
| Embedding model     | EmbeddingGemma        |
| Vector database     | Qdrant                |
| Web crawling        | Crawl4AI              |
| Browser automation  | Playwright            |
| PDF extraction      | pypdf                 |
| DOCX extraction     | python-docx           |
| Frontend            | HTML, CSS, JavaScript |
| Testing             | Pytest                |

---

## Project Structure

```text
foundational-local-model-rag-api/
├── data/
│   ├── documents.json
│   ├── uploads/
│   └── qdrant/
├── docs/
│   ├── architecture/
│   └── planning/
├── frontend/
│   └── index.html
├── src/
│   └── foundational_rag/
│       ├── api/
│       │   ├── chat.py
│       │   ├── documents.py
│       │   ├── health.py
│       │   └── schemas.py
│       ├── core/
│       │   ├── config.py
│       │   ├── container.py
│       │   └── file_utils.py
│       ├── generation/
│       │   ├── generator.py
│       │   └── prompt_builder.py
│       ├── ingestion/
│       │   ├── loaders/
│       │   │   ├── base.py
│       │   │   ├── docx_loader.py
│       │   │   ├── pdf_loader.py
│       │   │   └── txt_loader.py
│       │   ├── chunker.py
│       │   └── file_loader.py
│       ├── retrieval/
│       │   ├── embeddings.py
│       │   ├── qdrant_client.py
│       │   ├── retriever.py
│       │   └── vector_store.py
│       ├── services/
│       │   ├── document_service.py
│       │   ├── ingestion_service.py
│       │   ├── rag_service.py
│       │   └── web_crawl_service.py
│       └── main.py
├── tests/
├── .gitignore
├── pyproject.toml
└── README.md
```

The exact structure may evolve as additional memory, evaluation, and model-routing capabilities are introduced.

---

# Installation

## Prerequisites

Install the following before running the project:

- Python 3.12 or later
- Ollama
- Git

Crawl4AI and its browser dependencies are installed through the Python environment during the setup steps below.

---

## 1. Clone the Repository

```bash
git clone <repository-url>
cd foundational-local-model-rag-api
```

Replace `<repository-url>` with the repository URL.

---

## 2. Create a Virtual Environment

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Linux or macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install the Project

Install the application and development dependencies:

```powershell
pip install -e ".[dev]"
```

For a production-style installation without development tools:

```powershell
pip install -e .
```

---

## 4. Install Crawl4AI Browser Dependencies

Run the Crawl4AI setup command:

```powershell
crawl4ai-setup
```

When the executable is not available directly, run:

```powershell
python -m crawl4ai.install
```

You can also install Playwright browser files directly when required:

```powershell
python -m playwright install
```

Crawl4AI uses browser automation to render and extract content from web pages.

---

## 5. Download the Ollama Models

Start Ollama and pull the generation model:

```powershell
ollama pull qwen2.5:3b
```

Pull the embedding model:

```powershell
ollama pull embeddinggemma
```

Confirm that the models are installed:

```powershell
ollama list
```

Expected models include:

```text
qwen2.5:3b
embeddinggemma
```

---

# Running the Application

The backend and frontend run as separate local processes.

## 1. Start Ollama

Ensure the Ollama service is running.

You can test it with:

```powershell
ollama list
```

---

## 2. Start the FastAPI Backend

From the project root, with the virtual environment activated:

```powershell
uvicorn foundational_rag.main:app --reload
```

The API runs by default at:

```text
http://127.0.0.1:8000
```

Open Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Open the generated OpenAPI schema:

```text
http://127.0.0.1:8000/openapi.json
```

Check backend health:

```text
http://127.0.0.1:8000/health
```

---

## 3. Start the Browser Interface

From the project root, open a second terminal and run:

```powershell
python -m http.server 5500 --directory frontend
```

Then open:

```text
http://127.0.0.1:5500
```

The frontend expects the FastAPI backend at:

```text
http://127.0.0.1:8000
```

This value is configured in `frontend/index.html`:

```javascript
const API_BASE_URL = "http://127.0.0.1:8000";
```

Change this value when the backend runs on a different host or port.

Using a local HTTP server is recommended instead of opening `index.html` directly through a `file://` URL.

---

## 4. Configure CORS

Because the frontend and backend use different local ports, the FastAPI application must allow the frontend origin.

The backend should allow:

```text
http://127.0.0.1:5500
```

A typical FastAPI configuration is:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Keep production CORS origins restricted to known frontend domains.

---

# Using the Browser Interface

## Upload a Document

1. Open the **Upload file** tab.
2. Select or drag a supported file into the upload area.
3. Click **Upload and index**.
4. Wait for extraction, chunking, embedding, and indexing to complete.
5. Ask questions in the chat panel.

Supported upload formats:

- `.pdf`
- `.docx`
- `.txt`

Markdown files are supported by the ingestion pipeline and are also generated automatically for crawled pages.

---

## Crawl a Web Page

1. Open the **Crawl a URL** tab.
2. Enter a complete HTTP or HTTPS URL.
3. Click **Crawl and index**.
4. Crawl4AI retrieves the page and converts it to Markdown.
5. The Markdown file is saved, chunked, embedded, and indexed.
6. Ask questions about the crawled content through the chat panel.

Example:

```text
https://example.com/article
```

Some websites may reject automated browsers, require authentication, rely on unsupported browser behavior, or block crawling through anti-bot systems.

Only crawl content that you are authorized to access and process.

---

## Ask Questions

After at least one document or web page has been indexed:

1. Enter a question in the chat input.
2. Press `Enter` or click the send button.
3. The system embeds the question.
4. Qdrant retrieves semantically related chunks.
5. The local language model generates an answer from the retrieved context.
6. The UI displays the returned sources and similarity scores.

Use `Shift + Enter` to add a new line without sending the question.

---

## Delete a Document

Indexed documents created during the current browser session appear in the document panel.

Use the delete control to remove a document.

Deletion removes:

- The stored document metadata
- The locally saved source file
- The vectors associated with the document

The current static frontend tracks documents created during the active browser session. Reloading the page clears that client-side session list, but it does not delete documents from the backend.

---

# API Endpoints

| Method   | Endpoint                   | Description                       |
| -------- | -------------------------- | --------------------------------- |
| `GET`    | `/health`                  | Check backend availability        |
| `POST`   | `/documents/upload`        | Upload and ingest a document      |
| `POST`   | `/documents/crawl`         | Crawl and ingest a web page       |
| `GET`    | `/documents/{document_id}` | Retrieve document metadata        |
| `DELETE` | `/documents/{document_id}` | Delete a document and its vectors |
| `POST`   | `/chat`                    | Ask a knowledge-grounded question |

---

## Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "ok"
}
```

---

## Upload and Ingest a Document

```http
POST /documents/upload
```

Content type:

```text
multipart/form-data
```

Supported formats:

- `.pdf`
- `.docx`
- `.txt`

Example response:

```json
{
  "document_id": "868060aa-e663-46bd-b823-a13eaab99fd6",
  "original_filename": "distributed_systems.pdf",
  "stored_filename": "868060aa-e663-46bd-b823-a13eaab99fd6_distributed_systems.pdf",
  "mime_type": "application/pdf",
  "file_size": 128430,
  "content_hash": "9018d785...",
  "chunk_count": 18,
  "uploaded_at": "2026-07-28T12:30:00"
}
```

The exact timestamp and identifier values vary for each document.

---

## Crawl and Ingest a Web Page

```http
POST /documents/crawl
```

Example request:

```json
{
  "url": "https://example.com/article"
}
```

The endpoint:

1. Validates the URL.
2. Crawls the page.
3. Extracts Markdown.
4. Saves the Markdown as a local file.
5. Calculates its SHA-256 content hash.
6. checks for duplicate content.
7. Splits the Markdown into chunks.
8. Generates embeddings.
9. Stores vectors in Qdrant.
10. Creates persistent document metadata.

Example response:

```json
{
  "document_id": "b8114121-52dc-46a1-9d7b-aa74c67053af",
  "original_filename": "https://example.com/article",
  "stored_filename": "b8114121-52dc-46a1-9d7b-aa74c67053af_example_com_article.md",
  "mime_type": "text/markdown",
  "file_size": 28450,
  "content_hash": "65fc820d...",
  "chunk_count": 14,
  "uploaded_at": "2026-07-28T12:35:00"
}
```

---

## Duplicate-Content Response

The system compares SHA-256 hashes before completing ingestion.

When identical content already exists, the API returns:

```http
409 Conflict
```

Example response:

```json
{
  "detail": {
    "message": "Web content already exists.",
    "document_id": "868060aa-e663-46bd-b823-a13eaab99fd6",
    "source": "https://example.com/article"
  }
}
```

Duplicate detection is based on the saved content rather than only the source filename or URL.

---

## Retrieve Document Metadata

```http
GET /documents/{document_id}
```

Example:

```http
GET /documents/868060aa-e663-46bd-b823-a13eaab99fd6
```

The endpoint returns the document metadata stored by the application.

---

## Delete a Document

```http
DELETE /documents/{document_id}
```

Successful deletion returns:

```http
204 No Content
```

The operation removes the document metadata, associated vectors, and stored source file.

---

## Ask a Knowledge-Grounded Question

```http
POST /chat
```

Example request:

```json
{
  "question": "What conditions are required for a distributed deadlock?"
}
```

Example response:

```json
{
  "answer": "A distributed deadlock requires...",
  "sources": [
    {
      "source": "distributed_systems.pdf",
      "chunk_index": 4,
      "score": 0.87
    }
  ]
}
```

The answer is generated using context returned by semantic retrieval.

---

# Document and Query Processing

## Ingestion

Documents are embedded only when they enter the knowledge base:

```text
Upload or crawl
      ↓
Store source content
      ↓
Calculate content hash
      ↓
Check for duplicates
      ↓
Extract text
      ↓
Create overlapping chunks
      ↓
Generate embeddings
      ↓
Persist vectors in Qdrant
      ↓
Store document metadata
```

## Retrieval

For every question, the system embeds only the question:

```text
Question
    ↓
Generate query embedding
    ↓
Search stored vectors
    ↓
Retrieve relevant chunks
    ↓
Build grounded prompt
    ↓
Generate local answer
```

This avoids repeating document extraction and embedding for every request.

---

# Running Tests

Run the complete test suite:

```powershell
pytest -v
```

The test suite covers core pipeline behavior such as:

- Chunk creation
- Chunk overlap
- Blank-text handling
- Chunk configuration validation
- TXT document loading
- Unsupported-file validation
- Prompt construction
- Empty-question validation
- Semantic retrieval mapping
- Ingestion orchestration
- Unique vector-point identifiers
- Document metadata behavior
- Duplicate detection
- Document deletion behavior

Tests can use lightweight fake components where active Ollama or Qdrant integrations are unnecessary.

---

# Troubleshooting

## Backend Shows as Offline

Confirm that FastAPI is running:

```powershell
uvicorn foundational_rag.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/health
```

Also verify that the frontend `API_BASE_URL` matches the backend address.

---

## Browser Reports a CORS Error

Ensure the FastAPI application allows the frontend origin:

```text
http://127.0.0.1:5500
```

Do not use unrestricted production CORS settings unless the deployment specifically requires them.

---

## Ollama Connection Fails

Verify that Ollama is running:

```powershell
ollama list
```

Confirm that both configured models are installed:

```powershell
ollama pull qwen2.5:3b
ollama pull embeddinggemma
```

---

## Web Crawling Fails

Confirm that Crawl4AI and its browser dependencies are installed:

```powershell
crawl4ai-setup
python -m playwright install
```

On Windows, browser automation must run with an asyncio event loop that supports subprocess creation. The web-crawling service isolates Crawl4AI in an appropriate event loop when necessary.

Some websites may also block automated browsers or require authentication.

---

## The Request Times Out

Local generation and crawling can take longer on CPU-only machines.

Possible improvements include:

- Use a smaller generation model.
- Reduce retrieved chunk count.
- Reduce maximum response length.
- Crawl smaller pages.
- Index smaller documents.
- Increase the frontend request timeout.
- Use GPU acceleration when available.

---

# Current Limitations

- Scanned PDFs requiring OCR are not supported.
- Large files are currently read fully into memory.
- Web crawling processes one requested page rather than an entire website.
- Some websites block browser automation.
- Authenticated web pages are not currently supported.
- Conversation memory is not implemented.
- Retrieval evaluation is not implemented.
- Answer-quality evaluation is not implemented.
- Hybrid keyword and vector retrieval is not implemented.
- Reranking is not implemented.
- Authentication and user isolation are not implemented.
- The static frontend document list is limited to the active browser session.
- Answer rendering is visually progressive, but the backend does not yet provide true token streaming.

---

# Planned Development

- Short-term conversation memory
- Long-term semantic memory
- Persistent document listing in the frontend
- Multi-page website crawling
- Crawl-depth and domain controls
- Retrieval score thresholds
- Retrieval evaluation harness
- Answer-quality evaluation harness
- Hybrid semantic and keyword retrieval
- Result reranking
- Model comparison
- Model routing
- Streaming responses
- Authentication
- Multi-user knowledge spaces
- Background ingestion jobs
- Improved large-file processing
- Docker support
- CI/CD automation
- Production observability
- Agent-based workflows

---

# Development Status

The current implementation provides an end-to-end local AI knowledge system:

```text
Upload or Crawl
       ↓
Store
       ↓
Deduplicate
       ↓
Extract
       ↓
Chunk
       ↓
Embed
       ↓
Index
       ↓
Retrieve
       ↓
Prompt
       ↓
Generate
       ↓
Cite Sources
```

It demonstrates:

- Local model integration
- Explicit RAG orchestration
- Semantic search
- Persistent vector storage
- Multi-format ingestion
- Web-content ingestion
- Document lifecycle management
- Duplicate-content protection
- REST API design
- Service-layer architecture
- Browser-based user interaction
- Framework-light AI engineering

Advanced memory, evaluation, retrieval optimization, model routing, and production deployment capabilities remain planned for later releases.

---

## Author

**Mohamad Albukaai**
Software Engineer specializing in AI

This project showcases practical experience in local AI systems, Retrieval-Augmented Generation, semantic search, API architecture, document ingestion, and lightweight AI application development.

---

## License

MIT License.
