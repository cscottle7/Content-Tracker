"""Markdown file service for content management.

This service handles reading and writing content items as markdown files
with YAML frontmatter. Each content item is stored as a separate .md file
with metadata in the frontmatter and body content in markdown format.
"""

import os
import yaml
from pathlib import Path
from datetime import date
from typing import Optional, Dict
from uuid import uuid4

from app.config import settings
from app.models.content import ContentCreate, ContentUpdate, ContentResponse


def _get_content_file_path(content_id: str, content_type: str) -> str:
    """
    Construct file path for content item.

    Args:
        content_id: UUID of content item
        content_type: Type of content (blog, video, etc.)

    Returns:
        Absolute path to markdown file
    """
    content_dir = Path(settings.CONTENT_LIBRARY_PATH) / content_type
    content_dir.mkdir(parents=True, exist_ok=True)
    return str(content_dir / f"{content_id}.md")


def read_content_file(file_path: str) -> Dict:
    """
    Read markdown file and parse YAML frontmatter.

    Args:
        file_path: Absolute path to markdown file

    Returns:
        Dictionary with frontmatter fields + 'body' key

    Raises:
        FileNotFoundError: If file doesn't exist
        yaml.YAMLError: If frontmatter is invalid
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split frontmatter and body
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1]) or {}
                body = parts[2].strip()
                return {**frontmatter, 'body': body}

        # No frontmatter, entire content is body
        return {'body': content}

    except Exception as e:
        raise Exception(f"Failed to read {file_path}: {e}")


def write_content_file(file_path: str, frontmatter: Dict, body: str) -> None:
    """
    Write markdown file with YAML frontmatter.

    Args:
        file_path: Absolute path to markdown file
        frontmatter: Dictionary of metadata fields
        body: Markdown body content
    """
    # Ensure dates are in ISO format
    frontmatter_copy = frontmatter.copy()
    for key in ['created_date', 'updated_date', 'publish_date']:
        if key in frontmatter_copy and frontmatter_copy[key] is not None:
            if isinstance(frontmatter_copy[key], date):
                frontmatter_copy[key] = frontmatter_copy[key].isoformat()

    frontmatter_yaml = yaml.dump(frontmatter_copy, default_flow_style=False, allow_unicode=True)

    content = f"---\n{frontmatter_yaml}---\n\n{body}"

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


async def create_content_item(content_data: ContentCreate) -> ContentResponse:
    """
    Create new content item (markdown file + database index entry).

    Args:
        content_data: Content creation data

    Returns:
        Created content item with generated ID
    """
    content_id = str(uuid4())
    file_path = _get_content_file_path(content_id, content_data.content_type)

    today = date.today()
    frontmatter = {
        'id': content_id,
        'title': content_data.title,
        'content_type': content_data.content_type,
        'status': content_data.status,
        'created_date': today.isoformat(),
        'updated_date': today.isoformat(),
        'publish_date': content_data.publish_date.isoformat() if content_data.publish_date else None,
        'author': content_data.author,
        'url': content_data.url,
        'description': content_data.description,
        'categories': content_data.categories,
        'tags': content_data.tags,
        'custom_fields': content_data.custom_fields,
    }

    write_content_file(file_path, frontmatter, content_data.body)

    result = ContentResponse(
        id=content_id,
        file_path=file_path,
        created_date=today,
        updated_date=today,
        publish_date=content_data.publish_date,
        title=content_data.title,
        content_type=content_data.content_type,
        status=content_data.status,
        author=content_data.author,
        url=content_data.url,
        description=content_data.description,
        categories=content_data.categories,
        tags=content_data.tags,
        custom_fields=content_data.custom_fields,
        body=content_data.body
    )

    # Add to SQLite index
    from app.services import search_service
    search_service.index_content_item(result)

    return result


async def get_content_item(content_id: str) -> Optional[ContentResponse]:
    """
    Retrieve content item by ID.

    Args:
        content_id: UUID of content item

    Returns:
        Content item or None if not found
    """
    # TODO: Query SQLite index for file_path (Phase 3)
    # For now, search common content_types
    for content_type in ['blog', 'video', 'podcast', 'social', 'research', 'content-plans', 'website-content']:
        file_path = _get_content_file_path(content_id, content_type)
        if os.path.exists(file_path):
            data = read_content_file(file_path)

            # Convert string dates back to date objects
            for key in ['created_date', 'updated_date', 'publish_date']:
                if key in data and data[key] is not None:
                    if isinstance(data[key], str):
                        data[key] = date.fromisoformat(data[key])

            return ContentResponse(
                file_path=file_path,
                **data
            )
    return None


async def update_content_item(content_id: str, updates: ContentUpdate) -> Optional[ContentResponse]:
    """
    Update existing content item.

    Args:
        content_id: UUID of content item
        updates: Fields to update

    Returns:
        Updated content item or None if not found
    """
    existing = await get_content_item(content_id)
    if not existing:
        return None

    data = read_content_file(existing.file_path)

    # Apply updates
    update_dict = updates.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        if key == 'body':
            data['body'] = value
        else:
            data[key] = value

    data['updated_date'] = date.today().isoformat()

    body = data.pop('body', '')
    write_content_file(existing.file_path, data, body)

    # Convert string dates back to date objects
    for key in ['created_date', 'updated_date', 'publish_date']:
        if key in data and data[key] is not None:
            if isinstance(data[key], str):
                data[key] = date.fromisoformat(data[key])

    result = ContentResponse(
        file_path=existing.file_path,
        body=body,
        **data
    )

    # Update SQLite index
    from app.services import search_service
    search_service.index_content_item(result)

    return result


async def delete_content_item(content_id: str) -> bool:
    """
    Delete content item (markdown file + database index entry).

    Args:
        content_id: UUID of content item

    Returns:
        True if deleted, False if not found
    """
    existing = await get_content_item(content_id)
    if not existing:
        return False

    os.remove(existing.file_path)

    # Remove from SQLite index
    from app.services import search_service
    search_service.remove_from_index(content_id)

    return True
