"""User and authentication data models.

Defines user accounts, roles, and authentication-related models.
Post-MVP implementation.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserRole:
    """User role constants."""

    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


class UserBase(BaseModel):
    """Base user model with common fields."""

    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=200)
    role: str = Field(default=UserRole.VIEWER)


class UserCreate(UserBase):
    """Model for creating new user accounts."""

    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """Model for updating user accounts.

    All fields are optional to support partial updates.
    """

    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=200)
    role: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """Model for user API responses (without password)."""

    id: str
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool = True

    model_config = {"from_attributes": True}


class UserInDB(UserResponse):
    """User model with password hash (for internal use only)."""

    password_hash: str


class Token(BaseModel):
    """JWT token response model."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Data extracted from JWT token."""

    user_id: Optional[str] = None
    email: Optional[str] = None
