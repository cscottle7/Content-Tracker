"""Export API endpoints for generating DOCX and PDF reports.

Provides endpoints for exporting filtered content items to various formats.
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import FileResponse
from typing import List, Optional
from pydantic import BaseModel

from app.models.content import ContentResponse
from app.services import search_service, export_service
from app.routers.auth import get_current_user
from app.models.user import UserResponse


router = APIRouter(prefix="/export", tags=["export"])


class ExportRequest(BaseModel):
    """Request model for export operations."""

    title: str = "Content Report"
    include_fields: Optional[List[str]] = None
    template_name: Optional[str] = None
    # Filter parameters
    query: Optional[str] = None
    content_types: Optional[List[str]] = None
    statuses: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    client: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None


class ExportResponse(BaseModel):
    """Response model for export operations."""

    file_path: str
    format: str
    item_count: int
    message: str


@router.post("/docx", response_model=ExportResponse)
async def export_docx(
    request: ExportRequest,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Export content items to DOCX format.

    Applies filters from request and generates a professional Word document.

    Requires authentication. All user roles can export.
    """
    try:
        # Get filtered content items
        content_items, total = search_service.search_content(
            query=request.query,
            content_types=request.content_types,
            statuses=request.statuses,
            tags=request.tags,
            client=request.client,
            date_from=request.date_from,
            date_to=request.date_to,
            limit=1000,  # Max items for export
            offset=0
        )

        if not content_items:
            raise HTTPException(status_code=404, detail="No content items found matching filters")

        # Generate DOCX
        file_path = await export_service.export_to_docx(
            content_items=content_items,
            title=request.title,
            include_fields=request.include_fields,
            template_name=request.template_name
        )

        return ExportResponse(
            file_path=file_path,
            format="docx",
            item_count=len(content_items),
            message=f"Successfully exported {len(content_items)} items to DOCX"
        )

    except HTTPException:
        # Re-raise HTTP exceptions (like 404) without wrapping
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


@router.post("/pdf", response_model=ExportResponse)
async def export_pdf(
    request: ExportRequest,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Export content items to PDF format.

    Applies filters from request and generates a professional PDF document.

    Requires authentication. All user roles can export.
    """
    try:
        # Get filtered content items
        content_items, total = search_service.search_content(
            query=request.query,
            content_types=request.content_types,
            statuses=request.statuses,
            tags=request.tags,
            client=request.client,
            date_from=request.date_from,
            date_to=request.date_to,
            limit=1000,  # Max items for export
            offset=0
        )

        if not content_items:
            raise HTTPException(status_code=404, detail="No content items found matching filters")

        # Generate PDF
        file_path = await export_service.export_to_pdf(
            content_items=content_items,
            title=request.title,
            include_fields=request.include_fields,
            template_name=request.template_name
        )

        return ExportResponse(
            file_path=file_path,
            format="pdf",
            item_count=len(content_items),
            message=f"Successfully exported {len(content_items)} items to PDF"
        )

    except HTTPException:
        # Re-raise HTTP exceptions (like 404) without wrapping
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


@router.get("/download/{filename}")
async def download_export(
    filename: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Download a generated export file.

    Args:
        filename: Name of the file to download (with extension)

    Returns:
        File download response

    Requires authentication. Files auto-delete after 1 hour.
    """
    from pathlib import Path
    from app.config import settings

    file_path = Path(settings.EXPORTS_PATH) / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Export file not found or expired")

    # Validate file is in exports directory (security)
    if not str(file_path.resolve()).startswith(str(Path(settings.EXPORTS_PATH).resolve())):
        raise HTTPException(status_code=403, detail="Access denied")

    # Determine media type
    media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    if filename.endswith('.pdf'):
        media_type = "application/pdf"

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type=media_type
    )


@router.delete("/cleanup")
async def cleanup_exports(
    max_age_hours: int = Query(1, ge=1, le=24, description="Maximum age of files to keep (hours)"),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Clean up old export files.

    Only accessible to admin users.

    Args:
        max_age_hours: Delete files older than this many hours

    Returns:
        Count of deleted files
    """
    # Check admin permission
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    deleted_count = await export_service.cleanup_old_exports(max_age_hours)

    return {
        "message": f"Cleaned up {deleted_count} export files",
        "deleted_count": deleted_count
    }
