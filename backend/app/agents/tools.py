from langchain_core.tools import tool

@tool
def search_documents(
    query: str,
    workspace_id: int,
) -> list:
    """
    Search the workspace documents for information relevant
    to the user's question.
    """
    from app.core.dependencies import retrieval_service

    return retrieval_service.search(
        query=query,
        workspace_id=workspace_id,
        top_k=5,
    )
