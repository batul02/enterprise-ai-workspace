This is where your project starts becoming a **real RAG system**.

I would **not** jump straight into chunking yet. The improvements and the chunking feature should be done in this order because each step supports the next one.

# Day 8 Roadmap

```text
Step 1  Refactor (Constants, Config, Logging, Exceptions)
Step 2  Design DocumentChunk model
Step 3  Alembic migration
Step 4  Chunking Service
Step 5  Update upload pipeline
Step 6  APIs (if needed)
Step 7  Tests
```

---

# Before Coding: Design

## Feature

Document Chunking Pipeline

---

## Problem

Large documents cannot be embedded as one huge block of text.

They must be split into smaller overlapping chunks while preserving enough context for semantic retrieval.

---

## Pipeline

```text
Upload PDF
      │
      ▼
Extract Text
      │
      ▼
Chunk Text
      │
      ▼
Store Chunks
      │
      ▼
Ready for Embeddings
```

---

# Database

Instead of storing chunks inside Document,

create a new table.

```
Document

1
│
│
*
DocumentChunk
```

---

## DocumentChunk

I would use:

```text
id

document_id

chunk_index

content

start_char

end_char

page_number

character_count

created_at
```

Notice I **didn't use `token_count`**.

### Why?

Right now you're **not tokenizing**.

If you store:

```
token_count
```

you'll either

* have to estimate

or

* introduce a tokenizer

Neither is necessary today.

Instead:

```
character_count
```

is deterministic.

Later,

when embeddings arrive,

you can add

```
token_count
```

using `tiktoken`.

---

# Why start/end_char?

These become incredibly useful later.

Suppose the answer is wrong.

You can immediately know:

```
Chunk 14

Characters

4200

↓

5100
```

Much easier for debugging.

---

# Chunk Object

Instead of returning strings,

I'd return:

```python
Chunk(
    chunk_index=0,
    content="...",
    start_char=0,
    end_char=500,
)
```

Exactly like we did for `PDFParseResult`.

---

# Chunking Strategy

We'll implement something interview-friendly.

```
Chunk Size

1000 chars
```

```
Overlap

200 chars
```

Meaning

```
ABCDEFGHIJ
```

becomes

```
Chunk 1

ABCDEFGHIJ
```

```
Chunk 2

HIJKLMNOP
```

Notice

```
HIJ
```

appears in both.

This preserves context.

---

# Service

```
services/

chunking_service.py
```

Functions

```
chunk_text()

↓

List[DocumentChunkData]
```

Again,

no database.

No FastAPI.

Pure logic.

---

# Upload Pipeline

Today's

```
Upload

↓

Save

↓

Parse

↓

Save Document
```

becomes

```
Upload

↓

Save

↓

Parse

↓

Chunk

↓

Save Document

↓

Save Chunks
```

---

# Tests

I like your proposed tests, but I'd structure them like this:

### Parser Tests

* Valid PDF
* Corrupted PDF
* Blank PDF

### Chunking Tests

* Small text (1 chunk)
* Large text (multiple chunks)
* Empty text
* Overlap correctness
* Chunk ordering
* Character count

Keeping parser and chunker tests separate makes failures much easier to diagnose.

---

# Improvements


1. **`constants.py`**

   * `CHUNK_SIZE`
   * `CHUNK_OVERLAP`
   * `MAX_UPLOAD_SIZE`
   * `SUPPORTED_CONTENT_TYPES`
   * `ExtractionStatus`

2. **Custom Exceptions**

   * `PDFParsingException`
   * `InvalidFileException`
   * `WorkspaceAccessException`

3. **Logging**

   * Replace `print()` with `logger.info()`, `logger.error()`, etc.

4. **Configuration**

   * Keep a single `config.py` for now.
   * Split into `base.py`, `development.py`, and `production.py` only when you actually have environment-specific settings. Premature splitting tends to add complexity without much benefit.

---

## My recommended coding order

We'll build this in the following sequence:

1. ✅ `constants.py`
2. ✅ `DocumentChunk` model
3. ✅ Migration
4. ✅ Schemas
5. ✅ `chunking_service.py`
6. ✅ Integrate into `document_service.py`
7. ✅ Tests