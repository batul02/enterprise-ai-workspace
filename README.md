# Enterprise AI Workspace

A multi-tenant AI knowledge workspace built from scratch to understand and implement the core architecture behind enterprise RAG systems.

The project is being developed incrementally, with an emphasis on:

- clean backend architecture
- authentication and authorization
- workspace-level data isolation
- reliable document ingestion
- custom text chunking
- embedding generation
- vector storage and semantic retrieval
- automated testing
- evaluation-driven RAG development

The goal is not to hide the complexity behind frameworks. Core components such as chunking, embedding flow, retrieval, and vector-store abstraction are implemented explicitly so that the underlying system can be understood and explained.

---

## Project Status

### Completed

- [x] User registration
- [x] JWT authentication
- [x] Authenticated `/me` endpoint
- [x] Workspace creation
- [x] Workspace CRUD APIs
- [x] Workspace-level authorization
- [x] PDF upload
- [x] Local document storage
- [x] Document metadata in PostgreSQL
- [x] PDF text extraction
- [x] Extraction error handling
- [x] Custom text chunking
- [x] Chunk overlap
- [x] DocumentChunk model
- [x] Embedding generation
- [x] Qdrant vector storage
- [x] Document processing pipeline
- [x] Semantic search
- [x] Workspace-filtered vector retrieval
- [x] Automated tests for major components
- [x] Retrieval evaluation
- [x] LangChain orchestration

### In Progress

- [ ] Similarity threshold tuning
- [ ] Page-aware chunk metadata
- [ ] RAG answer generation
- [ ] Source citations
- [ ] Conversation / chat API
- [ ] Background document processing

### Planned

- [ ] DOCX ingestion
- [ ] PPTX ingestion
- [ ] Pluggable document parsers
- [ ] Cloud object storage
- [ ] Async processing
- [ ] Hybrid search
- [ ] Reranking
- [ ] RAG evaluation metrics
- [ ] Observability
- [ ] Production deployment


# Architecture

The current system follows a layered architecture:

                    Client
                      │
                      ▼
                FastAPI API
                      │
             Authentication
                      │
             Authorization
                      │
                      ▼
                 Services
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
   PostgreSQL      Qdrant       File Storage
        │             │
        │             │
        └───────┬─────┘
                │
                ▼
             RAG Layer

The document ingestion pipeline is:

```text
Upload PDF
    │
    ▼
Save File
    │
    ▼
Extract Text
    │
    ▼
Chunk Text
    │
    ▼
Store Document Chunks
    │
    ▼
Generate Embeddings
    │
    ▼
Store Vectors in Qdrant
    │
    ▼
Ready for Semantic Search
```

The retrieval pipeline is:

```text
User Query
    │
    ▼
Query Embedding
    │
    ▼
Workspace Filter
    │
    ▼
Qdrant Similarity Search
    │
    ▼
Top-K Chunks
    │
    ▼
Chunk + Metadata + Score
```

---

# Core Concepts

## Multi-Tenant Workspaces

A workspace acts as a logical isolation boundary.

For example:

```text
Workspace A
├── HR documents
├── Salary policies
└── Leave policies

Workspace B
├── Finance documents
├── Loan policies
└── Interest rate policies
```

Documents and vectors are associated with a workspace.

Retrieval is always filtered by `workspace_id` so that a search in Workspace A cannot return vectors belonging to Workspace B.

---

|                      | Custom RAG              | LangChain Runnable   |
| -------------------- | ----------------------- | -------------------- |
| Retrieval            | Your `RetrievalService` | LangChain Retriever  |
| Prompt               | Your `PromptService`    | `PromptTemplate`     |
| LLM                  | Your `LLMService`       | `ChatOllama`         |
| Orchestration        | Explicit Python         | Runnable composition |
| Debugging            | Explicit                | Chain components     |
| Framework dependency | Low                     | Higher               |


---

                    DONE
                      │
                      ▼
              Embedding Adapter
                      │
                      ▼
             QdrantVectorStore
                      │
                      ▼
                 Retriever
                      │
                      ▼
              PromptTemplate
                      │
                      ▼
                ChatOllama
                      │
                      ▼
             RAG Orchestration
                      │
                      ▼
             ┌────────────────┐
             │ NEXT: Runnable │
             │    Chain       │
             └────────────────┘

