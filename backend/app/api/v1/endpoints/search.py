from fastapi import APIRouter, Depends

from app.core.dependencies import retrieval_service
from app.schemas.retrieval import (
    SearchRequest,
    SearchResponse,
)
from app.services.retrieval_service import RetrievalService
from app.api.v1.endpoints.auth import get_current_user
from app.api.v1.endpoints.workspace import verify_workspace_owner
from app.services.workspace_service import get_workspace_by_id
from sqlalchemy.orm import Session
from app.db.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()


@router.post(
    "/workspaces/{workspace_id}/search",
    response_model=SearchResponse,
)
def search_workspace(
    workspace_id: int,
    request: SearchRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
    service: RetrievalService = Depends(
        lambda: retrieval_service
    ),
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

    results = service.search(
        query=request.query,
        workspace_id=workspace_id,
        top_k=request.top_k,
    )

    return SearchResponse(
        query=request.query,
        results=results,
    )