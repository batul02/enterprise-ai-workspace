from app.agents.state import AgentState


def route_query(state: AgentState) -> dict:
    query = state["query"].lower()

    rag_keywords = [
        "document",
        "policy",
        "report",
        "according to",
        "what does",
        "what are",
        "explain",
    ]

    if any(keyword in query for keyword in rag_keywords):
        return {"route": "rag"}

    return {"route": "direct"}
