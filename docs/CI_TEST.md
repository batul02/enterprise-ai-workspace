## 1. PROJECT — CI result

Based on your latest GitHub Actions result:

```
7 passed
1 failed
76 deselected
```

### Failure category

```
□ CI passed
□ Dependency installation failed
□ Import/configuration failed
□ External service was required
☑ Tests failed
□ Python-version issue
□ Other
```

The failure is specifically a test mocking/import-path issue:

```
AttributeError:
module 'app.api.v1.endpoints.search'
has no attribute 'retrieval_service'
```

The workspace tests are now passing.

### CI status note

Add this to your README or development notes:

Markdown

```
## CI Status

GitHub Actions is configured to:
- Set up Python
- Install dependencies
- Run Alembic database migrations
- Run pytest

Current status:
- [ ] All tests pass in CI
- [x] Unit tests are separated from integration tests
- [ ] Linting is enabled
- [ ] Docker build is checked in CI

Latest CI result:
- 7 tests passed
- 1 test failed
- 76 tests deselected
- Failure category: Tests failed
- Current failure: Search test uses an outdated mock target
```

Change the unit-test checkbox only if you have actually separated or clearly marked unit tests. Based on your current pytest command, tests are filtered by markers, but that is not necessarily the same as physically separating them into folders.

# 2. TESTING — Test classification

Based on the test files and test names you shared, the current classification should be:

Markdown

```
# Test Classification

## Unit tests

These should be fast and isolated.

Examples:
- Text chunking tests
- Input validation tests
- Pydantic schema tests
- Authentication/token utility tests
- Pure helper-function tests
- Repository-independent business logic tests
- Tests using mocks/fakes without PostgreSQL, Qdrant, Ollama, or FastAPI

## Integration tests

These verify multiple application components working together.

Current examples:
- `tests/test_workspace.py`
  - `test_create_workspace`
  - `test_list_workspaces`
  - `test_get_workspace`
  - `test_update_workspace`
  - `test_delete_workspace`
  - `test_workspace_without_token`
  - `test_access_other_users_workspace`

- `tests/test_search.py`
  - `test_search_valid_request`

Reason:
- Use FastAPI `TestClient`
- Register and authenticate users
- Access API routes
- Use PostgreSQL-backed application state
- Create and access workspaces
- Test authentication and authorization behavior

## Evaluation tests

These should measure AI or retrieval quality rather than only HTTP/API correctness.

Examples:
- Retrieval evaluation datasets
- Recall@k
- Precision@k
- MRR
- Context relevance
- Answer faithfulness
- RAG answer correctness
- LLM-as-judge evaluation
```

## Important distinction

Your current `test_search.py` test is an integration/API test, even though retrieval is mocked.

Why?

Because it still:

* Creates a user

* Logs in

* Creates a workspace

* Calls the FastAPI endpoint

* Tests authentication and route behavior

* Tests the endpoint response structure

The mocked retrieval service only isolates the vector-search dependency. It does not make the entire test a unit test.

## Recommended marker usage

For your current files:

Python

Run

```
# tests/test_workspace.py
pytestmark = pytest.mark.integration
```

Python

Run

```
# tests/test_search.py
pytestmark = pytest.mark.integration
```

Then your CI command:

Bash

```
pytest -m "not integration and not evaluation" -v
```

will exclude both files.

If you want these tests to run in CI, use a separate integration job:

Bash

```
pytest -m integration -v
```

## Current conclusion

```
Project:
  Tests failed — only search test remains.

Testing:
  test_workspace.py → Integration tests
  test_search.py    → Integration tests
  Unit tests        → Need separate isolated tests
  Evaluation tests  → Need retrieval/RAG quality tests
```

The next small task is not to redesign the whole test structure. First fix the search test’s mock target, then record the CI status.



## 1. PROJECT — Inspect the CI result


Go to:

```
Actions
  ↓
CI
  ↓
Latest workflow run
```

Record which one applies:

```
□ CI passed
□ Dependency installation failed
□ Import/configuration failed
□ Tests failed
□ External service was required
□ Python-version issue
□ Other
```

### Your only project task

Create a small note in your project, either in the README or a development note:

```
## CI Status

GitHub Actions is configured to:
- Set up Python
- Install dependencies
- Run pytest

Current status:
- [ ] All tests pass in CI
- [ ] Unit tests are separated from integration tests
- [ ] Linting is enabled
- [ ] Docker build is checked in CI
```

Do not solve every failure today. First understand the failure category.

## 2. TESTING — Create test categories

Time: 30 minutes

Look at your existing test files and classify them.

Suggested structure:

```
tests/
├── unit/
├── integration/
└── evaluation/
```

If moving files could break imports, do not move them yet. You can first create a simple classification document:

```
# Test Classification

## Unit tests
- Chunking tests
- Validation tests
- Pure utility tests

## Integration tests
- PostgreSQL tests
- Qdrant tests
- FastAPI + database tests

## Evaluation tests
- Retrieval evaluation dataset
- Retrieval quality checks
- RAG answer quality checks
```

### Key principle

- Unit tests: fast, isolated, no database/vector store/LLM
- Integration tests: verify components working together
- Evaluation tests: measure AI quality, not only code correctness
