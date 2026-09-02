from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.core.dependencies import AppResources
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
from app.schemas.search import ChatRequest, ChatResponse
from app.api.v1.endpoints.document import verify_workspace_access

router = APIRouter()


@router.post(
    "/workspaces/{workspace_id}/search",
    response_model=SearchResponse,
)
def search_workspace(
    workspace_id: int,
    request: SearchRequest,
    http_request: Request,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
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

    resources: AppResources = http_request.app.state.resources

    results = resources.retrieval_service.search(
        query=request.query,
        workspace_id=workspace_id,
        top_k=request.top_k,
    )

    return SearchResponse(
        query=request.query,
        results=results,
    )


@router.post(
    "/workspaces/{workspace_id}/chat",
    response_model=ChatResponse,
)
def chat(
    workspace_id: int,
    request: ChatRequest,
    http_request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
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

    # Use your existing workspace authorization logic here.
    verify_workspace_access(
        workspace=workspace,
        current_user=current_user,
    )

    resources: AppResources = http_request.app.state.resources

    result = resources.rag_service.answer(
        query=request.query,
        workspace_id=workspace_id,
        top_k=request.top_k,
        conversation_history=[
            message.model_dump() for message in request.conversation_history
        ],
    )

    return result
