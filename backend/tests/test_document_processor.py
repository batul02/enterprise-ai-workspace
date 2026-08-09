from unittest.mock import Mock

import pytest

from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.processors.document_processor import DocumentProcessor

def test_process_document(db):
    document = Document(
        workspace_id=1,
        filename="sample.pdf",
        original_filename="sample.pdf",
        content_type="application/pdf",
        file_size=1024,
        storage_path="storage/1/sample.pdf",
        uploaded_by=1,
    )

    db.add(document)
    db.flush()

    embedding_service = Mock()

    embedding_service.generate_embeddings.return_value = [
        [0.1, 0.2, 0.3],
    ]

    vector_store = Mock()

    processor = DocumentProcessor(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    text = "This is a small document."

    processor.process(
        db=db,
        document=document,
        extracted_text=text,
    )

    db.flush()

    # DocumentChunk was created
    chunks = (
        db.query(DocumentChunk)
        .filter(
            DocumentChunk.document_id
            == document.id
        )
        .all()
    )

    assert len(chunks) == 1

    # Chunk data is correct
    assert chunks[0].content == text
    assert chunks[0].chunk_index == 0

    # Embedding service was called
    embedding_service.generate_embeddings.assert_called_once_with(
        [text]
    )

    # Qdrant was called
    vector_store.upsert.assert_called_once()

    # Embedding status updated
    assert chunks[0].embedding_status == "COMPLETED"
    
def test_process_empty_text(db):
    document = Document(
        workspace_id=1,
        filename="empty.pdf",
        original_filename="empty.pdf",
        content_type="application/pdf",
        file_size=1024,
        storage_path="storage/1/empty.pdf",
        uploaded_by=1,
    )

    db.add(document)
    db.flush()

    embedding_service = Mock()
    vector_store = Mock()

    processor = DocumentProcessor(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    processor.process(
        db=db,
        document=document,
        extracted_text="",
    )

    embedding_service.generate_embeddings.assert_not_called()

    vector_store.upsert.assert_not_called()

    chunks = (
        db.query(DocumentChunk)
        .filter(
            DocumentChunk.document_id
            == document.id
        )
        .all()
    )

    assert chunks == []
    
def test_process_multiple_chunks(db):
    document = Document(
        workspace_id=1,
        filename="large.pdf",
        original_filename="large.pdf",
        content_type="application/pdf",
        file_size=1024,
        storage_path="storage/1/large.pdf",
        uploaded_by=1,
    )

    db.add(document)
    db.flush()

    embedding_service = Mock()

    embedding_service.generate_embeddings.side_effect = (
        lambda texts: [
            [0.1, 0.2, 0.3]
            for _ in texts
        ]
    )

    vector_store = Mock()

    processor = DocumentProcessor(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    text = "A" * 2500

    processor.process(
        db=db,
        document=document,
        extracted_text=text,
    )

    db.flush()

    chunks = (
        db.query(DocumentChunk)
        .filter(
            DocumentChunk.document_id
            == document.id
        )
        .order_by(DocumentChunk.chunk_index)
        .all()
    )

    assert len(chunks) > 1

    assert [
        chunk.chunk_index
        for chunk in chunks
    ] == list(range(len(chunks)))

    assert all(
        chunk.embedding_status == "COMPLETED"
        for chunk in chunks
    )

    embedding_service.generate_embeddings.assert_called_once()

    vector_store.upsert.assert_called_once()
    
def test_embedding_count_mismatch(db):
    document = Document(
        workspace_id=1,
        filename="sample.pdf",
        original_filename="sample.pdf",
        content_type="application/pdf",
        file_size=1024,
        storage_path="storage/1/sample.pdf",
        uploaded_by=1,
    )

    db.add(document)
    db.flush()

    embedding_service = Mock()

    embedding_service.generate_embeddings.return_value = [
        [0.1, 0.2, 0.3],
    ]

    vector_store = Mock()

    processor = DocumentProcessor(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    text = "A" * 2500

    with pytest.raises(
        ValueError,
        match="Embedding count does not match",
    ):
        processor.process(
            db=db,
            document=document,
            extracted_text=text,
        )

    vector_store.upsert.assert_not_called()
    
    
def test_qdrant_metadata(db):
    document = Document(
        workspace_id=1,
        filename="financial.pdf",
        original_filename="financial_report.pdf",
        content_type="application/pdf",
        file_size=1024,
        storage_path="storage/1/financial_report.pdf",
        uploaded_by=1,
    )

    db.add(document)
    db.flush()

    embedding_service = Mock()

    embedding_service.generate_embeddings.return_value = [
        [0.1, 0.2, 0.3],
    ]

    vector_store = Mock()

    processor = DocumentProcessor(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    processor.process(
        db=db,
        document=document,
        extracted_text="Financial report content.",
    )

    vector_store.upsert.assert_called_once()

    points = vector_store.upsert.call_args[0][0]

    assert len(points) == 1

    point = points[0]

    assert point.id > 0

    assert point.payload["document_id"] == document.id
    assert point.payload["workspace_id"] == 1
    assert point.payload["chunk_id"] == point.id
    assert point.payload["chunk_index"] == 0
    assert (
        point.payload["filename"]
        == "financial_report.pdf"
    )