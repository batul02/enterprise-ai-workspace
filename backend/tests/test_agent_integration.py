from app.core.dependencies import agents_service


def test_full_agent_rag_flow():

    result = agents_service.invoke(
        {
            "query": "What are the characteristics of trustworthy AI?",
            "workspace_id": 61,
        }
    )

    print("\n========== FINAL AGENT RESULT ==========")
    print(result)

    print("\n========== ANSWER ==========")
    print(result.get("answer"))

    print("\n========== MESSAGES ==========")

    for message in result.get("messages", []):
        print("\n--- MESSAGE ---")
        print(message)

    assert result
    assert result.get("answer")
    assert result.get("messages")

    # We expect the agent to have made at least one tool call
    tool_calls = []

    for message in result["messages"]:
        tool_calls.extend(getattr(message, "tool_calls", []))

    print("\n========== TOOL CALLS ==========")
    print(tool_calls)

    assert tool_calls

    assert any(call["name"] == "search_documents" for call in tool_calls)
