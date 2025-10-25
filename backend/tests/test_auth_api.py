"""Tests for authentication API endpoints."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.user import UserRole
from app.services import auth_service

client = TestClient(app)


@pytest.fixture
async def test_admin_user(monkeypatch):
    """Create a test admin user and return credentials."""
    from app.models.user import UserCreate
    import uuid

    # Use unique email for each test
    unique_email = f"admin_{uuid.uuid4().hex[:8]}@test.com"

    user_data = UserCreate(
        email=unique_email,
        password="adminpass123",
        role=UserRole.ADMIN,
        full_name="Test Admin"
    )

    user = await auth_service.create_user(user_data)
    return {"email": unique_email, "password": "adminpass123", "user": user}


@pytest.fixture
async def test_editor_user(monkeypatch):
    """Create a test editor user and return credentials."""
    from app.models.user import UserCreate
    import uuid

    # Use unique email for each test
    unique_email = f"editor_{uuid.uuid4().hex[:8]}@test.com"

    user_data = UserCreate(
        email=unique_email,
        password="editorpass123",
        role=UserRole.EDITOR,
        full_name="Test Editor"
    )

    user = await auth_service.create_user(user_data)
    return {"email": unique_email, "password": "editorpass123", "user": user}


def get_auth_token(email: str, password: str) -> str:
    """Helper to get authentication token."""
    response = client.post(
        "/auth/login",
        data={"username": email, "password": password}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_login_success(test_admin_user):
    """Test successful login."""
    response = client.post(
        "/auth/login",
        data={
            "username": test_admin_user["email"],
            "password": test_admin_user["password"]
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(test_admin_user):
    """Test login with wrong password."""
    response = client.post(
        "/auth/login",
        data={
            "username": test_admin_user["email"],
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


def test_login_nonexistent_user():
    """Test login with non-existent user."""
    response = client.post(
        "/auth/login",
        data={
            "username": "nonexistent@test.com",
            "password": "anypassword"
        }
    )

    assert response.status_code == 401


def test_get_current_user(test_admin_user):
    """Test getting current user information."""
    token = get_auth_token(test_admin_user["email"], test_admin_user["password"])

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_admin_user["email"]
    assert data["role"] == UserRole.ADMIN


def test_get_current_user_no_token():
    """Test accessing protected endpoint without token."""
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_get_current_user_invalid_token():
    """Test accessing protected endpoint with invalid token."""
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401


def test_register_user_as_admin(test_admin_user):
    """Test registering a new user as admin."""
    import uuid
    token = get_auth_token(test_admin_user["email"], test_admin_user["password"])

    new_email = f"newuser_{uuid.uuid4().hex[:8]}@test.com"
    response = client.post(
        "/auth/register",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": new_email,
            "password": "newuserpass123",
            "role": UserRole.VIEWER,
            "full_name": "New User"
        }
    )

    if response.status_code != 201:
        print(f"Error response: {response.json()}")

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == new_email
    assert data["role"] == UserRole.VIEWER


def test_register_user_as_editor(test_editor_user):
    """Test that editors cannot register new users."""
    token = get_auth_token(test_editor_user["email"], test_editor_user["password"])

    response = client.post(
        "/auth/register",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": "another@test.com",
            "password": "password123",
            "role": UserRole.VIEWER
        }
    )

    assert response.status_code == 403
    assert "Insufficient permissions" in response.json()["detail"]


def test_register_duplicate_email(test_admin_user):
    """Test registering user with duplicate email."""
    token = get_auth_token(test_admin_user["email"], test_admin_user["password"])

    # Register first user
    client.post(
        "/auth/register",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": "duplicate@test.com",
            "password": "password123",
            "role": UserRole.VIEWER
        }
    )

    # Attempt duplicate
    response = client.post(
        "/auth/register",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": "duplicate@test.com",
            "password": "password456",
            "role": UserRole.EDITOR
        }
    )

    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_list_users_as_admin(test_admin_user, test_editor_user):
    """Test listing users as admin."""
    token = get_auth_token(test_admin_user["email"], test_admin_user["password"])

    response = client.get(
        "/auth/users",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) >= 2  # At least admin and editor


def test_list_users_as_editor(test_editor_user):
    """Test that editors cannot list users."""
    token = get_auth_token(test_editor_user["email"], test_editor_user["password"])

    response = client.get(
        "/auth/users",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_user_as_admin(test_admin_user):
    """Test deleting a user as admin."""
    from app.models.user import UserCreate

    # Create user to delete
    user_data = UserCreate(
        email="todelete@test.com",
        password="password123",
        role=UserRole.VIEWER
    )
    user_to_delete = await auth_service.create_user(user_data)

    token = get_auth_token(test_admin_user["email"], test_admin_user["password"])

    response = client.delete(
        f"/auth/users/{user_to_delete.id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 204


def test_delete_self(test_admin_user):
    """Test that users cannot delete their own account."""
    token = get_auth_token(test_admin_user["email"], test_admin_user["password"])

    response = client.delete(
        f"/auth/users/{test_admin_user['user'].id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    assert "Cannot delete your own account" in response.json()["detail"]
