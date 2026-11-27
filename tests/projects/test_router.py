
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.main import app
from app.auth.dependencies import get_current_active_user
from app.users.models import User


@pytest.fixture
def authenticated_client(
    client: TestClient,
    db_session: Session,
):
    user = User(
        name="Test User",
        email="router-test@example.com",
        password_hash="fake-password-hash",
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    app.dependency_overrides[get_current_active_user] = lambda: user

    yield client

    app.dependency_overrides.pop(get_current_active_user, None)


def test_get_projects(client: TestClient):
    response = client.get("/projects/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_project_not_found(client: TestClient):
    response = client.get("/projects/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


def test_create_project(authenticated_client: TestClient):
    response = authenticated_client.post(
        "/projects/",
        json={
            "name": "Router Test Project",
            "description": "Project created through the API",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["name"] == "Router Test Project"
    assert data["description"] == "Project created through the API"
    assert data["owner"]["email"] == "router-test@example.com"


def test_create_project_unauthorized(client: TestClient):
    response = client.post(
        "/projects/",
        json={
            "name": "Unauthorized Project",
            "description": "This should not be created",
        },
    )

    assert response.status_code == 401


def test_create_project_empty_name(authenticated_client: TestClient):
    response = authenticated_client.post(
        "/projects/",
        json={"name": ""},
    )

    assert response.status_code == 422


def test_create_project_name_too_long(authenticated_client: TestClient):
    response = authenticated_client.post(
        "/projects/",
        json={"name": "A" * 151},
    )

    assert response.status_code == 422


def test_patch_project(authenticated_client: TestClient):
    create_response = authenticated_client.post(
        "/projects/",
        json={"name": "Original Project", "description": "Original description"},
    )

    project_id = create_response.json()["id"]

    response = authenticated_client.patch(
        f"/projects/{project_id}",
        json={"name": "Updated Project"},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Project"
    assert response.json()["description"] == "Original description"


def test_patch_project_not_found(authenticated_client: TestClient):
    response = authenticated_client.patch(
        "/projects/99999",
        json={"name": "Updated Project"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"



def test_patch_project_empty_name(authenticated_client: TestClient):
    create_response = authenticated_client.post(
        "/projects/",
        json={"name": "Original Project"},
    )
    project_id = create_response.json()["id"]

    response = authenticated_client.patch(
        f"/projects/{project_id}",
        json={"name": ""},
    )

    assert response.status_code == 422


def test_patch_project_null_name(authenticated_client: TestClient):
    create_response = authenticated_client.post(
        "/projects/",
        json={"name": "Original Project"},
    )
    project_id = create_response.json()["id"]

    response = authenticated_client.patch(
        f"/projects/{project_id}",
        json={"name": None},
    )

    assert response.status_code == 422


def test_patch_project_clear_description(authenticated_client: TestClient):
    create_response = authenticated_client.post(
        "/projects/",
        json={
            "name": "Original Project",
            "description": "Original description",
        },
    )
    project_id = create_response.json()["id"]

    response = authenticated_client.patch(
        f"/projects/{project_id}",
        json={"description": None},
    )

    assert response.status_code == 200
    assert response.json()["description"] is None


def test_update_project(authenticated_client: TestClient):
    create_response = authenticated_client.post(
        "/projects/",
        json={"name": "Original Project", "description": "Original description"},
    )

    project_id = create_response.json()["id"]

    response = authenticated_client.put(
        f"/projects/{project_id}",
        json={
            "name": "Completely Updated Project",
            "description": "New description",
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Completely Updated Project"
    assert response.json()["description"] == "New description"


def test_update_project_not_found(authenticated_client: TestClient):
    response = authenticated_client.put(
        "/projects/99999",
        json={"name": "Updated Project"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"



def test_update_project_empty_name(authenticated_client: TestClient):
    response = authenticated_client.put(
        "/projects/1",
        json={"name": ""},
    )

    assert response.status_code == 422


def test_update_project_name_too_long(authenticated_client: TestClient):
    response = authenticated_client.put(
        "/projects/1",
        json={"name": "A" * 151},
    )

    assert response.status_code == 422


def test_update_project_missing_name(authenticated_client: TestClient):
    response = authenticated_client.put(
        "/projects/1",
        json={"description": "Updated description"},
    )

    assert response.status_code == 422



def test_delete_project(authenticated_client: TestClient):
    create_response = authenticated_client.post(
        "/projects/",
        json={"name": "Project to delete"},
    )

    project_id = create_response.json()["id"]

    response = authenticated_client.delete(f"/projects/{project_id}")

    assert response.status_code == 204
    assert response.content == b""

    get_response = authenticated_client.get(f"/projects/{project_id}")

    assert get_response.status_code == 404


def test_delete_project_not_found(authenticated_client: TestClient):
    response = authenticated_client.delete("/projects/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


def test_delete_project_unauthorized(client: TestClient):
    response = client.delete("/projects/1")

    assert response.status_code == 401
