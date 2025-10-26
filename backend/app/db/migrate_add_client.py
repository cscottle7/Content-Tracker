"""Migration script to add client column to existing content_items table.

Run this script once to add the client field support to an existing database.
"""

import sqlite3
from pathlib import Path

from app.config import settings


def migrate_add_client_column():
    """Add client column to content_items table if it doesn't exist."""
    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    db_file = Path(db_path)

    if not db_file.exists():
        print(f"[INFO] Database {db_file} does not exist. No migration needed.")
        return

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Check if client column already exists
    cursor.execute("PRAGMA table_info(content_items)")
    columns = [row[1] for row in cursor.fetchall()]

    if "client" in columns:
        print("[INFO] Client column already exists. No migration needed.")
        conn.close()
        return

    print("[INFO] Adding client column to content_items table...")

    # Add client column (SQLite allows adding columns with ALTER TABLE)
    cursor.execute("""
        ALTER TABLE content_items
        ADD COLUMN client TEXT
    """)

    # Create index for client column
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_client
        ON content_items(client)
    """)

    conn.commit()
    conn.close()

    print("[OK] Client column added successfully!")
    print("[INFO] Existing content items will have NULL client values until updated.")


if __name__ == "__main__":
    migrate_add_client_column()
