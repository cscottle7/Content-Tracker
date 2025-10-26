"""Tests for markdown_service module.

Tests CRUD operations for content items stored as markdown files
with YAML frontmatter.
"""

import pytest
import tempfile
import os
from datetime import date
from pathlib import Path

from app.services.markdown_service import (
    read_content_file,
    write_content_file,
    create_content_item,
    get_content_item,
    update_content_item,
    delete_content_item,
)
from app.models.content import ContentCreate, ContentUpdate


@pytest.fixture
def temp_content_dir(tmp_path):
    """Create temporary content library directory."""
    content_dir = tmp_path / "content_library"
    content_dir.mkdir()
    return content_dir


@pytest.fixture
def mock_settings(temp_content_dir, monkeypatch):
    """Mock settings to use temporary directory."""
    monkeypatch.setattr("app.services.markdown_service.settings.CONTENT_LIBRARY_PATH", temp_content_dir)


@pytest.mark.asyncio
async def test_create_and_read_content(mock_settings):
    """Test creating a content item and reading it back."""
    content_data = ContentCreate(
        title="Test Blog Post",
        content_type="blog",
        status="draft",
        author="Test Author",
        tags=["test", "sample"],
        body="# Test Content\n\nThis is a test."
    )

    created = await create_content_item(content_data)
    assert created.id is not None
    assert created.title == "Test Blog Post"
    assert created.status == "draft"
    assert created.author == "Test Author"
    assert "test" in created.tags
    assert created.body == "# Test Content\n\nThis is a test."

    retrieved = await get_content_item(created.id)
    assert retrieved is not None
    assert retrieved.title == "Test Blog Post"
    assert "This is a test" in retrieved.body


@pytest.mark.asyncio
async def test_create_content_with_all_fields(mock_settings):
    """Test creating content with all optional fields."""
    content_data = ContentCreate(
        title="Complete Content Item",
        content_type="video",
        status="published",
        author="John Doe",
        url="https://example.com/video",
        description="A comprehensive test video",
        publish_date=date(2024, 1, 15),
        categories=["Tutorial", "Tech"],
        tags=["python", "fastapi"],
        custom_fields={"duration": "10:30", "platform": "YouTube"},
        body="Video description and transcript here."
    )

    created = await create_content_item(content_data)
    assert created.description == "A comprehensive test video"
    assert created.url == "https://example.com/video"
    assert created.publish_date == date(2024, 1, 15)
    assert "Tutorial" in created.categories
    assert created.custom_fields["duration"] == "10:30"


@pytest.mark.asyncio
async def test_update_content(mock_settings):
    """Test updating content item."""
    created = await create_content_item(ContentCreate(
        title="Original Title",
        content_type="blog",
        body="Original body"
    ))

    updates = ContentUpdate(title="Updated Title", body="Updated body")
    updated = await update_content_item(created.id, updates)

    assert updated is not None
    assert updated.title == "Updated Title"
    assert updated.body == "Updated body"
    assert updated.updated_date >= created.updated_date


@pytest.mark.asyncio
async def test_update_partial_fields(mock_settings):
    """Test updating only specific fields."""
    created = await create_content_item(ContentCreate(
        title="Original Title",
        content_type="blog",
        status="draft",
        tags=["original"],
        body="Original body"
    ))

    updates = ContentUpdate(status="published", tags=["updated", "new"])
    updated = await update_content_item(created.id, updates)

    assert updated is not None
    assert updated.title == "Original Title"  # Unchanged
    assert updated.status == "published"  # Updated
    assert "updated" in updated.tags  # Updated
    assert updated.body == "Original body"  # Unchanged


@pytest.mark.asyncio
async def test_delete_content(mock_settings):
    """Test deleting content item."""
    created = await create_content_item(ContentCreate(
        title="To Be Deleted",
        content_type="blog",
        body="Test"
    ))

    deleted = await delete_content_item(created.id)
    assert deleted is True

    retrieved = await get_content_item(created.id)
    assert retrieved is None


@pytest.mark.asyncio
async def test_delete_nonexistent_content(mock_settings):
    """Test deleting content that doesn't exist."""
    deleted = await delete_content_item("nonexistent-id")
    assert deleted is False


@pytest.mark.asyncio
async def test_get_nonexistent_content(mock_settings):
    """Test retrieving content that doesn't exist."""
    retrieved = await get_content_item("nonexistent-id")
    assert retrieved is None


@pytest.mark.asyncio
async def test_update_nonexistent_content(mock_settings):
    """Test updating content that doesn't exist."""
    updates = ContentUpdate(title="New Title")
    updated = await update_content_item("nonexistent-id", updates)
    assert updated is None


def test_read_write_content_file(tmp_path):
    """Test low-level file read/write operations."""
    file_path = tmp_path / "test.md"

    frontmatter = {
        'id': 'test-123',
        'title': 'Test Title',
        'tags': ['test', 'sample'],
        'created_date': '2024-01-15'
    }
    body = "# Test Heading\n\nTest body content."

    write_content_file(str(file_path), frontmatter, body)

    assert file_path.exists()

    data = read_content_file(str(file_path))
    assert data['id'] == 'test-123'
    assert data['title'] == 'Test Title'
    assert 'test' in data['tags']
    assert data['body'] == "# Test Heading\n\nTest body content."


def test_read_file_without_frontmatter(tmp_path):
    """Test reading markdown file without frontmatter."""
    file_path = tmp_path / "no_frontmatter.md"

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("# Just Content\n\nNo frontmatter here.")

    data = read_content_file(str(file_path))
    assert 'body' in data
    assert "Just Content" in data['body']


@pytest.mark.asyncio
async def test_create_content_with_client(mock_settings):
    """Test creating content with client field."""
    content_data = ContentCreate(
        title="Client Content",
        content_type="blog",
        client="TestClient",
        body="Content for TestClient"
    )

    created = await create_content_item(content_data)
    assert created.client == "TestClient"

    # Verify it can be retrieved
    retrieved = await get_content_item(created.id)
    assert retrieved is not None
    assert retrieved.client == "TestClient"


@pytest.mark.asyncio
async def test_update_client_field(mock_settings):
    """Test updating the client field."""
    created = await create_content_item(ContentCreate(
        title="Original Content",
        content_type="blog",
        client="OriginalClient",
        body="Test content"
    ))

    # Update client
    updates = ContentUpdate(client="UpdatedClient")
    updated = await update_content_item(created.id, updates)

    assert updated is not None
    assert updated.client == "UpdatedClient"
    assert updated.title == "Original Content"  # Other fields unchanged


@pytest.mark.asyncio
async def test_create_content_without_client(mock_settings):
    """Test creating content without client field (should be None)."""
    content_data = ContentCreate(
        title="No Client Content",
        content_type="blog",
        body="Content without client"
    )

    created = await create_content_item(content_data)
    assert created.client is None
