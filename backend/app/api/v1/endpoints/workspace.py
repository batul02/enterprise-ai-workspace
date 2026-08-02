from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.models.workspace import Workspace
from app.schemas.workspace import (
    WorkspaceCreate,
    WorkspaceResponse,
    WorkspaceUpdate,
)
from app.services.workspace_service import (
    create_workspace,
    delete_workspace,
    get_workspace_by_id,
    list_workspaces,
    update_workspace,
)

from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()

@router.post(
    "",
    response_model=WorkspaceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_workspace(
    workspace_data: WorkspaceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_workspace(
        db=db,
        workspace_data=workspace_data,
        owner_id=current_user.id,
    )

@router.get(
    "",
    response_model=list[WorkspaceResponse],
)
def get_workspaces(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_workspaces(
        db=db,
        owner_id=current_user.id,
    )

def verify_workspace_owner(
    workspace: Workspace,
    current_user: User,
):
    if workspace.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this workspace.",
        )

@router.get(
    "/{workspace_id}",
    response_model=WorkspaceResponse,
)
def get_workspace(
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found.",
        )

    verify_workspace_owner(
        workspace,
        current_user,
    )

    return workspace

@router.put(
    "/{workspace_id}",
    response_model=WorkspaceResponse,
)
def update_existing_workspace(
    workspace_id: int,
    workspace_data: WorkspaceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    workspace = get_workspace_by_id(
        db,
        workspace_id,
    )

    if workspace is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found.",
        )

    verify_workspace_owner(
        workspace,
        current_user,
    )

    return update_workspace(
        db,
        workspace,
        workspace_data,
    )

@router.delete(
    "/{workspace_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_workspace(
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found.",
        )

    verify_workspace_owner(
        workspace,
        current_user,
    )

    delete_workspace(
        db,
        workspace,
    )