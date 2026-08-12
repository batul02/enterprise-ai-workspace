from unittest.mock import patch

from tests.conftest import (
    get_auth_headers,
    register_user,
)


def create_workspace(client, headers):
    response = client.post(
        "/api/v1/workspaces",
        json={
            "name": "Finance",
            "description": "Finance Workspace",
        },
        headers=headers,
    )

    assert response.status_code == 201

    return response.json()


def test_search_valid_request(client):
    _, _, email = register_user(client)

    headers = get_auth_headers(
        client,
        email,
    )

    workspace = create_workspace(
        client,
        headers,
    )

    mocked_results = [
        {
            "chunk_id": 1,
            "content": "Personal loan interest rates start at 8.5%.",
            "score": 0.91,
            "document_id": 10,
            "page_number": 4,
            "filename": "loan_policy.pdf",
        }
    ]

    with patch(
        "app.api.v1.endpoints.search.retrieval_service.search",
        return_value=mocked_results,
    ):

        response = client.post(
            f"/api/v1/workspaces/{workspace['id']}/search",
            json={
                "query": "What is the personal loan interest rate?",
                "top_k": 5,
            },
            headers=headers,
        )

    assert response.status_code == 200

    body = response.json()

    assert body["query"] == (
        "What is the personal loan interest rate?"
    )

    assert len(body["results"]) == 1

    assert body["results"][0]["score"] == 0.91
    assert body["results"][0]["filename"] == "loan_policy.pdf"