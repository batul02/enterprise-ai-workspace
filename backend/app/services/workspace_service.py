from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.workspace import Workspace
from app.schemas.workspace import (
    WorkspaceCreate,
    WorkspaceUpdate,
)

def create_workspace(
    db: Session,
    workspace_data: WorkspaceCreate,
    owner_id: int,
) -> Workspace:

    workspace = Workspace(
        name=workspace_data.name,
        description=workspace_data.description,
        owner_id=owner_id,
    )

    db.add(workspace)
    db.commit()
    db.refresh(workspace)

    return workspace

def list_workspaces(
    db: Session,
    owner_id: int,
) -> list[Workspace]:

    statement = (
        select(Workspace)
        .where(Workspace.owner_id == owner_id)
        .order_by(Workspace.created_at.desc())
    )

    return list(db.scalars(statement).all())

def get_workspace_by_id(
    db: Session,
    workspace_id: int,
) -> Workspace | None:

    return db.get(
        Workspace,
        workspace_id,
    )

def update_workspace(
    db: Session,
    workspace: Workspace,
    workspace_data: WorkspaceUpdate,
) -> Workspace:

    if workspace_data.name is not None:
        workspace.name = workspace_data.name

    if workspace_data.description is not None:
        workspace.description = workspace_data.description

    db.commit()
    db.refresh(workspace)

    return workspace

def delete_workspace(
    db: Session,
    workspace: Workspace,
) -> None:

    db.delete(workspace)
    db.commit()