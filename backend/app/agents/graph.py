from langgraph.graph import StateGraph, START, END

from app.agents.state import AgentState
from app.agents.router import route_query
from app.agents.nodes import (
    agent_node,
    rag_search_node,
    direct_answer_node,
    generate_node,
)
from langgraph.prebuilt import ToolNode
from app.agents.tools import create_search_documents_tool


def should_continue(state):
    messages = state.get("messages", [])

    if not messages:
        return "direct"

    last_message = messages[-1]

    if getattr(last_message, "tool_calls", None):
        return "tools"

    return "direct"


def build_graph(
    retrieval_service,
    prompt_service,
    llm_service,
    langchain_llm_service,
):
    search_documents = create_search_documents_tool(retrieval_service)
    tool_node = ToolNode([search_documents])

    graph = StateGraph(AgentState)

    # graph.add_node(
    #     "router",
    #     route_query,
    # )

    # graph.add_node(
    #     "rag_search",
    #     lambda state: rag_search_node(
    #         state,
    #         retrieval_service,
    #     ),
    # )

    graph.add_node(
        "direct_answer",
        lambda state: direct_answer_node(
            state,
            llm_service,
        ),
    )

    graph.add_node(
        "generate",
        lambda state: generate_node(
            state,
            prompt_service,
            llm_service,
        ),
    )

    # graph.add_edge(
    #     START,
    #     "router",
    # )

    # graph.add_conditional_edges(
    #     "router",
    #     lambda state: state["route"],
    #     {
    #         "rag": "rag_search",
    #         "direct": "direct_answer",
    #     },
    # )

    # graph.add_edge(
    #     "rag_search",
    #     "generate",
    # )

    graph.add_node(
        "agent",
        lambda state: agent_node(
            state,
            langchain_llm_service,
            search_documents,
        ),
    )

    graph.add_edge(
        START,
        "agent",
    )

    # graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)

    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "direct": "direct_answer",
        },
    )

    # graph.add_edge("tools", "agent")
    graph.add_edge("tools", "generate")

    graph.add_edge(
        "generate",
        END,
    )

    graph.add_edge(
        "direct_answer",
        END,
    )

    return graph.compile()
