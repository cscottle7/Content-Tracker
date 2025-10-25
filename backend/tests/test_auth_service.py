"""Tests for authentication service."""

import pytest
import uuid

from app.models.user import UserCreate, UserRole
from app.services import auth_service


def unique_email(prefix="test"):
    """Generate unique email address for testing."""
    return f"{prefix}_{uuid.uuid4().hex[:8]}@example.com"


@pytest.mark.asyncio
async def test_create_user():
    """Test creating a new user."""
    email = unique_email("test")
    user_data = UserCreate(
        email=email,
        full_name="Test User",
        password="testpass123",
        role=UserRole.EDITOR,
    )

    user = await auth_service.create_user(user_data)

    assert user.email == email
    assert user.full_name == "Test User"
    assert user.role == UserRole.EDITOR
    assert user.is_active is True
    assert user.id is not None


@pytest.mark.asyncio
async def test_create_duplicate_user():
    """Test that creating duplicate email fails."""
    email = unique_email("duplicate")
    user_data = UserCreate(
        email=email,
        password="testpass123",
        role=UserRole.VIEWER,
    )

    # Create first user
    await auth_service.create_user(user_data)

    # Attempt to create duplicate
    with pytest.raises(ValueError, match="already exists"):
        await auth_service.create_user(user_data)


@pytest.mark.asyncio
async def test_authenticate_user_success():
    """Test successful user authentication."""
    # Create user
    email = unique_email("auth_test")
    user_data = UserCreate(
        email=email,
        password="mypassword123",
        role=UserRole.EDITOR,
    )
    created_user = await auth_service.create_user(user_data)

    # Authenticate
    authenticated_user = await auth_service.authenticate_user(
        email,
        "mypassword123"
    )

    assert authenticated_user is not None
    assert authenticated_user.id == created_user.id
    assert authenticated_user.email == email


@pytest.mark.asyncio
async def test_authenticate_user_wrong_password():
    """Test authentication with wrong password."""
    # Create user
    email = unique_email("wrong_pass")
    user_data = UserCreate(
        email=email,
        password="correctpassword",
        role=UserRole.VIEWER,
    )
    await auth_service.create_user(user_data)

    # Try to authenticate with wrong password
    result = await auth_service.authenticate_user(
        email,
        "wrongpassword"
    )

    assert result is None


@pytest.mark.asyncio
async def test_authenticate_nonexistent_user():
    """Test authentication of non-existent user."""
    result = await auth_service.authenticate_user(
        "nonexistent@example.com",
        "anypassword"
    )

    assert result is None


def test_password_hashing():
    """Test password hashing and verification."""
    password = "mysecretpassword123"

    # Hash password
    hashed = auth_service.get_password_hash(password)

    # Verify correct password
    assert auth_service.verify_password(password, hashed) is True

    # Verify incorrect password
    assert auth_service.verify_password("wrongpassword", hashed) is False


def test_create_and_decode_token():
    """Test JWT token creation and decoding."""
    data = {"sub": "user123", "email": "test@example.com"}

    # Create token
    token = auth_service.create_access_token(data)
    assert token is not None

    # Decode token
    decoded = auth_service.decode_access_token(token)
    assert decoded is not None
    assert decoded["sub"] == "user123"
    assert decoded["email"] == "test@example.com"
    assert "exp" in decoded


def test_decode_invalid_token():
    """Test decoding invalid JWT token."""
    result = auth_service.decode_access_token("invalid.token.string")
    assert result is None


@pytest.mark.asyncio
async def test_get_user_by_email():
    """Test retrieving user by email."""
    # Create user
    email = unique_email("lookup")
    user_data = UserCreate(
        email=email,
        password="password123",
        role=UserRole.ADMIN,
    )
    created_user = await auth_service.create_user(user_data)

    # Look up by email
    found_user = await auth_service.get_user_by_email(email)

    assert found_user is not None
    assert found_user.id == created_user.id
    assert found_user.email == email
    assert found_user.password_hash is not None  # UserInDB includes hash


@pytest.mark.asyncio
async def test_get_user_by_id():
    """Test retrieving user by ID."""
    # Create user
    email = unique_email("byid")
    user_data = UserCreate(
        email=email,
        password="password123",
        role=UserRole.EDITOR,
    )
    created_user = await auth_service.create_user(user_data)

    # Look up by ID
    found_user = await auth_service.get_user_by_id(created_user.id)

    assert found_user is not None
    assert found_user.id == created_user.id
    assert found_user.email == email


@pytest.mark.asyncio
async def test_list_users():
    """Test listing all users."""
    # Create multiple users
    for i in range(3):
        user_data = UserCreate(
            email=unique_email(f"listuser{i}"),
            password="password123",
            role=UserRole.VIEWER,
        )
        await auth_service.create_user(user_data)

    # List users
    users = await auth_service.list_users()

    assert len(users) >= 3
    assert all(user.email for user in users)


@pytest.mark.asyncio
async def test_delete_user():
    """Test deleting a user."""
    # Create user
    email = unique_email("delete_me")
    user_data = UserCreate(
        email=email,
        password="password123",
        role=UserRole.VIEWER,
    )
    created_user = await auth_service.create_user(user_data)

    # Delete user
    deleted = await auth_service.delete_user(created_user.id)
    assert deleted is True

    # Verify user no longer exists
    found_user = await auth_service.get_user_by_id(created_user.id)
    assert found_user is None


@pytest.mark.asyncio
async def test_update_user():
    """Test updating user fields."""
    # Create user
    email = unique_email("update_test")
    user_data = UserCreate(
        email=email,
        password="password123",
        role=UserRole.VIEWER,
    )
    created_user = await auth_service.create_user(user_data)

    # Update role
    updated_user = await auth_service.update_user(
        created_user.id,
        role=UserRole.EDITOR,
        full_name="Updated Name"
    )

    assert updated_user is not None
    assert updated_user.role == UserRole.EDITOR
    assert updated_user.full_name == "Updated Name"
