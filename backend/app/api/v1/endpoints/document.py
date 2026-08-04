from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.api.v1.endpoints.auth import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.document import (
    DocumentResponse,
    DocumentSummary,
)
from app.services.document_service import (
    create_document,
    delete_document,
    get_document,
    list_documents,
)
from app.services.workspace_service import (
    get_workspace_by_id,
)

router = APIRouter()

def verify_workspace_access(
    workspace,
    current_user,
):
    if workspace.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this workspace.",
        )

@router.post(
    "/workspaces/{workspace_id}/documents",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_document(
    workspace_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    workspace = get_workspace_by_id(
        db,
        workspace_id,
    )

    if workspace is None:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found.",
        )

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=415,
            detail="Only PDF files are allowed.",
        )

    verify_workspace_access(
        workspace,
        current_user,
    )

    return create_document(
        db=db,
        workspace_id=workspace.id,
        uploaded_by=current_user.id,
        file=file,
    )

@router.get(
    "/workspaces/{workspace_id}/documents",
    response_model=list[DocumentSummary],
)
def get_documents(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    workspace = get_workspace_by_id(
        db,
        workspace_id,
    )

    if workspace is None:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found.",
        )

    verify_workspace_access(
        workspace,
        current_user,
    )

    return list_documents(
        db,
        workspace.id,
    )

@router.get(
    "/documents/{document_id}",
    response_model=DocumentResponse,
)
def get_document_by_id(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    document = get_document(
        db,
        document_id,
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    workspace = get_workspace_by_id(
        db,
        document.workspace_id,
    )

    verify_workspace_access(
        workspace,
        current_user,
    )

    return document

@router.delete(
    "/documents/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    document = get_document(
        db,
        document_id,
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    workspace = get_workspace_by_id(
        db,
        document.workspace_id,
    )

    verify_workspace_access(
        workspace,
        current_user,
    )

    delete_document(
        db,
        document,
    )