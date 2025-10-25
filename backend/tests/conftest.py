"""Pytest configuration and shared fixtures for backend tests."""

import os
import tempfile
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.config import Settings, settings
from app.main import app


@pytest.fixture(scope="session")
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture(scope="session")
def test_settings(temp_dir: Path) -> Settings:
    """Override settings for testing."""
    test_settings = Settings(
        CONTENT_LIBRARY_PATH=temp_dir / "content_library",
        EXPORTS_PATH=temp_dir / "exports",
        DATABASE_URL=f"sqlite:///{temp_dir}/test_content_index.db",
        USERS_DATABASE_URL=f"sqlite:///{temp_dir}/test_users.db",
        DEBUG=True,
    )

    # Create test directories
    test_settings.CONTENT_LIBRARY_PATH.mkdir(parents=True, exist_ok=True)
    test_settings.EXPORTS_PATH.mkdir(parents=True, exist_ok=True)

    return test_settings


@pytest.fixture
def client(test_settings: Settings) -> Generator[TestClient, None, None]:
    """Create a test client for FastAPI application."""
    # Override settings for tests
    app.dependency_overrides[settings] = lambda: test_settings

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_content_data() -> dict:
    """Sample content item data for testing."""
    return {
        "title": "Test Blog Post",
        "content_type": "blog",
        "status": "published",
        "description": "A test blog post for unit testing",
        "author": "Test Author",
        "url": "https://example.com/test-blog-post",
        "categories": ["Testing", "Development"],
        "tags": ["pytest", "fastapi", "testing"],
        "body": "# Test Content\n\nThis is a test blog post.",
    }
