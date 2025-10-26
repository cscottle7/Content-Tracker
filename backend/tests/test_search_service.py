"""Tests for search_service module.

Tests search functionality including client filtering and unique value retrieval.
"""

import pytest
import tempfile
import sqlite3
from datetime import date
from pathlib import Path

from app.services.search_service import (
    index_content_item,
    search_content,
    get_unique_values,
    remove_from_index,
)
from app.models.content import ContentResponse


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """Create temporary database for testing."""
    db_file = tmp_path / "test_content_index.db"
    db_url = f"sqlite:///{db_file}"

    # Mock the database URL
    monkeypatch.setattr("app.services.search_service.settings.DATABASE_URL", db_url)

    # Initialize database schema
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

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

    cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS content_fts USING fts5(
            id UNINDEXED,
            title,
            description,
            body,
            tags
        )
    """)

    conn.commit()
    conn.close()

    return db_file


def test_index_content_with_client(temp_db):
    """Test indexing content with client field."""
    content = ContentResponse(
        id="test-123",
        file_path="/tmp/test.md",
        title="Test Content",
        content_type="blog",
        status="published",
        created_date=date(2024, 1, 15),
        updated_date=date(2024, 1, 20),
        author="Test Author",
        client="ClientA",
        tags=["test"],
        categories=["Testing"],
        custom_fields={},
        body="Sample body"
    )

    index_content_item(content)

    # Verify it was indexed
    results, total = search_content(query="Test")
    assert total == 1
    assert results[0].client == "ClientA"


def test_search_by_client(temp_db):
    """Test filtering content by client."""
    # Index content for different clients
    content1 = ContentResponse(
        id="test-1",
        file_path="/tmp/test1.md",
        title="Client A Content",
        content_type="blog",
        status="published",
        created_date=date(2024, 1, 15),
        updated_date=date(2024, 1, 15),
        client="ClientA",
        tags=[],
        categories=[],
        custom_fields={},
        body="Content for ClientA"
    )

    content2 = ContentResponse(
        id="test-2",
        file_path="/tmp/test2.md",
        title="Client B Content",
        content_type="blog",
        status="published",
        created_date=date(2024, 1, 15),
        updated_date=date(2024, 1, 15),
        client="ClientB",
        tags=[],
        categories=[],
        custom_fields={},
        body="Content for ClientB"
    )

    content3 = ContentResponse(
        id="test-3",
        file_path="/tmp/test3.md",
        title="No Client Content",
        content_type="blog",
        status="published",
        created_date=date(2024, 1, 15),
        updated_date=date(2024, 1, 15),
        client=None,
        tags=[],
        categories=[],
        custom_fields={},
        body="Content without client"
    )

    index_content_item(content1)
    index_content_item(content2)
    index_content_item(content3)

    # Search for ClientA content
    results, total = search_content(client="ClientA")
    assert total == 1
    assert results[0].id == "test-1"
    assert results[0].client == "ClientA"

    # Search for ClientB content
    results, total = search_content(client="ClientB")
    assert total == 1
    assert results[0].id == "test-2"
    assert results[0].client == "ClientB"

    # Search for all content (no client filter)
    results, total = search_content()
    assert total == 3


def test_get_unique_clients(temp_db):
    """Test getting unique client values."""
    # Index content for different clients
    clients_to_index = ["ClientA", "ClientB", "ClientA", "ClientC", None]

    for i, client in enumerate(clients_to_index):
        content = ContentResponse(
            id=f"test-{i}",
            file_path=f"/tmp/test{i}.md",
            title=f"Test {i}",
            content_type="blog",
            status="published",
            created_date=date(2024, 1, 15),
            updated_date=date(2024, 1, 15),
            client=client,
            tags=[],
            categories=[],
            custom_fields={},
            body="Test content"
        )
        index_content_item(content)

    # Get unique clients
    unique_clients = get_unique_values("client")

    # Should return 3 unique clients (ClientA, ClientB, ClientC) - None is filtered out
    assert len(unique_clients) == 3
    assert "ClientA" in unique_clients
    assert "ClientB" in unique_clients
    assert "ClientC" in unique_clients


def test_combined_client_and_type_filter(temp_db):
    """Test combining client filter with content_type filter."""
    # Index different content types for different clients
    content1 = ContentResponse(
        id="test-1",
        file_path="/tmp/test1.md",
        title="ClientA Blog",
        content_type="blog",
        status="published",
        created_date=date(2024, 1, 15),
        updated_date=date(2024, 1, 15),
        client="ClientA",
        tags=[],
        categories=[],
        custom_fields={},
        body="Blog content"
    )

    content2 = ContentResponse(
        id="test-2",
        file_path="/tmp/test2.md",
        title="ClientA Video",
        content_type="video",
        status="published",
        created_date=date(2024, 1, 15),
        updated_date=date(2024, 1, 15),
        client="ClientA",
        tags=[],
        categories=[],
        custom_fields={},
        body="Video content"
    )

    content3 = ContentResponse(
        id="test-3",
        file_path="/tmp/test3.md",
        title="ClientB Blog",
        content_type="blog",
        status="published",
        created_date=date(2024, 1, 15),
        updated_date=date(2024, 1, 15),
        client="ClientB",
        tags=[],
        categories=[],
        custom_fields={},
        body="Blog content"
    )

    index_content_item(content1)
    index_content_item(content2)
    index_content_item(content3)

    # Filter by ClientA and blog type
    results, total = search_content(client="ClientA", content_types=["blog"])
    assert total == 1
    assert results[0].id == "test-1"

    # Filter by ClientA (any type)
    results, total = search_content(client="ClientA")
    assert total == 2


def test_remove_from_index(temp_db):
    """Test removing content from index."""
    content = ContentResponse(
        id="test-remove",
        file_path="/tmp/test.md",
        title="To Remove",
        content_type="blog",
        status="published",
        created_date=date(2024, 1, 15),
        updated_date=date(2024, 1, 15),
        client="ClientA",
        tags=[],
        categories=[],
        custom_fields={},
        body="Content"
    )

    index_content_item(content)

    # Verify it exists
    results, total = search_content()
    assert total == 1

    # Remove it
    remove_from_index("test-remove")

    # Verify it's gone
    results, total = search_content()
    assert total == 0
