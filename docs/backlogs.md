Since we've already completed the basic Docker setup and decided to leave health/readiness for now, I would **not jump straight into more agent features**. We should fix the correctness issue first.

## Recommended order

### 🔴 Priority 1 — Fix deletion/failure consistency (done)

Your architecture has multiple stores:

```text
                 Document
                    │
          ┌─────────┼─────────┐
          ↓         ↓         ↓
       File      PostgreSQL  Qdrant
```

The dangerous situation is:

```text
Delete PostgreSQL ✓
Delete file       ✓
Delete Qdrant     ✗
```

Now Qdrant contains vectors for a document that no longer exists.

Similarly during ingestion:

```text
Save file ✓
DB insert ✗
```

→ orphaned file

or:

```text
DB insert ✓
Qdrant insert ✓
something fails
```

→ inconsistent state.

This is the **most important correctness problem** you've identified.

---

### 🔴 Priority 2 — Fix chunker bug (done)

We should reproduce and fix:

```python
start = end - CHUNK_OVERLAP
```

when `end < CHUNK_OVERLAP`.

Currently that can produce:

```text
start = -194
```

and potentially an empty/invalid chunk.

The fix should be accompanied by a **regression test**, not just a code change.

---

### 🟠 Priority 3 — Properly organize tests

Now that you've built:

* Custom RAG
* LangChain retrieval
* Query transformation
* LangGraph
* Agent routing
* Docker

we have enough tests that organization matters.

I'd move toward:

```text
tests/
│
├── unit/
│   ├── test_chunking.py
│   ├── test_router.py
│   ├── test_prompt_service.py
│   └── test_query_transformer.py
│
├── integration/
│   ├── test_retrieval.py
│   ├── test_langchain_retrieval.py
│   └── test_agent_graph.py
│
└── evaluation/
    └── ...
```

Then add pytest markers:

```text
unit
integration
evaluation
```

so you can do:

```bash
pytest -m unit
```

without starting Qdrant/Ollama/etc.

And:

```bash
pytest -m integration
```

when the infrastructure is available.

---

### 🟠 Priority 4 — CI

Once the tests are separated:

```text
git push
   ↓
GitHub Actions
   ↓
install dependencies
   ↓
unit tests
   ↓
✓ / ✗
```

This gives the project a much more professional engineering workflow.

---

### 🟡 Priority 5 — Operational/API hardening

This is a larger backlog:

```text
Background ingestion
Structured logging
Health/readiness
Metrics
Tracing
Pagination
Validation
PDF signature validation
Rate limiting
Duplicate username handling
```

We shouldn't tackle all of those at once.

---

# So what should we do now?

I'd follow this sequence:

```text
              CURRENT PROJECT
                    │
                    ▼
        ┌──────────────────────┐
        │ 1. Store consistency │ 🔴
        └──────────┬───────────┘
                   ↓
        ┌──────────────────────┐
        │ 2. Chunker bug       │ 🔴
        └──────────┬───────────┘
                   ↓
        ┌──────────────────────┐
        │ 3. Test organization │ 🟠
        └──────────┬───────────┘
                   ↓
        ┌──────────────────────┐
        │ 4. GitHub CI         │ 🟠
        └──────────┬───────────┘
                   ↓
        ┌──────────────────────┐
        │ 5. Operational       │ 🟡
        │    hardening         │
        └──────────────────────┘
```

