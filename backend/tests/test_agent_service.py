from app.core.dependencies import create_resources


def test_agent_service_direct_answer_with_history():
    resources = create_resources()

    result = resources.agent_service.chat(
        query="What database does the project use?",
        workspace_id=61,
        conversation_history=[
            {
                "role": "user",
                "content": "Tell me about the project's backend.",
            },
            {
                "role": "assistant",
                "content": "The project uses PostgreSQL for its database.",
            },
        ],
    )

    assert "answer" in result
    assert result["answer"]
    

def test_agent_service_rag_with_conversation_history():
    resources = create_resources()

    result = resources.agent_service.chat(
        query="What does that policy say about employees?",
        workspace_id=61,
        conversation_history=[
            {
                "role": "user",
                "content": "What is the leave policy?",
            },
            {
                "role": "assistant",
                "content": "The workspace documents contain the company's leave policy.",
            },
        ],
    )

    assert "answer" in result
    assert result["answer"]
    

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_chat_endpoint_with_conversation_history():
    response = client.post(
        "/api/v1/workspaces/61/chat",
        json={
            "query": "What database does the project use?",
            "top_k": 5,
            "conversation_history": [
                {
                    "role": "user",
                    "content": "Tell me about the backend.",
                },
                {
                    "role": "assistant",
                    "content": "The project uses PostgreSQL.",
                },
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert data["answer"]