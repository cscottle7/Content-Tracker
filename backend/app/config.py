"""Configuration settings for Content Tracking System.

Loads configuration from environment variables with sensible defaults.
Uses pydantic-settings for validation and type safety.
"""

from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "Content Tracking System"
    DEBUG: bool = False

    # Paths
    CONTENT_LIBRARY_PATH: Path = Path("/app/content_library")
    EXPORTS_PATH: Path = Path("/app/exports")

    # Database
    DATABASE_URL: str = "sqlite:///app/data/content_index.db"
    USERS_DATABASE_URL: str = "sqlite:///app/data/users.db"

    # Security (JWT for post-MVP)
    SECRET_KEY: str = "development-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://frontend:3000",
    ]

    # Pagination
    DEFAULT_PAGE_SIZE: int = 50
    MAX_PAGE_SIZE: int = 200

    # Export
    EXPORT_CLEANUP_HOURS: int = 1
    MAX_EXPORT_ITEMS: int = 1000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# Global settings instance
settings = Settings()


# Ensure required directories exist
def ensure_directories():
    """Create required directories if they don't exist."""
    settings.CONTENT_LIBRARY_PATH.mkdir(parents=True, exist_ok=True)
    settings.EXPORTS_PATH.mkdir(parents=True, exist_ok=True)
    (settings.EXPORTS_PATH / "templates").mkdir(parents=True, exist_ok=True)

    # Create content type directories
    content_types = ["blog", "video", "podcast", "social", "research", "content-plans", "website-content"]
    for content_type in content_types:
        (settings.CONTENT_LIBRARY_PATH / content_type).mkdir(parents=True, exist_ok=True)


ensure_directories()
