from langgraph.graph import StateGraph, START, END

from app.agents.state import AgentState
from app.agents.router import route_query
from app.agents.nodes import rag_search_node, direct_answer_node, generate_node


def build_graph(
    retrieval_service,
    prompt_service,
    llm_service,
):

    graph = StateGraph(AgentState)

    graph.add_node(
        "router",
        route_query,
    )

    graph.add_node(
        "rag_search",
        lambda state: rag_search_node(
            state,
            retrieval_service,
        ),
    )

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

    graph.add_edge(
        START,
        "router",
    )

    graph.add_conditional_edges(
        "router",
        lambda state: state["route"],
        {
            "rag": "rag_search",
            "direct": "direct_answer",
        },
    )

    graph.add_edge(
        "rag_search",
        "generate",
    )

    graph.add_edge(
        "generate",
        END,
    )

    graph.add_edge(
        "direct_answer",
        END,
    )

    return graph.compile()
