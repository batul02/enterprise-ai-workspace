from unittest.mock import Mock

import pytest

from app.services.rag_service import RAGService


@pytest.fixture
def retrieval_service():
    return Mock()


@pytest.fixture
def prompt_service():
    return Mock()


@pytest.fixture
def llm_service():
    return Mock()


@pytest.fixture
def rag_service(
    retrieval_service,
    prompt_service,
    llm_service,
):
    return RAGService(
        retrieval_service=retrieval_service,
        prompt_service=prompt_service,
        llm_service=llm_service,
    )
    
def test_answer(
    rag_service,
    retrieval_service,
    prompt_service,
    llm_service,
):

    results = [
        {
            "chunk_id": 1,
            "document_id": 10,
            "filename": "loan_policy.pdf",
            "content": "Interest rates start at 8.5%.",
            "score": 0.91,
        }
    ]

    retrieval_service.search.return_value = results

    prompt_service.build_prompt.return_value = (
        "Answer using the provided context."
    )

    llm_service.generate.return_value = (
        "The interest rate starts at 8.5%."
    )

    response = rag_service.answer(
        query="What is the interest rate?",
        workspace_id=1,
        top_k=5,
    )

    assert response["answer"] == (
        "The interest rate starts at 8.5%."
    )

    assert response["sources"] == results

    retrieval_service.search.assert_called_once_with(
        query="What is the interest rate?",
        workspace_id=1,
        top_k=5,
    )

    prompt_service.build_prompt.assert_called_once_with(
        query="What is the interest rate?",
        chunks=results,
    )

    llm_service.generate.assert_called_once_with(
        "Answer using the provided context."
    )
    
def test_answer_with_no_results(
    rag_service,
    retrieval_service,
    prompt_service,
    llm_service,
):

    retrieval_service.search.return_value = []

    response = rag_service.answer(
        query="What is the CEO's favorite food?",
        workspace_id=1,
        top_k=5,
    )

    assert response["answer"] == (
        "I don't have enough information "
        "in the provided documents."
    )

    assert response["sources"] == []

    prompt_service.build_prompt.assert_not_called()
    llm_service.generate.assert_not_called()
    
def test_empty_query(
    rag_service,
    retrieval_service,
):

    with pytest.raises(ValueError):

        rag_service.answer(
            query="",
            workspace_id=1,
        )

    retrieval_service.search.assert_not_called()
    
def test_whitespace_query(
    rag_service,
    retrieval_service,
):

    with pytest.raises(ValueError):

        rag_service.answer(
            query="   ",
            workspace_id=1,
        )

    retrieval_service.search.assert_not_called()