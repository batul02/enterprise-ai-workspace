from langchain_core.embeddings import Embeddings


class LangChainEmbeddingAdapter(Embeddings):
    """
    Adapts the existing EmbeddingService
    to LangChain's Embeddings interface.
    """

    def __init__(self, embedding_service):
        self.embedding_service = embedding_service

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        return self.embedding_service.generate_embeddings(texts)

    def embed_query(
        self,
        text: str,
    ) -> list[float]:
        embeddings = self.embedding_service.generate_embeddings([text])

        return embeddings[0]
