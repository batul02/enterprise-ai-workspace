from app.agents.state import AgentState


def agent_node(state: AgentState,
    langchain_llm_service,
    search_documents,):
    query = state["query"]
    llm = langchain_llm_service.llm.bind_tools([search_documents])

    response = llm.invoke(
        [
            (
                "system",
                """
                You are an assistant for a document workspace.

                You have access to the search_documents tool.

                When the user's question requires information
                from workspace documents, use the tool.

                The workspace ID is provided by the application.
                Always use the provided workspace ID when calling
                search_documents.
                """,
            ),
            (
                "user",
                f"""
                Workspace ID: {state["workspace_id"]}
                User question:
                {query}
                """,
            ),
        ]
    )

    return {
        "messages": [response],
    }

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
