from app.schemas.retrieval import SearchResult


class RetrievalService:
    """
    Performs semantic search over document chunks
    using query embeddings and a vector store.
    """

    def __init__(
        self,
        embedding_service,
        vector_store,
        score_threshold: float | None = None,
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.score_threshold = score_threshold

    def search(
        self,
        query: str,
        workspace_id: int,
        top_k: int,
    ) -> list[SearchResult]:

        if not query.strip():
            return []

        # Generate embedding for the query
        embeddings = (
            self.embedding_service.generate_embeddings(
                [query]
            )
        )

        if len(embeddings) != 1:
            raise ValueError(
                "Expected exactly one query embedding."
            )

        query_vector = embeddings[0]

        # Search Qdrant
        points = self.vector_store.search(
            vector=query_vector,
            top_k=top_k,
            workspace_id=workspace_id,
            score_threshold=self.score_threshold,
        )

        results = []

        for point in points:

            payload = point.payload or {}

            results.append(
                SearchResult(
                    chunk_id=payload["chunk_id"],
                    content=payload["content"],
                    score=point.score,
                    document_id=payload["document_id"],
                    page_number=payload.get(
                        "page_number"
                    ),
                    filename=payload["filename"],
                )
            )

        return results