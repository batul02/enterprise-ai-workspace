from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi import UploadFile

from app.models.document import Document
from app.storage.file_storage import (
    delete_file,
    save_file,
)

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

    document = Document(
        workspace_id=workspace_id,
        filename=filename,
        original_filename=file.filename,
        content_type=file.content_type,
        file_size=file.size,
        storage_path=storage_path,
        uploaded_by=uploaded_by,
    )

    db.add(document)
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