# Authentication

The API uses JWT-based authentication.

Authentication is enforced on protected endpoints.

Current authentication flow:

```text
Register
   │
   ▼
User
   │
   ▼
Login
   │
   ▼
JWT Access Token
   │
   ▼
Authenticated API Requests
```

Authentication tests currently cover:

* valid registration
* duplicate email
* valid login
* invalid password
* missing token
* invalid token
* valid `/me` request

---

# Workspaces

Workspace APIs:

```text
POST   /api/v1/workspaces
GET    /api/v1/workspaces
GET    /api/v1/workspaces/{id}
PUT    /api/v1/workspaces/{id}
DELETE /api/v1/workspaces/{id}
```

Workspace ownership is enforced at the API/service layer.

A user cannot access another user's workspace.

---

# Document Ingestion

Current document APIs:

```text
POST   /api/v1/workspaces/{id}/documents
GET    /api/v1/workspaces/{id}/documents
GET    /api/v1/documents/{id}
DELETE /api/v1/documents/{id}
```

Uploaded files are currently stored locally:

```text
storage/
└── workspace-id/
    └── file.pdf
```

The storage layer is intentionally separated so that local storage can later be replaced by:

* S3
* OCI Object Storage
* another object storage provider

without rewriting document-processing logic.

---

# PDF Processing

PDF parsing is isolated from database logic.

Current pipeline:

```text
PDF
 │
 ▼
PDF Parser
 │
 ├── page count
 ├── extracted text
 └── parsing errors
```

The parser handles failure cases such as:

* corrupted PDFs
* empty PDFs
* invalid files
* unsupported content
* parsing failures

Extraction state is stored with the document.

---

# Chunking

The project uses a custom chunking implementation instead of LangChain's text splitters.

This is intentional.

The chunking service is responsible for:

* splitting extracted text
* respecting chunk size
* preserving overlap
* preferring natural text boundaries
* maintaining character positions
* preserving chunk ordering

The implementation prefers:

```text
Paragraph / newline boundary
        ↓
Sentence boundary
        ↓
Word boundary
        ↓
Hard character split
```

This makes the chunking process explicit and easier to reason about.

---

# Document Chunks

Each document is divided into `DocumentChunk` records.

Conceptually:

```text
Document
   │
   ├── Chunk 0
   ├── Chunk 1
   ├── Chunk 2
   └── ...
```

Chunk metadata currently includes information such as:

* document ID
* chunk index
* content
* start character
* end character
* character count
* embedding status

This metadata will later support retrieval debugging and source citations.

---

# Embeddings

Document chunks are converted into dense vectors using a shared embedding service.

Current model:

```text
BAAI/bge-small-en-v1.5
```

The same embedding model is used for:

```text
Document chunks
      │
      ▼
Embedding model
      │
      ▼
Vector


User query
      │
      ▼
Same embedding model
      │
      ▼
Query vector
```

Using the same embedding model ensures that document and query vectors exist in the same embedding space.

The embedding implementation is isolated behind an `EmbeddingService` so the model can be changed later without changing retrieval logic.

---

# Vector Database

Qdrant is currently used as the vector database.

The project uses a vector-store abstraction rather than coupling application services directly to Qdrant APIs.

Conceptually:

```text
Retrieval Service
       │
       ▼
Vector Store
       │
       ▼
Qdrant
```

The vector store is responsible for:

* collection creation
* vector insertion
* vector upsert
* vector search
* vector deletion
* metadata filtering

Each vector stores metadata such as:

```text
document_id
workspace_id
chunk_id
chunk_index
filename
```

This allows retrieved vectors to be traced back to their source document.

---

# Semantic Search

Semantic search follows:

```text
Query
  │
  ▼
EmbeddingService
  │
  ▼
Query Vector
  │
  ▼
Qdrant
  │
  ├── workspace filter
  │
  └── similarity search
  │
  ▼
Top-K chunks
```

Current search endpoint:

```text
POST /api/v1/workspaces/{workspace_id}/search
```

Example request:

