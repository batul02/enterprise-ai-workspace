

# Today's Architecture

```text
Client
    │
    ▼
Upload Endpoint
    │
    ▼
Document Service
    │
    ├── Storage Service
    ├── PDF Parser
    └── PostgreSQL
```


---

# Step 0 — Design

## Feature

PDF Processing Pipeline

---

## Problem

Uploaded PDFs should be parsed immediately so that their text is available for downstream AI features like chunking, embeddings, semantic search, and RAG.

---

## User Story

As a user,

I want my uploaded PDF to be processed automatically,

So that it becomes searchable and ready for AI analysis.

---

## Pipeline

```text
Upload PDF
      │
      ▼
Validate PDF
      │
      ▼
Save File
      │
      ▼
Extract Text
      │
      ▼
Store Metadata
      │
      ▼
Store Extracted Text
      │
      ▼
Ready for Chunking
```

---

## New Service

```text
app/
└── services/
      pdf_parser.py
```

Single responsibility:

* Read PDF
* Extract text page by page
* Count pages
* Handle parsing failures
* Return structured result

It **must not**:

* Save to database
* Save files
* Know anything about FastAPI

---

## Database

I would extend `Document`.

```text
Document
────────────

id
workspace_id
filename
original_filename
content_type
file_size
storage_path
uploaded_by

extraction_status
page_count
extracted_text
processing_error

created_at
```

---

## Status

Instead of boolean:

```text
parsed = true
```

I'd use:

```text
PENDING
PROCESSING
COMPLETED
FAILED
```

Why?

Because later you'll introduce background workers.

The same states still work.

---

## Error Cases

Handle:

✅ Corrupted PDF

✅ Empty PDF

✅ Password protected PDF

✅ Wrong MIME type

Gracefully.

Don't let exceptions crash the endpoint.

---

# Step 1 — Install Parser

I recommend **PyMuPDF**.

```bash
pip install pymupdf
```

It's:

* faster than pypdf
* excellent text extraction
* supports page count
* supports images later

---

# Step 2 — Extend Document Model

I would add:

```python
extraction_status
```

```python
page_count
```

```python
extracted_text
```

```python
processing_error
```

Why?

### page_count

Later UI:

```text
HR Policy

25 pages
```

---

### extracted_text

Temporary storage.

Eventually:

```text
Extracted Text

↓

Chunking

↓

Embeddings

↓

Vector DB
```

---

### processing_error

Instead of:

```text
500 Internal Server Error
```

Store:

```text
Password protected PDF
```

or

```text
Corrupted file
```

---

# Step 3 — PDF Parser Service

```text
services/

pdf_parser.py
```

Functions I'd build:

```text
parse_pdf()

↓

returns

PDFParseResult
```

Instead of returning:

```python
str
```

I'd return an object.

For example:

```text
text

page_count

status

error
```

Much easier to extend later.

---

# Step 4 — Upload Flow

Instead of today's flow:

```text
Upload

↓

Save File

↓

Database
```

Tomorrow becomes:

```text
Upload

↓

Save File

↓

Parse PDF

↓

Update Document

↓

Return Response
```

---

# Step 5 — Future Pipeline

You're actually building the first half of RAG.

```text
PDF

↓

Parser

↓

Extracted Text

↓

Chunker

↓

Embeddings

↓

Vector DB

↓

Retriever

↓

LLM
```

---

# Coding Order


### ✅ Step 1

Document model migration

---

### ✅ Step 2

PDF parser service

---

### ✅ Step 3

Update document service

---

### ✅ Step 4

Update upload endpoint

---

### ✅ Step 5

Tests

---


1. **Extend `Document` model + Alembic migration**
2. **Implement `pdf_parser.py`**
3. **Integrate parsing into `document_service.py`**
4. **Update upload endpoint**
5. **Write tests**

This order keeps each layer buildable and testable before the next one depends on it.
