from typing import TypedDict


class AgentState(TypedDict, total=False):
    query: str
    workspace_id: int
    route: str
    retrieved_chunks: list
    answer: str
