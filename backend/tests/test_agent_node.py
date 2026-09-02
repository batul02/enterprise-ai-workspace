from app.agents.nodes import agent_node
from app.agents.tools import create_search_documents_tool
from app.core.dependencies import create_resources


def test_agent_node_can_call_search_tool():
    
    # Create application resources for this test
    resources = create_resources()
    
    # Create the tool using the real retrieval service
    search_documents = create_search_documents_tool(
        resources.retrieval_service
    )
    
    state = {
        "query": "What are the characteristics of trustworthy AI?",
        "workspace_id": 61,
    }

    result = agent_node(
        state,
        resources.langchain_llm_service,
        search_documents,
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
    
    assert tool_call["args"]["workspace_id"] == 61
