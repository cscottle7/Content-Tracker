"""Script to create initial admin user.

Run this script to create the first admin account for the system.
Usage: python -m app.scripts.create_admin
"""

import asyncio
import sys
from getpass import getpass

from app.models.user import UserCreate, UserRole
from app.services import auth_service


async def create_admin_user():
    """Interactive script to create admin user."""
    print("=" * 50)
    print("Create Initial Admin User")
    print("=" * 50)
    print()

    # Get user input
    email = input("Email address: ").strip()
    if not email or "@" not in email:
        print("Error: Invalid email address")
        sys.exit(1)

    full_name = input("Full name (optional): ").strip() or None

    password = getpass("Password (min 8 characters): ")
    if len(password) < 8:
        print("Error: Password must be at least 8 characters")
        sys.exit(1)

    password_confirm = getpass("Confirm password: ")
    if password != password_confirm:
        print("Error: Passwords do not match")
        sys.exit(1)

    # Create user
    user_data = UserCreate(
        email=email,
        full_name=full_name,
        password=password,
        role=UserRole.ADMIN,
    )

    try:
        user = await auth_service.create_user(user_data)
        print()
        print("✓ Admin user created successfully!")
        print(f"  Email: {user.email}")
        print(f"  Name: {user.full_name or 'Not provided'}")
        print(f"  Role: {user.role}")
        print(f"  User ID: {user.id}")
        print()
        print("You can now log in with these credentials.")

    except ValueError as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(create_admin_user())
