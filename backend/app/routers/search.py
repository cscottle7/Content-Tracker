"""Search API routes for content discovery.

This module provides dedicated search endpoints for finding content
across the library using full-text search and advanced filtering.
"""

from fastapi import APIRouter, Query
from typing import Optional, List

from app.models.content import ContentResponse
from app.services import search_service


router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=List[ContentResponse])
async def search(
    q: str = Query(..., min_length=1, description="Search query"),
    content_type: Optional[List[str]] = Query(None),
    status: Optional[List[str]] = Query(None),
    tags: Optional[List[str]] = Query(None),
    client: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100)
):
    """
    Full-text search across content items.

    Searches title, description, body, and tags for the provided query.
    Results can be filtered by content type, status, tags, and client.

    Args:
        q: Search query (required)
        content_type: Filter by content type(s)
        status: Filter by status(es)
        tags: Filter by tag(s)
        client: Filter by client name
        limit: Maximum results to return (default 20, max 100)

    Returns:
        List of matching content items
    """
    results, _ = search_service.search_content(
        query=q,
        content_types=content_type,
        statuses=status,
        tags=tags,
        client=client,
        limit=limit,
        offset=0
    )

    return results


@router.get("/filters", response_model=dict)
async def get_filter_options():
    """
    Get available filter options for the search interface.

    Returns unique values for content types, statuses, authors, and clients
    to populate filter dropdowns in the frontend.

    Returns:
        Dictionary with filter options for each field
    """
    return {
        "content_types": search_service.get_unique_values("content_type"),
        "statuses": search_service.get_unique_values("status"),
        "authors": search_service.get_unique_values("author"),
        "clients": search_service.get_unique_values("client")
    }


@router.post("/rebuild-index")
async def rebuild_index():
    """
    Rebuild the search index from all markdown files.

    This endpoint scans the entire content library and recreates the
    SQLite index. Useful after bulk file operations or manual edits.

    Returns:
        Dictionary with count of indexed files
    """
    count = search_service.rebuild_index_from_files()
    return {
        "message": "Index rebuilt successfully",
        "files_indexed": count
    }
