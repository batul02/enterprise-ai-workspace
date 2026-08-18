from unittest.mock import Mock

from app.services.langchain_rag_service import LangChainRAGService


def test_rag_answer():

    retrieval_service = Mock()
    prompt_service = Mock()
    llm_service = Mock()

    document_1 = Mock()
    document_1.page_content = "Trustworthy AI is valid and reliable."

    document_2 = Mock()
    document_2.page_content = "Trustworthy AI should also be safe and secure."

    retrieval_service.search.return_value = [
        document_1,
        document_2,
    ]

    prompt_service.build_prompt.return_value = (
        "constructed prompt"
    )

    llm_service.generate.return_value = (
        "Trustworthy AI should be valid, reliable, safe, and secure."
    )

    service = LangChainRAGService(
        retrieval_service=retrieval_service,
        prompt_service=prompt_service,
        llm_service=llm_service,
    )

    result = service.answer(
        question="What is trustworthy AI?",
        workspace_id=61,
        top_k=5,
    )

    assert result == (
        "Trustworthy AI should be valid, reliable, safe, and secure."
    )

    retrieval_service.search.assert_called_once_with(
        query="What is trustworthy AI?",
        workspace_id=61,
        top_k=5,
    )

    prompt_service.build_prompt.assert_called_once_with(
        question="What is trustworthy AI?",
        context=(
            "Trustworthy AI is valid and reliable.\n\n"
            "Trustworthy AI should also be safe and secure."
        ),
    )

    llm_service.generate.assert_called_once_with(
        "constructed prompt"
    )