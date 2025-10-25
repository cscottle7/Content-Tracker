"""Authentication and user management service.

Handles user authentication, JWT token generation, and password hashing.
Implements role-based access control for admin/editor/viewer roles.
"""

from datetime import datetime, timedelta
from typing import Optional
import sqlite3
from uuid import uuid4

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings
from app.models.user import UserCreate, UserResponse, UserInDB

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_users_db_connection():
    """Get SQLite database connection for users database.

    Returns:
        sqlite3.Connection: Database connection with row factory configured
    """
    db_path = settings.USERS_DATABASE_URL.replace("sqlite:///", "")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash.

    Args:
        plain_password: Plain text password
        hashed_password: Hashed password from database

    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token.

    Args:
        data: Payload data to encode in token
        expires_delta: Token expiration time (default: 30 minutes)

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """Decode and verify JWT access token.

    Args:
        token: JWT token string

    Returns:
        Decoded token payload or None if invalid
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


async def create_user(user_data: UserCreate) -> UserResponse:
    """Create a new user account.

    Args:
        user_data: User registration data

    Returns:
        Created user (without password hash)

    Raises:
        ValueError: If email already exists
    """
    conn = get_users_db_connection()
    cursor = conn.cursor()

    try:
        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (user_data.email,))
        if cursor.fetchone():
            raise ValueError(f"User with email {user_data.email} already exists")

        user_id = str(uuid4())
        password_hash = get_password_hash(user_data.password)

        cursor.execute("""
            INSERT INTO users (id, email, password_hash, full_name, role, is_active)
            VALUES (?, ?, ?, ?, ?, 1)
        """, (
            user_id,
            user_data.email,
            password_hash,
            user_data.full_name,
            user_data.role,
        ))

        conn.commit()

        # Fetch created user
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()

        return UserResponse(
            id=row["id"],
            email=row["email"],
            full_name=row["full_name"],
            role=row["role"],
            created_at=row["created_at"],
            last_login=row["last_login"],
            is_active=bool(row["is_active"]),
        )

    finally:
        conn.close()


async def get_user_by_email(email: str) -> Optional[UserInDB]:
    """Get user by email address.

    Args:
        email: User email address

    Returns:
        User with password hash or None if not found
    """
    conn = get_users_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()

        if not row:
            return None

        return UserInDB(
            id=row["id"],
            email=row["email"],
            password_hash=row["password_hash"],
            full_name=row["full_name"],
            role=row["role"],
            created_at=row["created_at"],
            last_login=row["last_login"],
            is_active=bool(row["is_active"]),
        )

    finally:
        conn.close()


async def get_user_by_id(user_id: str) -> Optional[UserResponse]:
    """Get user by ID.

    Args:
        user_id: User UUID

    Returns:
        User (without password hash) or None if not found
    """
    conn = get_users_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()

        if not row:
            return None

        return UserResponse(
            id=row["id"],
            email=row["email"],
            full_name=row["full_name"],
            role=row["role"],
            created_at=row["created_at"],
            last_login=row["last_login"],
            is_active=bool(row["is_active"]),
        )

    finally:
        conn.close()


async def authenticate_user(email: str, password: str) -> Optional[UserInDB]:
    """Authenticate user with email and password.

    Args:
        email: User email
        password: Plain text password

    Returns:
        User if authentication successful, None otherwise
    """
    user = await get_user_by_email(email)
    if not user:
        return None
    if not user.is_active:
        return None
    if not verify_password(password, user.password_hash):
        return None

    # Update last login timestamp
    conn = get_users_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE users SET last_login = datetime('now') WHERE id = ?",
            (user.id,)
        )
        conn.commit()
    finally:
        conn.close()

    return user


async def update_user(user_id: str, **updates) -> Optional[UserResponse]:
    """Update user fields.

    Args:
        user_id: User UUID
        **updates: Fields to update (role, full_name, is_active)

    Returns:
        Updated user or None if not found
    """
    conn = get_users_db_connection()
    cursor = conn.cursor()

    try:
        # Build update query
        allowed_fields = ["role", "full_name", "is_active"]
        update_fields = {k: v for k, v in updates.items() if k in allowed_fields}

        if not update_fields:
            # No valid updates provided, just return current user
            return await get_user_by_id(user_id)

        set_clause = ", ".join([f"{field} = ?" for field in update_fields.keys()])
        values = list(update_fields.values()) + [user_id]

        cursor.execute(f"UPDATE users SET {set_clause} WHERE id = ?", values)
        conn.commit()

        if cursor.rowcount == 0:
            return None

        return await get_user_by_id(user_id)

    finally:
        conn.close()


async def list_users() -> list[UserResponse]:
    """List all users (admin only).

    Returns:
        List of all users in system
    """
    conn = get_users_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
        rows = cursor.fetchall()

        return [
            UserResponse(
                id=row["id"],
                email=row["email"],
                full_name=row["full_name"],
                role=row["role"],
                created_at=row["created_at"],
                last_login=row["last_login"],
                is_active=bool(row["is_active"]),
            )
            for row in rows
        ]

    finally:
        conn.close()


async def delete_user(user_id: str) -> bool:
    """Delete user account (admin only).

    Args:
        user_id: User UUID

    Returns:
        True if deleted, False if not found
    """
    conn = get_users_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return cursor.rowcount > 0

    finally:
        conn.close()
