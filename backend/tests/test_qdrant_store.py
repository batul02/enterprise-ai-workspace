import pytest

pytestmark = pytest.mark.integration
from qdrant_client.models import PointStruct

def make_point(point_id: int):
    from app.core.dependencies import create_resources
    resources = create_resources()
    return PointStruct(
        id=point_id,
        vector=[0.1] * resources.qdrant_store.vector_size,
        payload={
            "document_id": 999,
            "workspace_id": 999,
            "chunk_id": point_id,
            "chunk_index": 0,
            "filename": "test.pdf",
        },
    )


def test_vector_insertion():
    from app.core.dependencies import create_resources
    resources = create_resources()
    
    point = make_point(900001)

    resources.qdrant_store.upsert([point])

    result = resources.qdrant_store.client.retrieve(
        collection_name=resources.qdrant_store.collection_name,
        ids=[900001],
    )

    assert len(result) == 1
    assert result[0].id == 900001


def test_duplicate_upsert():
    from app.core.dependencies import create_resources
    resources = create_resources()
    point = make_point(900002)

    # Insert once
    resources.qdrant_store.upsert([point])

    # Insert same ID again
    resources.qdrant_store.upsert([point])

    result = resources.qdrant_store.client.retrieve(
        collection_name=resources.qdrant_store.collection_name,
        ids=[900002],
    )

    # Should still have only one point
    assert len(result) == 1


def test_vector_deletion():
    from app.core.dependencies import create_resources
    resources = create_resources()
    point = make_point(900003)

    resources.qdrant_store.upsert([point])

    # Verify it exists
    result = resources.qdrant_store.client.retrieve(
        collection_name=resources.qdrant_store.collection_name,
        ids=[900003],
    )

    assert len(result) == 1

    # Delete
    resources.qdrant_store.delete_by_ids([900003])

    # Verify it is gone
    result = resources.qdrant_store.client.retrieve(
        collection_name=resources.qdrant_store.collection_name,
        ids=[900003],
    )

    assert len(result) == 0