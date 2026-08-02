def register_user(client):
    return client.post(
        "/api/v1/auth/register",
        json={
            "username": "batul",
            "email": "batul@test.com",
            "password": "Password123"
        },
    )


def login_user(client, password="Password123"):
    return client.post(
        "/api/v1/auth/login",
        json={
            "email": "batul@test.com",
            "password": password,
        },
    )


def test_register_valid_user(client):
    response = register_user(client)

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "batul"
    assert data["email"] == "batul@test.com"

    assert "password" not in data
    assert "hashed_password" not in data


def test_duplicate_email(client):
    register_user(client)

    response = register_user(client)

    assert response.status_code == 409


def test_login_valid_credentials(client):
    register_user(client)

    response = login_user(client)

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    register_user(client)

    response = login_user(client, "WrongPassword")

    assert response.status_code == 401


def test_me_without_token(client):
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401


def test_me_invalid_token(client):
    response = client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": "Bearer invalid_token"
        },
    )

    assert response.status_code == 401


def test_me_valid_token(client):
    register_user(client)

    login_response = login_user(client)

    token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "batul"
    assert data["email"] == "batul@test.com"

    assert "hashed_password" not in data