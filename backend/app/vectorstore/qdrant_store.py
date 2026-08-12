from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    Filter,
    FieldCondition,
    MatchValue,
    PointIdsList,
    PointStruct,
    VectorParams,
)


class QdrantStore:
    """
    Stores and retrieves document embeddings using Qdrant.
    """

    def __init__(
        self,
        host: str,
        port: int,
        collection_name: str,
        vector_size: int,
    ):
        self.collection_name = collection_name

        self.client = QdrantClient(
            host=host,
            port=port,
        )

        self.vector_size = vector_size

        self.create_collection()

    def create_collection(self) -> None:
        """
        Create the Qdrant collection if it does not already exist.
        """

        collections = self.client.get_collections()

        existing_names = {
            collection.name
            for collection in collections.collections
        }

        if self.collection_name in existing_names:
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE,
            ),
        )

    def upsert(
        self,
        points: list[PointStruct],
    ) -> None:
        """
        Insert or update vector points in Qdrant.
        """

        if not points:
            return

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
            wait=True,
        )

    def delete_by_document(
        self,
        document_id: int,
    ) -> None:
        """
        Delete all vectors belonging to a document.
        """

        self.client.delete(
            collection_name=self.collection_name,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(
                            value=document_id
                        ),
                    )
                ]
            ),
            wait=True,
        )

    def delete_by_ids(
        self,
        point_ids: list[int],
    ) -> None:
        """
        Delete vectors using their point IDs.
        """

        if not point_ids:
            return

        self.client.delete(
            collection_name=self.collection_name,
            points_selector=PointIdsList(
                points=point_ids,
            ),
            wait=True,
        )
        
    def search(
        self,
        vector: list[float],
        top_k: int,
        workspace_id: int,
        score_threshold: float | None = None,
    ):
        """
        Search for semantically similar vectors within a workspace.
        """

        query_filter = Filter(
            must=[
                FieldCondition(
                    key="workspace_id",
                    match=MatchValue(
                        value=workspace_id
                    ),
                )
            ]
        )

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=vector,
            query_filter=query_filter,
            limit=top_k,
            score_threshold=score_threshold,
            with_payload=True,
        )

        return results.points