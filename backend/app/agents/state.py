from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages


class AgentState(TypedDict, total=False):
    query: str
    workspace_id: int
    conversation_history: list[dict]
    route: str
    retrieved_chunks: list
    answer: str
    messages: Annotated[list, add_messages]
