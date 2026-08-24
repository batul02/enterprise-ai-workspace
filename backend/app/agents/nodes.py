from app.agents.state import AgentState


def rag_search_node(
    state: AgentState,
    retrieval_service,
) -> dict:

    results = retrieval_service.search(
        query=state["query"],
        workspace_id=state["workspace_id"],
        top_k=5,
    )

    return {"retrieved_chunks": results}


def direct_answer_node(
    state: AgentState,
    llm_service,
) -> dict:

    answer = llm_service.generate(state["query"])

    return {"answer": answer}


def generate_node(
    state: AgentState,
    prompt_service,
    llm_service,
) -> dict:

    chunks = state.get("retrieved_chunks", [])

    if not chunks:
        return {
            "answer": ("I don't have enough information " "in the provided documents.")
        }

    prompt = prompt_service.build_prompt(
        query=state["query"],
        chunks=chunks,
    )

    answer = llm_service.generate(prompt)

    return {"answer": answer}
