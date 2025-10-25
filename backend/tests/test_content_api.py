"""API integration tests for content endpoints.

Tests the REST API endpoints for content CRUD operations.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import date

from app.main import app
from app.services.markdown_service import create_content_item
from app.models.content import ContentCreate


client = TestClient(app)


@pytest.fixture
def mock_settings(tmp_path, monkeypatch):
    """Mock settings to use temporary directory."""
    content_dir = tmp_path / "content_library"
    content_dir.mkdir()
    monkeypatch.setattr("app.services.markdown_service.settings.CONTENT_LIBRARY_PATH", content_dir)
    return content_dir


@pytest.fixture
async def created_content_id(mock_settings):
    """Create a content item for testing and return its ID."""
    content_data = ContentCreate(
        title="Test Content for API",
        content_type="blog",
        status="draft",
        body="Test body content"
    )
    created = await create_content_item(content_data)
    return created.id


def test_health_endpoint():
    """Test that health check endpoint works."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_create_content(mock_settings):
    """Test POST /content endpoint."""
    response = client.post("/content", json={
        "title": "API Test Post",
        "content_type": "blog",
        "status": "draft",
        "body": "Test content from API"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "API Test Post"
    assert data["content_type"] == "blog"
    assert data["status"] == "draft"
    assert "id" in data
    assert "created_date" in data
    assert "updated_date" in data


def test_create_content_with_all_fields(mock_settings):
    """Test creating content with all optional fields."""
    response = client.post("/content", json={
        "title": "Complete Content",
        "content_type": "video",
        "status": "published",
        "author": "Test Author",
        "url": "https://example.com/video",
        "description": "Test description",
        "publish_date": "2024-01-15",
        "categories": ["Tech", "Tutorial"],
        "tags": ["python", "fastapi"],
        "custom_fields": {"duration": "10:30"},
        "body": "Video transcript here"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["author"] == "Test Author"
    assert data["url"] == "https://example.com/video"
    assert "Tech" in data["categories"]
    assert "python" in data["tags"]
    assert data["custom_fields"]["duration"] == "10:30"


def test_create_content_missing_required_fields():
    """Test that creating content without required fields fails."""
    response = client.post("/content", json={
        "status": "draft"
        # Missing title and content_type
    })
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_get_content(mock_settings, created_content_id):
    """Test GET /content/{id} endpoint."""
    response = client.get(f"/content/{created_content_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_content_id
    assert data["title"] == "Test Content for API"


def test_get_nonexistent_content(mock_settings):
    """Test getting content that doesn't exist."""
    response = client.get("/content/nonexistent-id")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_update_content(mock_settings, created_content_id):
    """Test PUT /content/{id} endpoint."""
    response = client.put(f"/content/{created_content_id}", json={
        "title": "Updated Title",
        "status": "published"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["status"] == "published"
    assert data["content_type"] == "blog"  # Unchanged


@pytest.mark.asyncio
async def test_update_content_body(mock_settings, created_content_id):
    """Test updating content body."""
    response = client.put(f"/content/{created_content_id}", json={
        "body": "# Updated Content\n\nNew body text."
    })
    assert response.status_code == 200
    data = response.json()
    assert "Updated Content" in data["body"]


def test_update_nonexistent_content(mock_settings):
    """Test updating content that doesn't exist."""
    response = client.put("/content/nonexistent-id", json={
        "title": "Updated Title"
    })
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_content(mock_settings, created_content_id):
    """Test DELETE /content/{id} endpoint."""
    response = client.delete(f"/content/{created_content_id}")
    assert response.status_code == 204

    # Verify deletion
    response = client.get(f"/content/{created_content_id}")
    assert response.status_code == 404


def test_delete_nonexistent_content(mock_settings):
    """Test deleting content that doesn't exist."""
    response = client.delete("/content/nonexistent-id")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_content_lifecycle(mock_settings):
    """Test full CRUD lifecycle."""
    # Create
    create_response = client.post("/content", json={
        "title": "Lifecycle Test",
        "content_type": "blog",
        "body": "Original content"
    })
    assert create_response.status_code == 201
    content_id = create_response.json()["id"]

    # Read
    get_response = client.get(f"/content/{content_id}")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Lifecycle Test"

    # Update
    update_response = client.put(f"/content/{content_id}", json={
        "title": "Updated Lifecycle Test",
        "body": "Updated content"
    })
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated Lifecycle Test"

    # Delete
    delete_response = client.delete(f"/content/{content_id}")
    assert delete_response.status_code == 204

    # Verify deletion
    final_get = client.get(f"/content/{content_id}")
    assert final_get.status_code == 404
