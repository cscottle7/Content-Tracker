"""Content item data models using Pydantic.

Defines the structure for content items stored as markdown files
with YAML frontmatter and used throughout the API.
"""

from datetime import date, datetime
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ContentBase(BaseModel):
    """Base content model with common fields."""

    title: str = Field(..., min_length=1, max_length=500)
    content_type: str = Field(..., description="Type of content (blog, video, podcast, etc.)")
    status: str = Field(default="draft", description="Content status (draft, published, archived)")
    description: Optional[str] = Field(None, max_length=2000)
    author: Optional[str] = Field(None, max_length=200)
    url: Optional[str] = Field(None, max_length=1000)
    publish_date: Optional[date] = None
    categories: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    custom_fields: Dict[str, Any] = Field(default_factory=dict)


class ContentCreate(ContentBase):
    """Model for creating new content items."""

    body: str = Field(default="", description="Markdown body content")


class ContentUpdate(BaseModel):
    """Model for updating existing content items.

    All fields are optional to support partial updates.
    """

    title: Optional[str] = Field(None, min_length=1, max_length=500)
    content_type: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = Field(None, max_length=2000)
    author: Optional[str] = Field(None, max_length=200)
    url: Optional[str] = Field(None, max_length=1000)
    publish_date: Optional[date] = None
    categories: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    custom_fields: Optional[Dict[str, Any]] = None
    body: Optional[str] = None


class ContentResponse(ContentBase):
    """Model for content item API responses."""

    id: str = Field(..., description="Unique content item ID")
    created_date: date
    updated_date: date
    file_path: str = Field(..., description="Relative path to markdown file")
    body: str = Field(default="", description="Markdown body content")

    model_config = {"from_attributes": True}


class ContentListItem(ContentBase):
    """Lightweight model for content list views (without body)."""

    id: str
    created_date: date
    updated_date: date
    file_path: str

    model_config = {"from_attributes": True}


class ContentFilter(BaseModel):
    """Model for filtering content items."""

    content_type: Optional[str] = None
    status: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    tag: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    search_query: Optional[str] = None


class ContentListResponse(BaseModel):
    """Paginated response for content list endpoints."""

    items: List[ContentListItem]
    total: int
    page: int
    page_size: int
    total_pages: int
