"""Authentication API endpoints.

Handles user login, registration, and session management.
Implements JWT-based authentication.
"""

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.config import settings
from app.models.user import Token, UserCreate, UserResponse, UserRole
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["authentication"])

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserResponse:
    """Dependency to get current authenticated user from JWT token.

    Args:
        token: JWT access token

    Returns:
        Current user

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = auth_service.decode_access_token(token)
    if not payload:
        raise credentials_exception

    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = await auth_service.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    return user


def require_role(required_role: str):
    """Dependency factory to require specific role.

    Args:
        required_role: Required role (admin, editor, viewer)

    Returns:
        Dependency function that checks user role
    """
    async def role_checker(current_user: Annotated[UserResponse, Depends(get_current_user)]) -> UserResponse:
        role_hierarchy = {UserRole.ADMIN: 3, UserRole.EDITOR: 2, UserRole.VIEWER: 1}

        user_level = role_hierarchy.get(current_user.role, 0)
        required_level = role_hierarchy.get(required_role, 999)

        if user_level < required_level:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. {required_role} role required."
            )

        return current_user

    return role_checker


@router.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Authenticate user and return JWT token.

    Args:
        form_data: OAuth2 password form with username (email) and password

    Returns:
        JWT access token

    Raises:
        HTTPException: If credentials are invalid
    """
    user = await auth_service.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.id, "email": user.email},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    current_user: Annotated[UserResponse, Depends(require_role(UserRole.ADMIN))]
):
    """Register a new user account (admin only).

    Args:
        user_data: User registration data
        current_user: Current authenticated admin user

    Returns:
        Created user

    Raises:
        HTTPException: If email already exists
    """
    try:
        user = await auth_service.create_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: Annotated[UserResponse, Depends(get_current_user)]
):
    """Get current authenticated user information.

    Args:
        current_user: Current authenticated user

    Returns:
        Current user data
    """
    return current_user


@router.get("/users", response_model=list[UserResponse])
async def list_users(
    current_user: Annotated[UserResponse, Depends(require_role(UserRole.ADMIN))]
):
    """List all users (admin only).

    Args:
        current_user: Current authenticated admin user

    Returns:
        List of all users
    """
    return await auth_service.list_users()


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    current_user: Annotated[UserResponse, Depends(require_role(UserRole.ADMIN))]
):
    """Delete user account (admin only).

    Args:
        user_id: User UUID to delete
        current_user: Current authenticated admin user

    Raises:
        HTTPException: If user not found or trying to delete self
    """
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )

    deleted = await auth_service.delete_user(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return None
