"""Database initialization and schema setup.

Creates SQLite databases for content indexing and user management.
"""

import asyncio
import sqlite3
from pathlib import Path

from app.config import settings


def create_content_index_db():
    """Create content metadata index database with FTS5 support."""
    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create main content metadata table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS content_items (
            id TEXT PRIMARY KEY,
            file_path TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            content_type TEXT NOT NULL,
            status TEXT,
            created_date DATE,
            updated_date DATE,
            publish_date DATE,
            author TEXT,
            client TEXT,
            url TEXT,
            description TEXT,
            categories_json TEXT,
            tags_json TEXT,
            custom_fields_json TEXT,
            body_preview TEXT,
            last_indexed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create indexes for common queries
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_content_type
        ON content_items(content_type)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_status
        ON content_items(status)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_created_date
        ON content_items(created_date)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_publish_date
        ON content_items(publish_date)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_client
        ON content_items(client)
    """)

    # Create FTS5 virtual table for full-text search
    # Note: This is a standalone FTS table, not linked to content_items
    # Index is managed manually by search_service.py
    cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS content_fts USING fts5(
            id UNINDEXED,
            title,
            description,
            body,
            tags
        )
    """)

    # Note: FTS index is managed manually by search_service.py
    # Triggers are not used to avoid complexity with body content syncing

    conn.commit()
    conn.close()

    print(f"[OK] Content index database created at {db_file}")


def create_users_db():
    """Create user accounts database for authentication (post-MVP)."""
    db_path = settings.USERS_DATABASE_URL.replace("sqlite:///", "")
    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    """)

    # Create indexes
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_user_email
        ON users(email)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_user_role
        ON users(role)
    """)

    conn.commit()
    conn.close()

    print(f"[OK] Users database created at {db_file}")


async def init_database():
    """Initialize all required databases.

    Called during application startup.
    """
    create_content_index_db()
    create_users_db()
    print("[OK] All databases initialized successfully")


if __name__ == "__main__":
    # Allow running as standalone script
    asyncio.run(init_database())
