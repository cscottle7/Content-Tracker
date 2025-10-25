"""Content API routes for CRUD operations.

This module provides REST API endpoints for creating, reading,
updating, and deleting content items, plus list/search functionality.
"""

from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional

from app.models.content import ContentCreate, ContentUpdate, ContentResponse
from app.services import markdown_service, search_service


router = APIRouter(prefix="/content", tags=["content"])


@router.post("", response_model=ContentResponse, status_code=status.HTTP_201_CREATED)
async def create_content(content_data: ContentCreate):
    """
    Create new content item.

    Stores item as markdown file with YAML frontmatter in the content library.
    Returns the created content item with generated ID and timestamps.

    Args:
        content_data: Content creation data including title, type, and body

    Returns:
        Created content item with all metadata
    """
    return await markdown_service.create_content_item(content_data)


@router.get("/{content_id}", response_model=ContentResponse)
async def get_content(content_id: str):
    """
    Retrieve content item by ID.

    Args:
        content_id: UUID of the content item

    Returns:
        Content item with all metadata and body

    Raises:
        HTTPException: 404 if content not found
    """
    content = await markdown_service.get_content_item(content_id)
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content item with ID '{content_id}' not found"
        )
    return content


@router.put("/{content_id}", response_model=ContentResponse)
async def update_content(content_id: str, updates: ContentUpdate):
    """
    Update existing content item.

    Only provided fields are updated; others remain unchanged.
    Updates the updated_date timestamp automatically.

    Args:
        content_id: UUID of the content item
        updates: Fields to update (all optional)

    Returns:
        Updated content item

    Raises:
        HTTPException: 404 if content not found
    """
    content = await markdown_service.update_content_item(content_id, updates)
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content item with ID '{content_id}' not found"
        )
    return content


@router.delete("/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_content(content_id: str):
    """
    Delete content item.

    Removes markdown file from content library.
    This operation cannot be undone.

    Args:
        content_id: UUID of the content item

    Raises:
        HTTPException: 404 if content not found
    """
    deleted = await markdown_service.delete_content_item(content_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content item with ID '{content_id}' not found"
        )
    return None


@router.get("", response_model=dict)
async def list_content(
    q: Optional[str] = Query(None, description="Search query"),
    content_type: Optional[List[str]] = Query(None),
    status: Optional[List[str]] = Query(None),
    tags: Optional[List[str]] = Query(None),
    client: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100)
):
    """
    List and filter content items.

    Supports full-text search, filtering by multiple criteria, and pagination.

    Args:
        q: Full-text search query
        content_type: Filter by content type(s)
        status: Filter by status(es)
        tags: Filter by tag(s)
        client: Filter by client name
        date_from: Filter by created_date >= this date (YYYY-MM-DD)
        date_to: Filter by created_date <= this date (YYYY-MM-DD)
        page: Page number (1-indexed)
        per_page: Items per page (max 100)

    Returns:
        Dictionary with 'items' list and 'pagination' metadata
    """
    offset = (page - 1) * per_page

    results, total = search_service.search_content(
        query=q,
        content_types=content_type,
        statuses=status,
        tags=tags,
        client=client,
        date_from=date_from,
        date_to=date_to,
        limit=per_page,
        offset=offset
    )

    return {
        "items": results,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page  # Ceiling division
        }
    }