```json
{
  "query": "What is the personal loan interest rate?",
  "top_k": 5
}
```

Example response:

```json
{
  "query": "What is the personal loan interest rate?",
  "results": [
    {
      "chunk_id": 15,
      "content": "Personal loan interest rates...",
      "score": 0.91,
      "document_id": 4,
      "page_number": 4,
      "filename": "loan_policy.pdf"
    }
  ]
}
```

Search is workspace-scoped.

A query against Workspace A must never retrieve vectors belonging to Workspace B.

---

## RAG Pipeline

The current document processing and retrieval pipeline is:

Upload PDF
   ↓
PDF Text Extraction
   ↓
Custom Text Chunking
   ↓
Embedding Generation
   ↓
Qdrant Vector Store
   ↓
Semantic Search
   ↓
Top-K Relevant Chunks

The project intentionally implements the core chunking, embedding, retrieval,
and vector-store abstractions without relying on LangChain.

---

# Retrieval Thresholds

Similarity thresholds are configurable rather than hardcoded to an arbitrary value.

The correct threshold depends on:

* embedding model
* vector distance configuration
* document characteristics
* chunking strategy
* query distribution

Threshold selection will therefore be based on retrieval experiments rather than assumptions.

---

# Testing

Testing is treated as part of the architecture rather than an afterthought.

Current test areas include:

```text
tests/
├── test_auth.py
├── test_workspace.py
├── test_document.py
├── test_chunking_service.py
├── test_document_processor.py
├── test_embedding_service.py
├── test_qdrant_store.py
└── test_search.py
```

Tests cover areas such as:

### Authentication

* registration
* duplicate users
* login
* invalid credentials
* JWT validation

### Workspace Security

* workspace ownership
* unauthorized access
* cross-user access

### Document Processing

* valid PDF
* corrupted PDF
* empty PDF
* invalid MIME type
* document deletion

### Chunking

* small text
* large text
* empty text
* overlap
* chunk ordering
* natural sentence boundaries

### Embeddings

* embedding generation
* empty chunks
* embedding validation

### Vector Store

* vector insertion
* duplicate upsert
* vector deletion
* workspace filtering

### Retrieval

* relevant results
* Top-K behavior
* metadata
* workspace isolation
* empty queries
* invalid Top-K
* empty result sets

Run the complete test suite with:

```bash
pytest -v
```

---

# Project Structure

The backend is organized around responsibilities rather than putting everything inside API routes.

```text
enterprise-ai-workspace/
│
├── backend/
│   │
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── constants.py
│   │   │   └── dependencies.py
│   │   │
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── workspace.py
│   │   │   ├── document.py
│   │   │   └── document_chunk.py
│   │   │
│   │   ├── schemas/
│   │   │
│   │   ├── services/
│   │   │   ├── document_service.py
│   │   │   ├── pdf_parser.py
│   │   │   ├── chunking_service.py
│   │   │   ├── embedding_service.py
│   │   │   └── retrieval_service.py
│   │   │
│   │   ├── processors/
│   │   │   └── document_processor.py
│   │   │
│   │   └── vectorstore/
│   │       └── qdrant_store.py
│   │
│   ├── alembic/
│   │
│   ├── tests/
│   │
│   ├── Dockerfile
│   ├── requirements.txt
│   └── alembic.ini
│
├── docs/
│   └── retrieval_evaluation.md
│
├── docker-compose.yml
└── README.md
```

The exact structure will evolve as the system grows.

---

# Infrastructure

Current infrastructure includes:

* PostgreSQL
* Qdrant
* Docker Compose
* FastAPI backend

The goal is to keep infrastructure replaceable and application services loosely coupled to infrastructure-specific implementations.

---

# Running Locally

## 1. Clone the repository

```bash
git clone https://github.com/batul02/enterprise-ai-workspace.git

cd enterprise-ai-workspace
```

## 2. Start infrastructure

```bash
docker compose up -d
```

This starts the services defined in `docker-compose.yml`.

Check running containers:

```bash
docker ps
```

## 3. Create the Python environment

