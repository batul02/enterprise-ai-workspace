from app.agents.state import AgentState


def agent_node(state: AgentState,
    langchain_llm_service,
    search_documents,):
    query = state["query"]
    llm = langchain_llm_service.llm.bind_tools([search_documents])

    messages = [
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
        )
    ]

    # Add previous conversation
    for message in state.get("conversation_history", []):
        messages.append(
            (
                message["role"],
                message["content"],
            )
        )

    messages.append(
        (
            "user",
            f"""
            Workspace ID: {state["workspace_id"]}
            User question:
            {query}
            """,
        )
    )

    response = llm.invoke(messages)

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

# direct_answer_node with conversation history
# def direct_answer_node(
#     state: AgentState,
#     llm_service,
# ) -> dict:

#     history = state.get("conversation_history", [])

#     history_text = "\n".join(
#         f"{message['role'].upper()}: {message['content']}"
#         for message in history
#         if message.get("role") and message.get("content")
#     )

#     prompt = f"""
#     You are an AI assistant.

#     Use the conversation history to understand the user's current question.

#     CONVERSATION HISTORY:
#     {history_text}

#     CURRENT USER QUESTION:
#     {state["query"]}

#     ANSWER:
#     """

#     answer = llm_service.generate(prompt)

#     return {"answer": answer}


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
        conversation_history=state.get(
            "conversation_history",
            [],
        ),
    )

    answer = llm_service.generate(prompt)

    return {"answer": answer}
