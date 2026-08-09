from qdrant_client.models import PointStruct

from app.core.dependencies import qdrant_store


def make_point(point_id: int):
    return PointStruct(
        id=point_id,
        vector=[0.1] * qdrant_store.vector_size,
        payload={
            "document_id": 999,
            "workspace_id": 999,
            "chunk_id": point_id,
            "chunk_index": 0,
            "filename": "test.pdf",
        },
    )


def test_vector_insertion():
    point = make_point(900001)

    qdrant_store.upsert([point])

    result = qdrant_store.client.retrieve(
        collection_name=qdrant_store.collection_name,
        ids=[900001],
    )

    assert len(result) == 1
    assert result[0].id == 900001


def test_duplicate_upsert():
    point = make_point(900002)

    # Insert once
    qdrant_store.upsert([point])

    # Insert same ID again
    qdrant_store.upsert([point])

    result = qdrant_store.client.retrieve(
        collection_name=qdrant_store.collection_name,
        ids=[900002],
    )

    # Should still have only one point
    assert len(result) == 1


def test_vector_deletion():
    point = make_point(900003)

    qdrant_store.upsert([point])

    # Verify it exists
    result = qdrant_store.client.retrieve(
        collection_name=qdrant_store.collection_name,
        ids=[900003],
    )

    assert len(result) == 1

    # Delete
    qdrant_store.delete_by_ids([900003])

    # Verify it is gone
    result = qdrant_store.client.retrieve(
        collection_name=qdrant_store.collection_name,
        ids=[900003],
    )

    assert len(result) == 0