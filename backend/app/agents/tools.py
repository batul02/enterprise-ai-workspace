from langchain_core.tools import tool

def create_search_documents_tool(retrieval_service):

    @tool
    def search_documents(
        query: str,
        workspace_id: int,
    ) -> list:
        """
        Search the workspace documents for information relevant
        to the user's question.
        """

        return retrieval_service.search(
            query=query,
            workspace_id=workspace_id,
            top_k=5,
        )

    return search_documents