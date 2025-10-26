"""API integration tests for export endpoints.

Tests the REST API endpoints for DOCX and PDF export operations.
"""

import pytest
from pathlib import Path
from fastapi.testclient import TestClient

from app.services import auth_service, markdown_service
from app.models.content import ContentCreate
from app.models.user import UserCreate


@pytest.fixture
def admin_token(client):
    """Create admin user and return auth token."""
    import uuid
    import asyncio

    # Use unique email to avoid conflicts
    email = f"admin_export_{uuid.uuid4().hex[:8]}@test.com"

    # Create admin user (run async function in sync context)
    loop = asyncio.get_event_loop()
    user = loop.run_until_complete(auth_service.create_user(
        UserCreate(
            email=email,
            password="adminpass123",
            full_name="Admin User",
            role="admin"
        )
    ))

    # Get token
    token = auth_service.create_access_token(data={"sub": user.id, "role": user.role})
    return token


@pytest.fixture
def sample_content_for_export(client, test_settings):
    """Create sample content items for export testing."""
    import asyncio

    # Create test content items
    items = []
    loop = asyncio.get_event_loop()
    for i in range(3):
        content = loop.run_until_complete(markdown_service.create_content_item(
            ContentCreate(
                title=f"Test Content {i+1}",
                content_type="blog" if i == 0 else "video",
                status="published",
                author=f"Author {i+1}",
                tags=["test", "export"],
                categories=["Testing"],
                body=f"Content body {i+1}"
            )
        ))
        items.append(content)

    return items


def test_export_docx_requires_auth(client):
    """Test that DOCX export requires authentication."""
    response = client.post("/export/docx", json={
        "title": "Test Report"
    })

    assert response.status_code == 401


def test_export_pdf_requires_auth(client):
    """Test that PDF export requires authentication."""
    response = client.post("/export/pdf", json={
        "title": "Test Report"
    })

    assert response.status_code == 401


def test_export_docx_success(client, admin_token, sample_content_for_export, test_settings):
    """Test successful DOCX export."""

    response = client.post(
        "/export/docx",
        json={
            "title": "Test DOCX Report",
            "include_fields": ["title", "content_type", "status", "author"]
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    if response.status_code != 200:
        print(f"\n\n{'='*80}\nERROR Response:")
        print(f"Status: {response.status_code}")
        print(f"Body: {response.text}")
        try:
            print(f"JSON: {response.json()}")
        except:
            pass
        print(f"{'='*80}\n\n")

    assert response.status_code == 200
    data = response.json()

    assert data["format"] == "docx"
    assert data["item_count"] == 3
    assert "file_path" in data
    assert data["file_path"].endswith(".docx")

    # Verify file exists
    file_path = Path(data["file_path"])
    assert file_path.exists()


def test_export_pdf_success(client, admin_token, sample_content_for_export, test_settings):
    """Test successful PDF export."""

    response = client.post(
        "/export/pdf",
        json={
            "title": "Test PDF Report",
            "include_fields": ["title", "content_type", "description"]
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["format"] == "pdf"
    assert data["item_count"] >= 3  # At least the 3 items from this fixture
    assert "file_path" in data
    # PDF export may fall back to HTML if WeasyPrint is not available
    assert data["file_path"].endswith(".pdf") or data["file_path"].endswith(".html")

    # Verify file exists
    file_path = Path(data["file_path"])
    assert file_path.exists()


def test_export_with_filters(client, admin_token, sample_content_for_export, test_settings):
    """Test export with content filters."""

    # Export only blog content
    response = client.post(
        "/export/docx",
        json={
            "title": "Blog Posts Only",
            "content_types": ["blog"]
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    data = response.json()

    # Should only export blog items (at least 1 from this fixture)
    assert data["item_count"] >= 1


def test_export_no_matching_content(client, admin_token, test_settings):
    """Test export when no content matches filters."""

    response = client.post(
        "/export/docx",
        json={
            "title": "No Results",
            "content_types": ["nonexistent"]
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    if response.status_code != 404:
        print(f"\n\nExpected 404, got {response.status_code}")
        print(f"Response: {response.json()}\n\n")

    assert response.status_code == 404
    assert "No content items found" in response.json()["detail"]


def test_download_export_file(client, admin_token, test_settings):
    """Test downloading an export file."""
    # Create a test file
    test_file = test_settings.EXPORTS_PATH / "test-export.docx"
    test_file.write_text("test content")

    response = client.get(
        "/export/download/test-export.docx",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def test_download_nonexistent_file(client, admin_token):
    """Test downloading a file that doesn't exist."""
    response = client.get(
        "/export/download/nonexistent.docx",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 404


def test_download_requires_auth(client):
    """Test that download requires authentication."""
    response = client.get("/export/download/test.docx")

    assert response.status_code == 401


def test_cleanup_exports_admin_only(client, admin_token, test_settings):
    """Test that cleanup is admin-only."""
    # Create old test files
    old_file = test_settings.EXPORTS_PATH / "old_export.docx"
    old_file.touch()

    import time, os
    old_time = time.time() - (2 * 3600)
    os.utime(old_file, (old_time, old_time))

    response = client.delete(
        "/export/cleanup?max_age_hours=1",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["deleted_count"] == 1


def test_cleanup_exports_non_admin_forbidden(client):
    """Test that non-admin users cannot cleanup exports."""
    import uuid
    import asyncio

    # Create editor user with unique email
    email = f"editor_export_{uuid.uuid4().hex[:8]}@test.com"
    loop = asyncio.get_event_loop()
    user = loop.run_until_complete(auth_service.create_user(
        UserCreate(
            email=email,
            password="editorpass123",
            role="editor"
        )
    ))

    token = auth_service.create_access_token(data={"sub": user.id, "role": user.role})

    response = client.delete(
        "/export/cleanup?max_age_hours=1",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403
    assert "Admin access required" in response.json()["detail"]
