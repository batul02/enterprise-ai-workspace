import pytest
from fastapi.testclient import TestClient

from app.main import app
import uuid

from app.db.database import SessionLocal


@pytest.fixture
def client():
    """
    Returns a FastAPI TestClient.
    """
    with TestClient(app) as test_client:
        yield test_client
        
@pytest.fixture
def db():
    """
    Returns a database session for tests.
    """
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()

def register_user(client):
    unique = uuid.uuid4().hex[:8]

    email = f"{unique}@test.com"
    username = f"user_{unique}"

    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "Password123",
        },
    )

    assert response.status_code == 201

    return response, username, email

def login_user(client, email, password="Password123"):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    return response

def get_auth_headers(client, email):
    response = login_user(client, email)

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }