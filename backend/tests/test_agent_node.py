from app.agents.nodes import agent_node


def test_agent_node_can_call_search_tool():
    state = {
        "query": "What are the characteristics of trustworthy AI?",
        "workspace_id": 61,
    }

    result = agent_node(
        state,
    )

    assert result
    assert "messages" in result
    assert result["messages"]

    response = result["messages"][0]

    print("\n--- AGENT RESPONSE ---")
    print(response)

    print("\n--- TOOL CALLS ---")
    print(response.tool_calls)

    assert response.tool_calls

    tool_call = response.tool_calls[0]

    assert tool_call["name"] == "search_documents"

    print("\n--- TOOL NAME ---")
    print(tool_call["name"])

    print("\n--- TOOL ARGUMENTS ---")
    print(tool_call["args"])
