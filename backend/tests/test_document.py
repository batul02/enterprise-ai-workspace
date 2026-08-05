from pathlib import Path
from tests.conftest import get_auth_headers, register_user

from fastapi.testclient import TestClient

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

def upload_document(
    client,
    workspace_id,
    headers,
    filename="sample.pdf",
    content_type="application/pdf",
):
    pdf_path = (
        Path(__file__).parent
        / "files"
        / filename
    )

    with open(pdf_path, "rb") as pdf:
        response = client.post(
            f"/api/v1/workspaces/{workspace_id}/documents",
            headers=headers,
            files={
                "file": (
                    filename,
                    pdf,
                    content_type,
                )
            },
        )

    return response

def test_upload_document(client):
    _, _, email = register_user(client)

    headers = get_auth_headers(
        client,
        email,
    )

    workspace = create_workspace(
        client,
        headers,
    )

    response = upload_document(
        client,
        workspace["id"],
        headers,
    )

    assert response.status_code == 201

    body = response.json()

    assert body["workspace_id"] == workspace["id"]
    assert body["original_filename"] == "sample.pdf"
    assert body["extraction_status"] == "COMPLETED"
    assert body["page_count"] > 0

def test_upload_without_auth(client):
    response = client.post(
        "/api/v1/workspaces/1/documents"
    )

    assert response.status_code == 401

def test_upload_other_user_workspace(client):
    _, _, email1 = register_user(client)

    headers1 = get_auth_headers(
        client,
        email1,
    )

    workspace = create_workspace(
        client,
        headers1,
    )

    _, _, email2 = register_user(client)

    headers2 = get_auth_headers(
        client,
        email2,
    )

    response = upload_document(
        client,
        workspace["id"],
        headers2,
    )

    assert response.status_code == 403

def test_list_documents(client):
    _, _, email = register_user(client)

    headers = get_auth_headers(
        client,
        email,
    )

    workspace = create_workspace(
        client,
        headers,
    )

    upload_document(
        client,
        workspace["id"],
        headers,
    )

    response = client.get(
        f"/api/v1/workspaces/{workspace['id']}/documents",
        headers=headers,
    )

    assert response.status_code == 200

    documents = response.json()

    assert len(documents) == 1

def test_delete_document(client):
    _, _, email = register_user(client)

    headers = get_auth_headers(
        client,
        email,
    )

    workspace = create_workspace(
        client,
        headers,
    )

    upload_response = upload_document(
        client,
        workspace["id"],
        headers,
    )

    document = upload_response.json()

    response = client.delete(
        f"/api/v1/documents/{document['id']}",
        headers=headers,
    )

    assert response.status_code == 204

def test_delete_nonexistent_document(client):
    _, _, email = register_user(client)

    headers = get_auth_headers(
        client,
        email,
    )

    response = client.delete(
        "/api/v1/documents/99999",
        headers=headers,
    )

    assert response.status_code == 404

def test_upload_wrong_mime_type(client):
    _, _, email = register_user(client)

    headers = get_auth_headers(client, email)

    workspace = create_workspace(client, headers)

    response = upload_document(
        client,
        workspace["id"],
        headers,
        filename="sample.txt",
        content_type="text/plain",
    )

    assert response.status_code == 415

def test_upload_corrupted_pdf(client):
    _, _, email = register_user(client)

    headers = get_auth_headers(client, email)

    workspace = create_workspace(client, headers)

    response = upload_document(
        client,
        workspace["id"],
        headers,
        filename="corrupted.pdf",
    )

    assert response.status_code == 201

    body = response.json()

    assert body["extraction_status"] == "FAILED"

def test_upload_empty_pdf(client):
    _, _, email = register_user(client)

    headers = get_auth_headers(client, email)

    workspace = create_workspace(client, headers)

    response = upload_document(
        client,
        workspace["id"],
        headers,
        filename="empty_01.pdf",
    )

    assert response.status_code == 201

    body = response.json()

    assert body["extraction_status"] == "FAILED"
    assert body["page_count"] == 0

def test_upload_zero_byte_pdf(client):
    _, _, email = register_user(client)

    headers = get_auth_headers(client, email)

    workspace = create_workspace(client, headers)

    response = upload_document(
        client,
        workspace["id"],
        headers,
        filename="empty.pdf",
    )

    assert response.status_code == 400