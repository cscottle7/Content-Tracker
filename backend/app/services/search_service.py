"""Search and filtering service for content items.

This service manages the SQLite index for fast searching and filtering.
It provides full-text search using FTS5 and metadata-based filtering.
"""

import sqlite3
import json
from typing import List, Optional, Dict, Tuple
from pathlib import Path
from datetime import date

from app.config import settings
from app.models.content import ContentResponse
from app.services.markdown_service import read_content_file


def get_db_connection():
    """Get SQLite database connection.

    Returns:
        sqlite3.Connection: Database connection with row factory configured
    """
    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn


def index_content_item(content: ContentResponse) -> None:
    """
    Add or update content item in SQLite index.

    Args:
        content: Content item to index
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT OR REPLACE INTO content_items (
                id, file_path, title, content_type, status, created_date, updated_date,
                publish_date, author, url, description, categories_json, tags_json,
                custom_fields_json, last_indexed
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """, (
            content.id,
            content.file_path,
            content.title,
            content.content_type,
            content.status,
            content.created_date.isoformat() if isinstance(content.created_date, date) else content.created_date,
            content.updated_date.isoformat() if isinstance(content.updated_date, date) else content.updated_date,
            content.publish_date.isoformat() if content.publish_date and isinstance(content.publish_date, date) else content.publish_date,
            content.author,
            content.url,
            content.description,
            json.dumps(content.categories),
            json.dumps(content.tags),
            json.dumps(content.custom_fields),
        ))

        # Update FTS index
        cursor.execute("""
            INSERT OR REPLACE INTO content_fts (id, title, description, body, tags)
            VALUES (?, ?, ?, ?, ?)
        """, (
            content.id,
            content.title,
            content.description or '',
            content.body or '',
            ' '.join(content.tags),
        ))

        conn.commit()
    finally:
        conn.close()


def remove_from_index(content_id: str) -> None:
    """Remove content item from SQLite index.

    Args:
        content_id: UUID of content item to remove
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM content_items WHERE id = ?", (content_id,))
        cursor.execute("DELETE FROM content_fts WHERE id = ?", (content_id,))
        conn.commit()
    finally:
        conn.close()


def search_content(
    query: Optional[str] = None,
    content_types: Optional[List[str]] = None,
    statuses: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
    client: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
) -> Tuple[List[ContentResponse], int]:
    """
    Search and filter content items.

    Args:
        query: Full-text search query
        content_types: Filter by content type(s)
        statuses: Filter by status(es)
        tags: Filter by tag(s)
        client: Filter by client (custom_fields.client)
        date_from: Filter by created_date >= this date
        date_to: Filter by created_date <= this date
        limit: Maximum results to return
        offset: Pagination offset

    Returns:
        Tuple of (list of matching content items, total count)
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Build query
        sql = "SELECT * FROM content_items WHERE 1=1"
        count_sql = "SELECT COUNT(*) FROM content_items WHERE 1=1"
        params = []

        if query:
            # Use FTS for full-text search
            sql += " AND id IN (SELECT id FROM content_fts WHERE content_fts MATCH ?)"
            count_sql += " AND id IN (SELECT id FROM content_fts WHERE content_fts MATCH ?)"
            params.append(query)

        if content_types:
            placeholders = ','.join('?' * len(content_types))
            sql += f" AND content_type IN ({placeholders})"
            count_sql += f" AND content_type IN ({placeholders})"
            params.extend(content_types)

        if statuses:
            placeholders = ','.join('?' * len(statuses))
            sql += f" AND status IN ({placeholders})"
            count_sql += f" AND status IN ({placeholders})"
            params.extend(statuses)

        if tags:
            # Match any tag (OR logic)
            tag_conditions = ' OR '.join([f"tags_json LIKE ?" for _ in tags])
            sql += f" AND ({tag_conditions})"
            count_sql += f" AND ({tag_conditions})"
            params.extend([f'%"{tag}"%' for tag in tags])

        if client:
            sql += " AND custom_fields_json LIKE ?"
            count_sql += " AND custom_fields_json LIKE ?"
            params.append(f'%"client": "{client}"%')

        if date_from:
            sql += " AND created_date >= ?"
            count_sql += " AND created_date >= ?"
            params.append(date_from)

        if date_to:
            sql += " AND created_date <= ?"
            count_sql += " AND created_date <= ?"
            params.append(date_to)

        # Get total count
        cursor.execute(count_sql, params)
        total = cursor.fetchone()[0]

        # Get paginated results
        sql += " ORDER BY updated_date DESC LIMIT ? OFFSET ?"
        cursor.execute(sql, params + [limit, offset])
        rows = cursor.fetchall()

        # Convert rows to ContentResponse objects
        results = []
        for row in rows:
            try:
                results.append(ContentResponse(
                    id=row['id'],
                    file_path=row['file_path'],
                    title=row['title'],
                    content_type=row['content_type'],
                    status=row['status'],
                    created_date=date.fromisoformat(row['created_date']) if row['created_date'] else date.today(),
                    updated_date=date.fromisoformat(row['updated_date']) if row['updated_date'] else date.today(),
                    publish_date=date.fromisoformat(row['publish_date']) if row['publish_date'] else None,
                    author=row['author'],
                    url=row['url'],
                    description=row['description'],
                    categories=json.loads(row['categories_json']) if row['categories_json'] else [],
                    tags=json.loads(row['tags_json']) if row['tags_json'] else [],
                    custom_fields=json.loads(row['custom_fields_json']) if row['custom_fields_json'] else {},
                ))
            except Exception as e:
                print(f"Error parsing row {row['id']}: {e}")
                continue

        return results, total
    finally:
        conn.close()


def rebuild_index_from_files() -> int:
    """
    Rebuild entire SQLite index from markdown files.

    Returns:
        Number of files indexed
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Clear existing index
        cursor.execute("DELETE FROM content_items")
        cursor.execute("DELETE FROM content_fts")
        conn.commit()

        # Scan content library
        content_library = Path(settings.CONTENT_LIBRARY_PATH)
        count = 0

        for md_file in content_library.rglob("*.md"):
            try:
                data = read_content_file(str(md_file))

                # Convert string dates to date objects if needed
                for key in ['created_date', 'updated_date', 'publish_date']:
                    if key in data and data[key] is not None:
                        if isinstance(data[key], str):
                            data[key] = date.fromisoformat(data[key])

                content = ContentResponse(file_path=str(md_file), **data)
                index_content_item(content)
                count += 1
            except Exception as e:
                print(f"Error indexing {md_file}: {e}")
                continue

        return count
    finally:
        conn.close()


def get_unique_values(field: str) -> List[str]:
    """
    Get unique values for a field (for filter dropdowns).

    Args:
        field: Field name (content_type, status, author, client)

    Returns:
        List of unique values
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if field in ['content_type', 'status', 'author']:
            cursor.execute(f"SELECT DISTINCT {field} FROM content_items WHERE {field} IS NOT NULL ORDER BY {field}")
            return [row[0] for row in cursor.fetchall()]
        elif field == 'client':
            # Extract unique clients from custom_fields_json
            cursor.execute("SELECT DISTINCT custom_fields_json FROM content_items WHERE custom_fields_json IS NOT NULL")
            clients = set()
            for row in cursor.fetchall():
                try:
                    custom_fields = json.loads(row[0])
                    if 'client' in custom_fields:
                        clients.add(custom_fields['client'])
                except:
                    continue
            return sorted(list(clients))
        else:
            return []
    finally:
        conn.close()
