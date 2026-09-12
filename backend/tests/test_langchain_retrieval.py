import pytest

pytestmark = pytest.mark.integration
from app.services.langchain_rag_service import LangChainRetrievalService
from app.services.embedding_service import EmbeddingService
from app.core.config import settings
from qdrant_client import QdrantClient
from app.core.dependencies import create_resources
resources = create_resources()


def test_langchain_retrieval():

    service = LangChainRetrievalService(
        qdrant_client=resources.qdrant_store.client,
        collection_name=settings.QDRANT_COLLECTION,
        embedding_service=resources.embedding_service,
    )

    results = service.search(
        query="What are the characteristics of trustworthy AI?",
        workspace_id=61,
        top_k=5,
    )
    
    points = resources.qdrant_store.client.retrieve(
        collection_name=settings.QDRANT_COLLECTION,
        ids=[59],
        with_payload=True,
    )

    print("\n--- RAW QDRANT POINT ---")
    print(points[0])

    assert results
    assert len(results) <= 5

    for result in results:
        print("\n--- RESULT ---")
        print("Content:", result.page_content[:300])
        print("Metadata:", result.metadata)

    assert any("trustworthy ai" in result.page_content.lower() for result in results)
