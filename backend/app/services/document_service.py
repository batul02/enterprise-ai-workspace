from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi import UploadFile

from app.services.pdf_parser import parse_pdf
from app.models.document import Document
from app.storage.file_storage import (
    delete_file,
    save_file,
)
from app.core.constants import ExtractionStatus
from app.models.document_chunk import DocumentChunk
from app.services.chunking_service import chunk_text

def create_document(
    db: Session,
    workspace_id: int,
    uploaded_by: int,
    file: UploadFile,
) -> Document:

    filename, storage_path = save_file(
        workspace_id,
        file,
    )

    parse_result = parse_pdf(storage_path)

    document = Document(
        workspace_id=workspace_id,
        filename=filename,
        original_filename=file.filename,
        content_type=file.content_type,
        file_size=file.size,
        storage_path=storage_path,
        uploaded_by=uploaded_by,
    )

    # Save parser results
    if parse_result.success:
        document.extraction_status = ExtractionStatus.COMPLETED.value
        document.page_count = parse_result.page_count
        document.extracted_text = parse_result.extracted_text
        document.processing_error = None

    else:
        document.extraction_status = ExtractionStatus.FAILED.value
        document.page_count = 0
        document.extracted_text = None
        document.processing_error = parse_result.error

    db.add(document)
    # db.commit()
    # db.refresh(document)
    db.flush()

    if parse_result.success:

        chunks = chunk_text(
            parse_result.extracted_text
        )

        for chunk in chunks:

            document_chunk = DocumentChunk(
                document_id=document.id,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                start_char=chunk.start_char,
                end_char=chunk.end_char,
                character_count=chunk.character_count,
                embedding_status="PENDING",
            )

            db.add(document_chunk)

    db.commit()
    db.refresh(document)
    return document

def list_documents(
    db: Session,
    workspace_id: int,
) -> list[Document]:

    statement = (
        select(Document)
        .where(Document.workspace_id == workspace_id)
        .order_by(Document.created_at.desc())
    )

    return list(db.scalars(statement).all())

def get_document(
    db: Session,
    document_id: int,
) -> Document | None:

    return db.get(
        Document,
        document_id,
    )

def delete_document(
    db: Session,
    document: Document,
):

    delete_file(document.storage_path)

    db.delete(document)

    db.commit()