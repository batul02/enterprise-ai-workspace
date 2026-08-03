I like doing this exercise before coding. It forces you to think like a backend engineer rather than jumping into implementation.

Here's how I would design this feature.

---

# Feature

Document Upload Service

---

# Problem

Users need a secure way to upload PDF documents into a workspace.

Documents should be organized by workspace, stored safely on disk, and tracked in PostgreSQL so they can later be searched, embedded, summarized, and versioned.

---

# User Story

As a logged-in user,

I want to upload PDF files into my workspace,

So that I can organize and later use them for AI-powered search and Q&A.

---

# API

### Upload Document

```http
POST /api/v1/workspaces/{workspace_id}/documents
```

Uploads one PDF into a workspace.

---

### List Documents

```http
GET /api/v1/workspaces/{workspace_id}/documents
```

Returns all documents belonging to that workspace.

---

### Get Document

```http
GET /api/v1/documents/{document_id}
```

Returns metadata for a single document.

---

### Delete Document

```http
DELETE /api/v1/documents/{document_id}
```

Deletes both:

* database record
* physical file

---

# Database

## Document

```text
Document
--------
id
workspace_id
filename
original_filename
content_type
file_size
storage_path
uploaded_by
created_at
```

---

## Relationships

```text
User
│
├──────────────┐
│              │
│ owns         │ uploads
│              │
▼              ▼
Workspace ───── Document
        1        *
```

One workspace contains many documents.

One user may upload many documents.

---

# Storage

For now we'll store files locally.

```text
storage/

    workspace_1/
        company_policy.pdf
        handbook.pdf

    workspace_2/
        budget.pdf
        invoice.pdf
```

Later this folder will be replaced by:

```text
OCI Object Storage

or

Amazon S3
```

without changing the API layer.

---

# Validation

Allowed file types:

```text
application/pdf
```

Maximum size (initially):

```text
10 MB
```

Reject:

* images
* zip files
* executables
* empty files

---

# Security

Authentication

```text
JWT required
```

Authorization

Only the workspace owner can:

* upload
* list
* view
* delete

Example

```text
Workspace A

Owner → User A
```

User B

```http
POST /workspaces/1/documents
```

↓

```http
403 Forbidden
```

---

# Metadata Flow

```text
Upload PDF

↓

Validate JWT

↓

Validate workspace ownership

↓

Validate PDF

↓

Generate unique filename

↓

Save file

↓

Insert metadata into PostgreSQL

↓

Return DocumentResponse
```

---

# Response Example

```json
{
    "id": 15,
    "workspace_id": 3,
    "original_filename": "HR Policy.pdf",
    "filename": "3b2f94d9.pdf",
    "content_type": "application/pdf",
    "file_size": 582144,
    "created_at": "2026-08-03T18:20:11Z"
}
```

Notice:

The client sees both

```text
HR Policy.pdf
```

and

```text
3b2f94d9.pdf
```

The first is the user's filename.

The second is our internal storage filename.

---

# Project Structure

```text
app/

├── api/
│   └── v1/
│       └── endpoints/
│             documents.py
│
├── services/
│       document_service.py
│
├── models/
│       document.py
│
├── schemas/
│       document.py
│
├── storage/
│       file_storage.py
│
└── utils/
        validators.py
```

Notice I introduced a `storage/` service.

Instead of writing:

```python
file.save(...)
```

inside the endpoint,

we'll eventually call:

```python
storage.save_file(...)
```

That abstraction will make migrating from local storage to S3 or OCI much easier.

---

# Tests

Authentication

* Upload without JWT → 401

Authorization

* Upload to another user's workspace → 403

Upload

* Upload valid PDF → 201

Validation

* Upload non-PDF → 400/415
* Upload empty file → 400
* Upload oversized file → 413 (if size limits are enforced)

Listing

* List workspace documents → 200

Deletion

* Delete existing document → 204
* Delete non-existent document → 404
* Delete another user's document → 403

---

# Future Enhancements

This feature is the foundation for the AI pipeline.

```text
Upload PDF
      │
      ▼
Extract text (PyMuPDF / pdfplumber)
      │
      ▼
OCR (scanned PDFs)
      │
      ▼
Chunking
      │
      ▼
Embeddings
      │
      ▼
Vector Database
      │
      ▼
Semantic Search
      │
      ▼
RAG
```

Other future improvements:

* Multiple file uploads
* Drag & drop uploads
* Document versioning
* File previews
* Duplicate detection
* Virus scanning
* Cloud storage (OCI/S3)
* Background processing with Celery or FastAPI BackgroundTasks
* Document tags and categories

---

## Design Principles

For this feature, I'd keep the same layered architecture you've used so far:

```text
Client
   │
   ▼
API Endpoint
   │
   ▼
Pydantic Schema
   │
   ▼
Document Service
   │
   ├── Storage Service
   ├── Authorization
   └── SQLAlchemy
            │
            ▼
     PostgreSQL + Local Storage
```

This keeps HTTP handling, business logic, storage, and persistence separated. It also means that when you later replace local disk with S3 or OCI Object Storage, you'll mostly update the storage layer rather than rewriting your endpoints or services.


Step 1 — Project Structure

Before writing any code, create these files.

app/
├── api/
│   └── v1/
│       └── endpoints/
│           ├── auth.py
│           ├── workspace.py
│           └── document.py          ← NEW
│
├── models/
│   ├── user.py
│   ├── workspace.py
│   └── document.py                  ← NEW
│
├── schemas/
│   ├── user.py
│   ├── workspace.py
│   └── document.py                  ← NEW
│
├── services/
│   ├── auth_service.py
│   ├── workspace_service.py
│   └── document_service.py          ← NEW
│
├── storage/
│   └── file_storage.py              ← NEW
│
└── utils/
    └── validators.py                ← NEW