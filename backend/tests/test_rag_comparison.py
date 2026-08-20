from app.services.rag_service import RAGService
from app.services.langchain_rag_service import (
    LangChainRAGService,
    LangChainRetrievalService,
)
from app.services.langchain_prompt_service import (
    LangChainPromptService,
)
from app.services.langchain_llm_service import (
    LangChainLLMService,
)

# Use the same objects/configuration that your existing tests use.
from app.services.embedding_service import EmbeddingService
from app.core.config import settings
from app.core.dependencies import qdrant_store, rag_service, embedding_service

WORKSPACE_ID = 61
TOP_K = 5

QUESTIONS = [
    "What are the characteristics of trustworthy AI?",
    "What are the four core functions of the AI RMF?",
    "What does the GOVERN function address?",
    "What is the difference between the MAP and MEASURE functions?",
    "What does the AI RMF say about validity and reliability?",
]


def create_langchain_rag():

    retrieval_service = LangChainRetrievalService(
        qdrant_client=qdrant_store.client,
        collection_name=settings.QDRANT_COLLECTION,
        embedding_service=embedding_service,
    )

    prompt_service = LangChainPromptService()

    llm_service = LangChainLLMService(
        model=settings.LLM_MODEL,
    )

    return LangChainRAGService(
        retrieval_service=retrieval_service,
        prompt_service=prompt_service,
        llm_service=llm_service,
    )


def test_rag_comparison():

    custom_rag = rag_service
    langchain_rag = create_langchain_rag()

    for question in QUESTIONS:

        print("\n")
        print("=" * 80)
        print("QUESTION")
        print(question)
        print("=" * 80)

        custom_result = custom_rag.answer(
            query=question,
            workspace_id=WORKSPACE_ID,
            top_k=TOP_K,
        )

        langchain_result = langchain_rag.answer(
            question=question,
            workspace_id=WORKSPACE_ID,
            top_k=TOP_K,
        )

        print("\n--- CUSTOM RAG ---")
        print(custom_result)

        print("\n--- LANGCHAIN RAG ---")
        print(langchain_result)

        assert custom_result
        assert langchain_result
