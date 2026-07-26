# Foundational Local Model RAG API

A modular Retrieval-Augmented Generation API that runs locally using Ollama, Qdrant and FastAPI.

The project implements the core RAG pipeline directly from foundational components instead of relying on a high-level orchestration framework. Document ingestion, text chunking, embedding generation, vector storage, semantic retrieval, prompt construction and answer generation remain explicit within the codebase.

## Why This Project Exists

Many RAG implementations begin with frameworks that combine several operations behind abstractions. Those tools can accelerate development, but they can also make the underlying retrieval and generation flow difficult to inspect.

This repository takes a framework-light approach to demonstrate how the main RAG components communicate:

```text
Document
   ↓
Text extraction
   ↓
Chunking
   ↓
Embedding generation
   ↓
Vector storage
   ↓
User question
   ↓
Query embedding
   ↓
Semantic retrieval
   ↓
Context construction
   ↓
Local language model
   ↓
Grounded answer
```

The API is designed with clear module boundaries so that individual components can later be evaluated, replaced or extended independently.

## Core Capabilities

- Local language-model inference
- Local embedding generation
- Document ingestion and text chunking
- Vector storage with Qdrant
- Semantic similarity retrieval
- Context-grounded answer generation
- REST API built with FastAPI
- Source metadata and retrieval scores
- Automated tests
- Retrieval and answer evaluation
- Extensible architecture for memory and model routing

## Technology Stack

| Component           | Technology     |
| ------------------- | -------------- |
| Language            | Python         |
| API                 | FastAPI        |
| Local model runtime | Ollama         |
| Generation model    | Qwen 2.5 3B    |
| Embedding model     | EmbeddingGemma |
| Vector database     | Qdrant         |
| Validation          | Pydantic       |
| Testing             | Pytest         |

## Architecture Principles

The project follows several engineering principles:

- Keep retrieval and generation logic independent.
- Separate API concerns from AI orchestration.
- Keep model and database integrations replaceable.
- Use explicit Python code for the core RAG workflow.
- Store document text and metadata alongside vectors.
- Validate external inputs at system boundaries.
- Make retrieval behavior observable and testable.
- Add abstractions only when they solve a demonstrated need.

## Framework-Light RAG

The core RAG pipeline does not depend on orchestration frameworks such as LangChain or LlamaIndex.

This is an intentional architectural decision for the foundational implementation. The pipeline directly coordinates:

1. Document loading
2. Text normalization
3. Chunk creation
4. Embedding generation
5. Vector persistence
6. Query embedding
7. Similarity search
8. Context assembly
9. Prompt construction
10. Local-model generation

Focused libraries are still used for their intended infrastructure responsibilities:

- Ollama runs local embedding and generation models.
- Qdrant stores vectors and performs similarity search.
- FastAPI exposes application capabilities through HTTP.
- Pydantic validates API data.

This separation makes the complete data flow visible and creates a baseline for evaluating higher-level frameworks later.

## Project Structure

```text
foundational-local-model-rag-api/
├── data/
│   ├── documents/
│   └── qdrant/
├── docs/
│   ├── architecture/
│   └── planning/
├── src/
│   └── foundational_rag/
│       ├── api/
│       ├── core/
│       ├── generation/
│       ├── ingestion/
│       ├── retrieval/
│       └── services/
├── tests/
├── .gitignore
├── pyproject.toml
└── README.md
```

## Development Status

The project is under active development.

The initial implementation will establish a complete local RAG pipeline before introducing advanced capabilities such as conversational memory, hybrid retrieval, reranking, model routing and agentic workflows.

## Planned Milestones

- Repository and application foundation
- Document ingestion pipeline
- Embedding and vector-storage pipeline
- Semantic retrieval
- Context-grounded generation
- FastAPI integration
- Automated testing
- Evaluation harness
- Short-term conversation memory
- Long-term memory
- Retrieval improvements and model routing

## License

MIT License.
