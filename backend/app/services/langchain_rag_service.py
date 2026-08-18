from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore

from app.services.embedding_service import EmbeddingService
from app.services.langchain_embeddings import LangChainEmbeddingAdapter
from qdrant_client.models import (
    FieldCondition,
    Filter,
    MatchValue,
)


class LangChainRetrievalService:
    """
    Provides semantic retrieval using LangChain
    over the existing Qdrant vector collection.
    """

    def __init__(
        self,
        qdrant_client: QdrantClient,
        collection_name: str,
        embedding_service: EmbeddingService,
    ):
        self.embedding_adapter = LangChainEmbeddingAdapter(embedding_service)

        self.vector_store = QdrantVectorStore(
            client=qdrant_client,
            collection_name=collection_name,
            embedding=self.embedding_adapter,
            content_payload_key="content",
        )

    def get_retriever(
        self,
        workspace_id: int,
        top_k: int = 5,
    ):
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="workspace_id",
                    match=MatchValue(value=workspace_id),
                )
            ]
        )

        return self.vector_store.as_retriever(
            search_kwargs={
                "k": top_k,
                "filter": query_filter,
            }
        )

    def search(
        self,
        query: str,
        workspace_id: int,
        top_k: int = 5,
    ):
        retriever = self.get_retriever(
            workspace_id=workspace_id,
            top_k=top_k,
        )

        results = retriever.invoke(query)

        for result in results:
            print("\n--- LANGCHAIN DOCUMENT ---")
            print("Content:", result.page_content[:100])
            print("Metadata:", result.metadata)

        return results

class LangChainRAGService:

    def __init__(
        self,
        retrieval_service,
        prompt_service,
        llm_service,
    ):
        self.retrieval_service = retrieval_service
        self.prompt_service = prompt_service
        self.llm_service = llm_service

    def answer(
        self,
        question: str,
        workspace_id: int,
        top_k: int = 5,
    ):

        documents = self.retrieval_service.search(
            query=question,
            workspace_id=workspace_id,
            top_k=top_k,
        )

        context = "\n\n".join(document.page_content for document in documents)

        prompt = self.prompt_service.build_prompt(
            question=question,
            context=context,
        )

        return self.llm_service.generate(prompt)
