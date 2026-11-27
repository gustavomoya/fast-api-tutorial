
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.main import app
from app.auth.dependencies import get_current_active_user
from app.users.models import User


def create_user(
    db_session: Session,
    email: str,
    is_active: bool = True,
) -> User:
    user = User(
        name="Test User",
        email=email,
        password_hash="fake-password-hash",
        is_active=is_active,
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


def create_project(client: TestClient) -> int:
    response = client.post(
        "/projects/",
        json={"name": "Project Members Test"},
    )

    assert response.status_code == 201

    return response.json()["id"]


def test_add_member(
    authenticated_client: TestClient,
    db_session: Session,
):
    owner = app.dependency_overrides[get_current_active_user]()
    project_id = create_project(authenticated_client)

    user = create_user(db_session, "member@example.com")

    response = authenticated_client.post(
        f"/projects/{project_id}/members/",
        json={"user_id": user.id},
    )

    assert response.status_code == 201
    assert response.json()["project_id"] == project_id
    assert response.json()["user_id"] == user.id
    assert response.json()["created_at"] is not None


def test_add_member_duplicate(
    authenticated_client: TestClient,
    db_session: Session,
):
    project_id = create_project(authenticated_client)
    user = create_user(db_session, "duplicate@example.com")

    url = f"/projects/{project_id}/members/"

    first_response = authenticated_client.post(
        url,
        json={"user_id": user.id},
    )

    second_response = authenticated_client.post(
        url,
        json={"user_id": user.id},
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_add_nonexistent_user(authenticated_client: TestClient):
    project_id = create_project(authenticated_client)

    response = authenticated_client.post(
        f"/projects/{project_id}/members/",
        json={"user_id": 99999},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_add_inactive_user(
    authenticated_client: TestClient,
    db_session: Session,
):
    project_id = create_project(authenticated_client)

    user = create_user(
        db_session,
        "inactive@example.com",
        is_active=False,
    )

    response = authenticated_client.post(
        f"/projects/{project_id}/members/",
        json={"user_id": user.id},
    )

    assert response.status_code == 400


def test_owner_cannot_be_added_as_member(
    authenticated_client: TestClient,
):
    owner = app.dependency_overrides[get_current_active_user]()
    project_id = create_project(authenticated_client)

    response = authenticated_client.post(
        f"/projects/{project_id}/members/",
        json={"user_id": owner.id},
    )

    assert response.status_code == 400


def test_non_owner_cannot_add_member(
    authenticated_client: TestClient,
    db_session: Session,
):
    project_id = create_project(authenticated_client)

    collaborator = create_user(
        db_session,
        "collaborator@example.com",
    )

    target_user = create_user(
        db_session,
        "target@example.com",
    )

    app.dependency_overrides[get_current_active_user] = (
        lambda: collaborator
    )

    response = authenticated_client.post(
        f"/projects/{project_id}/members/",
        json={"user_id": target_user.id},
    )

    assert response.status_code == 403


def test_get_members_as_owner(
    authenticated_client: TestClient,
    db_session: Session,
):
    project_id = create_project(authenticated_client)
    user = create_user(db_session, "list-member@example.com")

    authenticated_client.post(
        f"/projects/{project_id}/members/",
        json={"user_id": user.id},
    )

    response = authenticated_client.get(
        f"/projects/{project_id}/members/"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["user_id"] == user.id


def test_get_members_as_member(
    authenticated_client: TestClient,
    db_session: Session,
):
    project_id = create_project(authenticated_client)

    collaborator = create_user(
        db_session,
        "list-collaborator@example.com",
    )

    authenticated_client.post(
        f"/projects/{project_id}/members/",
        json={"user_id": collaborator.id},
    )

    app.dependency_overrides[get_current_active_user] = (
        lambda: collaborator
    )

    response = authenticated_client.get(
        f"/projects/{project_id}/members/"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_external_user_cannot_get_members(
    authenticated_client: TestClient,
    db_session: Session,
):
    project_id = create_project(authenticated_client)

    outsider = create_user(
        db_session,
        "outsider@example.com",
    )

    app.dependency_overrides[get_current_active_user] = (
        lambda: outsider
    )

    response = authenticated_client.get(
        f"/projects/{project_id}/members/"
    )

    assert response.status_code == 403


def test_remove_member(
    authenticated_client: TestClient,
    db_session: Session,
):
    project_id = create_project(authenticated_client)
    user = create_user(db_session, "remove-member@example.com")

    authenticated_client.post(
        f"/projects/{project_id}/members/",
        json={"user_id": user.id},
    )

    response = authenticated_client.delete(
        f"/projects/{project_id}/members/{user.id}"
    )

    assert response.status_code == 204
    assert response.content == b""

    members_response = authenticated_client.get(
        f"/projects/{project_id}/members/"
    )

    assert members_response.status_code == 200
    assert members_response.json() == []


def test_non_owner_cannot_remove_member(
    authenticated_client: TestClient,
    db_session: Session,
):
    project_id = create_project(authenticated_client)

    collaborator = create_user(
        db_session,
        "remove-collaborator@example.com",
    )

    target_user = create_user(
        db_session,
        "remove-target@example.com",
    )

    authenticated_client.post(
        f"/projects/{project_id}/members/",
        json={"user_id": collaborator.id},
    )

    authenticated_client.post(
        f"/projects/{project_id}/members/",
        json={"user_id": target_user.id},
    )

    app.dependency_overrides[get_current_active_user] = (
        lambda: collaborator
    )

    response = authenticated_client.delete(
        f"/projects/{project_id}/members/{target_user.id}"
    )

    assert response.status_code == 403


def test_add_member_unauthorized(client: TestClient):
    response = client.post(
        "/projects/1/members/",
        json={"user_id": 2},
    )

    assert response.status_code == 401
