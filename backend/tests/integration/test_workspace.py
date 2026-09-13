from tests.conftest import register_user, login_user, get_auth_headers


def create_workspace(client, headers):
    response = client.post(
        "/api/v1/workspaces",
        json={
            "name": "Finance",
            "description": "Finance documents",
        },
        headers=headers,
    )

    assert response.status_code == 201

    return response.json()

def test_create_workspace(client):
    _, _, email = register_user(client)

    headers = get_auth_headers(client, email)

    response = client.post(
        "/api/v1/workspaces",
        json={
            "name": "Finance",
            "description": "Finance documents",
        },
        headers=headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Finance"
    assert data["description"] == "Finance documents"

def test_list_workspaces(client):
    _, _, email = register_user(client)

    headers = get_auth_headers(client, email)

    create_workspace(client, headers)

    response = client.get(
        "/api/v1/workspaces",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) >= 1

def test_get_workspace(client):
    _, _, email = register_user(client)

    headers = get_auth_headers(client, email)

    workspace = create_workspace(
        client,
        headers,
    )

    response = client.get(
        f"/api/v1/workspaces/{workspace['id']}",
        headers=headers,
    )

    assert response.status_code == 200

    assert response.json()["id"] == workspace["id"]

def test_update_workspace(client):
    _, _, email = register_user(client)

    headers = get_auth_headers(client, email)

    workspace = create_workspace(
        client,
        headers,
    )

    response = client.put(
        f"/api/v1/workspaces/{workspace['id']}",
        json={
            "name": "HR Workspace",
            "description": "HR documents",
        },
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "HR Workspace"

def test_delete_workspace(client):
    _, _, email = register_user(client)

    headers = get_auth_headers(client, email)

    workspace = create_workspace(
        client,
        headers,
    )

    response = client.delete(
        f"/api/v1/workspaces/{workspace['id']}",
        headers=headers,
    )

    assert response.status_code == 204

def test_workspace_without_token(client):
    response = client.get(
        "/api/v1/workspaces",
    )

    assert response.status_code == 401

def test_access_other_users_workspace(client):
    _, _, email_one = register_user(client)

    headers_one = get_auth_headers(
        client,
        email_one,
    )

    workspace = create_workspace(
        client,
        headers_one,
    )

    _, _, email_two = register_user(client)

    headers_two = get_auth_headers(
        client,
        email_two,
    )

    response = client.get(
        f"/api/v1/workspaces/{workspace['id']}",
        headers=headers_two,
    )

    assert response.status_code == 403