```bash
cd backend

python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 5. Run database migrations

```bash
alembic upgrade head
```

## 6. Start the API

```bash
uvicorn app.main:app --reload
```

The API can then be accessed locally through the FastAPI server.

---

# API Documentation

FastAPI provides interactive API documentation during local development.

Once the server is running, use:

```text
/docs
```

for Swagger UI.

---

# Development Philosophy

This project is being built incrementally instead of starting with a large RAG framework.

The implementation intentionally focuses on understanding the underlying system:

```text
Authentication
      ↓
Authorization
      ↓
Workspace isolation
      ↓
Document ingestion
      ↓
Text extraction
      ↓
Chunking
      ↓
Embeddings
      ↓
Vector storage
      ↓
Semantic retrieval
      ↓
Evaluation
      ↓
RAG generation
```

Frameworks such as LangChain may be evaluated later, but core components are being implemented explicitly first.

The goal is to understand what the abstractions are doing rather than treating them as black boxes.

---

# Design Principles

## Separation of concerns

API routes should coordinate requests rather than contain business logic.

```text
API
 ↓
Service
 ↓
Infrastructure
```

## Reusability

The document pipeline should make it possible to add additional document types without rewriting the entire ingestion system.

For example:

```text
PDF Parser
DOCX Parser
PPTX Parser
     │
     ▼
Document Processor
     │
     ▼
Chunking
     │
     ▼
Embedding
     │
     ▼
Vector Store
```

## Replaceable infrastructure

Services should depend on abstractions where practical.

For example:

```text
RetrievalService
      ↓
VectorStore
      ↓
Qdrant
```

This leaves room for another vector database later.

## Security by design

Workspace isolation is enforced at multiple levels:

```text
Authenticated User
        ↓
Workspace Authorization
        ↓
workspace_id filtering
        ↓
Vector Retrieval
```

---

# Roadmap

The planned evolution of the system is:

```text
Phase 1
Authentication + Workspaces
        ✓

Phase 2
Document Upload + Storage
        ✓

Phase 3
PDF Extraction
        ✓

Phase 4
Custom Chunking
        ✓

Phase 5
Embeddings + Qdrant
        ✓

Phase 6
Semantic Search
        ✓

Phase 7
Retrieval Evaluation
        ✓

Phase 8
RAG Generation
        →

Phase 9
Citations + Source Attribution
        →

Phase 10
Hybrid Search + Reranking
        →

Phase 11
Async Processing
        →

Phase 12
Production Hardening
```

---

# Current Focus

The current focus is **retrieval quality**.

Before adding an LLM generation layer, the system will be evaluated on whether the correct chunks are retrieved for representative questions.

## Retrieval Evaluation

An initial evaluation was performed using 10 questions against the NIST AI
Risk Management Framework (AI RMF 1.0).

| Metric | Result |
|---|---:|
| Questions | 10 |
| Top-1 Relevant | 7/10 |
| Top-3 Relevant | 10/10 |
| Top-5 Relevant | 10/10 |
| Top-1 Accuracy | 70% |
| Top-3 Accuracy | 100% |
| Top-5 Accuracy | 100% |
| Average Best Similarity Score | 0.8200 |

The initial results indicate that the retrieval system has strong recall within
the Top-3 and Top-5 results, while Top-1 ranking remains an area for improvement.

Detailed evaluation results are available in:

`docs/retrieval_evaluation.md`

---

# License

License information will be added as the project matures.

```

### One change I'd make before you commit this

I would **not claim things that aren't actually in the repository yet**. For example, if your current `DocumentChunk` does not have `page_number`, the README should not say that it currently stores page numbers. Same with any endpoint or folder that we have discussed but haven't actually committed yet.

Your repository is currently public and the GitHub page shows the README is only one line, so this is a good point to establish a proper project narrative before the RAG generation layer gets added. :contentReference[oaicite:1]{index=1}

Also, I deliberately wrote the README as a **living document** rather than a finished-project README. As we add reranking, citations, evaluation, chat, async processing, etc., we can update the relevant sections instead of rewriting the whole thing.

:contentReference[oaicite:2]{index=2}

```

[1]: https://github.com/batul02/enterprise-ai-workspace/blob/main/README.md "enterprise-ai-workspace/README.md at main · batul02/enterprise-ai-workspace · GitHub"
