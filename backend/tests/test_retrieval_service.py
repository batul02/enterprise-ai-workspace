from unittest.mock import Mock

import pytest

from app.services.retrieval_service import RetrievalService


def make_point(
    chunk_id,
    content,
    score,
    document_id=1,
    workspace_id=1,
    filename="test.pdf",
    page_number=None,
    chunk_index=0,
):
    point = Mock()

    point.id = chunk_id
    point.score = score

    point.payload = {
        "chunk_id": chunk_id,
        "content": content,
        "document_id": document_id,
        "workspace_id": workspace_id,
        "filename": filename,
        "page_number": page_number,
        "chunk_index": chunk_index,
    }

    return point


def create_service():
    embedding_service = Mock()
    vector_store = Mock()

    embedding_service.generate_embeddings.return_value = [
        [0.1, 0.2, 0.3]
    ]

    service = RetrievalService(
        embedding_service=embedding_service,
        vector_store=vector_store,
        score_threshold=0.0,
    )

    return service, embedding_service, vector_store


def test_search_returns_results():
    service, embedding_service, vector_store = create_service()

    vector_store.search.return_value = [
        make_point(
            chunk_id=1,
            content="Personal loan interest rates...",
            score=0.91,
            document_id=10,
            filename="loan_policy.pdf",
            page_number=4,
        )
    ]

    results = service.search(
        query="What is the interest rate?",
        workspace_id=1,
        top_k=5,
    )

    assert len(results) == 1

    result = results[0]

    assert result.chunk_id == 1
    assert result.content == "Personal loan interest rates..."
    assert result.score == 0.91
    assert result.document_id == 10
    assert result.filename == "loan_policy.pdf"
    assert result.page_number == 4


def test_query_embedding_generated():
    service, embedding_service, vector_store = create_service()

    vector_store.search.return_value = []

    service.search(
        query="What is the interest rate?",
        workspace_id=1,
        top_k=5,
    )

    embedding_service.generate_embeddings.assert_called_once_with(
        ["What is the interest rate?"]
    )


def test_top_k_passed_to_vector_store():
    service, embedding_service, vector_store = create_service()

    vector_store.search.return_value = []

    service.search(
        query="What is the interest rate?",
        workspace_id=1,
        top_k=3,
    )

    vector_store.search.assert_called_once()

    call_kwargs = vector_store.search.call_args.kwargs

    assert call_kwargs["top_k"] == 3


def test_workspace_id_passed_to_vector_store():
    service, embedding_service, vector_store = create_service()

    vector_store.search.return_value = []

    service.search(
        query="What is the interest rate?",
        workspace_id=42,
        top_k=5,
    )

    call_kwargs = vector_store.search.call_args.kwargs

    assert call_kwargs["workspace_id"] == 42


def test_results_ordered():
    service, embedding_service, vector_store = create_service()

    vector_store.search.return_value = [
        make_point(
            chunk_id=1,
            content="Highest similarity",
            score=0.95,
        ),
        make_point(
            chunk_id=2,
            content="Medium similarity",
            score=0.82,
        ),
        make_point(
            chunk_id=3,
            content="Lowest similarity",
            score=0.71,
        ),
    ]

    results = service.search(
        query="loan interest",
        workspace_id=1,
        top_k=3,
    )

    scores = [
        result.score
        for result in results
    ]

    assert scores == [0.95, 0.82, 0.71]


def test_empty_results():
    service, embedding_service, vector_store = create_service()

    vector_store.search.return_value = []

    results = service.search(
        query="Something unrelated",
        workspace_id=1,
        top_k=5,
    )

    assert results == []


def test_empty_query():
    service, embedding_service, vector_store = create_service()

    results = service.search(
        query="   ",
        workspace_id=1,
        top_k=5,
    )

    assert results == []

    embedding_service.generate_embeddings.assert_not_called()

    vector_store.search.assert_not_called()