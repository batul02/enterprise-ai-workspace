class AgentService:

    def __init__(self, graph):
        self.graph = graph

    def chat(
        self,
        query: str,
        workspace_id: int,
        conversation_history: list[dict] | None = None,
    ):
        return self.graph.invoke(
            {
                "query": query,
                "workspace_id": workspace_id,
                "conversation_history": conversation_history or [],
            }
        )