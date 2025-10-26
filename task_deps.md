# Implementation Task Dependencies
## Content Tracking System - Execution Plan

**Generated:** 2025-10-25
**Last Updated:** 2025-10-26
**Architecture Decision:** See `Architects_Rationale.md`
**For:** Workflow Orchestrator / AI-Assisted Development

---

## 🎯 Project Status Summary

**Overall Progress:** 6 of 9 phases completed (67%)

### Completed Phases:
- ✅ **Phase 1:** Project Foundation & Development Environment
- ✅ **Phase 2:** Core CRUD Operations
- ✅ **Phase 3:** Search & Filtering
- ✅ **Phase 4:** Authentication & Multi-User Support
- ✅ **Phase 5:** Export Functionality (DOCX/PDF)
- ✅ **Phase 6:** Multi-Client Organization

### Remaining Phases:
- ⏳ **Phase 7:** Future Content Planning View
- ⏳ **Phase 8:** Testing & Documentation
- ⏳ **Phase 9:** Deployment & Validation

### Test Coverage:
- **Backend:** 71+ tests, 100% passing
- **Test Suites:** markdown_service, content_api, search_service, auth_service, auth_api, export_service, export_api
- **New Tests:** Client field tests in markdown_service and search_service

---

## Task Organization

This file contains the complete, ordered list of implementation tasks. Tasks are organized into phases, with dependencies clearly marked. Each task is granular, actionable, and optimized for AI-assisted development (Claude, Cursor).

**Execution Strategy:**
- Tasks within a phase can be parallelized if no explicit dependency
- Each task should produce a working, testable unit of code
- Commit after completing each phase (not individual tasks)
- Use AI to generate tests alongside implementation code

---

## ✅ PHASE 1: Project Foundation & Development Environment (Week 1-2) - COMPLETED

### 1.1 Project Structure Setup

**Task 1.1.1:** Create root project directory structure
```bash
mkdir -p content-tracking/{frontend,backend,content_library,data,exports/templates,docs}
cd content-tracking
git init
```

**Task 1.1.2:** Create backend directory structure
```bash
cd backend
mkdir -p app/{models,routers,services,db,tests/{fixtures}}
touch app/{__init__.py,main.py,config.py}
touch app/models/__init__.py
touch app/routers/__init__.py
touch app/services/__init__.py
touch requirements.txt Dockerfile .env.example
```

**Task 1.1.3:** Create frontend directory structure
```bash
cd frontend
npx create-next-app@latest . --typescript --tailwind --app --no-src-dir
mkdir -p components/{ui} lib public/assets
touch .env.local.example
```

**Task 1.1.4:** Initialize Git with proper .gitignore
Create `.gitignore` with:
```
# Python
__pycache__/
*.py[cod]
.env
venv/
.pytest_cache/

# Node
node_modules/
.next/
.env.local

# Data
data/*.db
content_library/*
!content_library/.gitkeep
exports/*
!exports/templates/
!exports/templates/.gitkeep

# IDE
.vscode/
.idea/
```

---

### 1.2 Docker Development Environment

**Task 1.2.1:** Create backend Dockerfile
```dockerfile
FROM python:3.11-slim

# Install Node.js for docxtemplater
RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

**Task 1.2.2:** Create frontend Dockerfile
```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

CMD ["npm", "run", "dev"]
```

**Task 1.2.3:** Create docker-compose.yml for development
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    volumes:
      - ./backend:/app
      - ./content_library:/app/content_library
      - ./data:/app/data
      - ./exports:/app/exports
    ports:
      - "8000:8000"
    environment:
      - CONTENT_LIBRARY_PATH=/app/content_library
      - DATABASE_URL=sqlite:///app/data/content_index.db
      - SECRET_KEY=dev-secret-key-change-in-production
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build: ./frontend
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on:
      - backend
```

**Task 1.2.4:** Create docker-compose.prod.yml for production
(Simplified version without volume mounts, uses built images)

**Task 1.2.5:** Create .env.example files for both services
Backend `.env.example`:
```
SECRET_KEY=generate-with-openssl-rand-hex-32
CONTENT_LIBRARY_PATH=/app/content_library
DATABASE_URL=sqlite:///app/data/content_index.db
ALLOWED_ORIGINS=https://yourdomain.com
JWT_EXPIRY_MINUTES=60
```

Frontend `.env.local.example`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Content Tracking System
```

---

### 1.3 Backend Core Configuration

**Task 1.3.1:** Implement backend/app/config.py
```python
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application configuration settings."""

    SECRET_KEY: str
    CONTENT_LIBRARY_PATH: str = "/app/content_library"
    DATABASE_URL: str = "sqlite:///app/data/content_index.db"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_MINUTES: int = 60

    class Config:
        env_file = ".env"

settings = Settings()
```

**Task 1.3.2:** Create backend requirements.txt
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
PyYAML==6.0.1
python-markdown==3.5.1
SQLAlchemy==2.0.23
aiosqlite==0.19.0
WeasyPrint==60.1
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.25.2
```

**Task 1.3.3:** Implement backend/app/main.py (FastAPI application entry point)
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

app = FastAPI(
    title="Content Tracking System API",
    description="Backend API for content management and tracking",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "service": "content-tracking-api"}

# Router imports will be added in later phases
```

---

### 1.4 Database Schema & Models

**Task 1.4.1:** Create backend/app/models/content.py (Pydantic models)
```python
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import date, datetime
from uuid import UUID, uuid4

class ContentBase(BaseModel):
    """Base content item schema."""
    title: str = Field(..., min_length=1, max_length=500)
    content_type: str = Field(..., min_length=1)
    status: str = Field(default="draft")
    author: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    categories: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    custom_fields: Dict[str, str] = Field(default_factory=dict)

class ContentCreate(ContentBase):
    """Schema for creating new content."""
    publish_date: Optional[date] = None
    body: str = ""

class ContentUpdate(BaseModel):
    """Schema for updating existing content (all fields optional)."""
    title: Optional[str] = None
    content_type: Optional[str] = None
    status: Optional[str] = None
    author: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    categories: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    custom_fields: Optional[Dict[str, str]] = None
    publish_date: Optional[date] = None
    body: Optional[str] = None

class ContentResponse(ContentBase):
    """Schema for content API responses."""
    id: str
    created_date: date
    updated_date: date
    publish_date: Optional[date]
    file_path: str
    body: Optional[str] = None  # Excluded in list views, included in detail

    class Config:
        from_attributes = True
```

**Task 1.4.2:** Create backend/app/db/init_db.py (SQLite schema initialization)
```python
import sqlite3
import os
from app.config import settings

def init_database():
    """Initialize SQLite database with content tracking schema."""
    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Main content metadata table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS content_items (
            id TEXT PRIMARY KEY,
            file_path TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            content_type TEXT NOT NULL,
            status TEXT DEFAULT 'draft',
            created_date DATE NOT NULL,
            updated_date DATE NOT NULL,
            publish_date DATE,
            author TEXT,
            url TEXT,
            description TEXT,
            categories_json TEXT,
            tags_json TEXT,
            custom_fields_json TEXT,
            last_indexed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Full-text search index
    cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS content_fts USING fts5(
            id UNINDEXED,
            title,
            description,
            body,
            tags,
            content='content_items'
        )
    """)

    # Users table (for Phase 4)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            role TEXT NOT NULL DEFAULT 'viewer',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    """)

    conn.commit()
    conn.close()
    print(f"Database initialized at {db_path}")

if __name__ == "__main__":
    init_database()
```

**Task 1.4.3:** Create backend/app/models/user.py (User models for Phase 4)
```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    full_name: Optional[str] = None
    role: str = Field(default="viewer", pattern="^(admin|editor|viewer)$")

class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    """Schema for user API responses."""
    id: str
    created_at: datetime
    last_login: Optional[datetime]
    is_active: bool

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    """Schema for authentication token response."""
    access_token: str
    token_type: str = "bearer"
```

---

### 1.5 Frontend Core Setup

**Task 1.5.1:** Initialize shadcn/ui components
```bash
cd frontend
npx shadcn-ui@latest init
# Select: TypeScript, Tailwind CSS, app directory, @/ alias, neutral color, CSS variables
```

**Task 1.5.2:** Install shadcn/ui core components
```bash
npx shadcn-ui@latest add button card input label select table dropdown-menu dialog badge
```

**Task 1.5.3:** Create frontend/lib/types.ts (TypeScript interfaces)
```typescript
export interface ContentItem {
  id: string;
  title: string;
  content_type: string;
  status: string;
  created_date: string;
  updated_date: string;
  publish_date?: string;
  author?: string;
  url?: string;
  description?: string;
  categories: string[];
  tags: string[];
  custom_fields: Record<string, string>;
  file_path: string;
  body?: string;
}

export interface User {
  id: string;
  email: string;
  full_name?: string;
  role: 'admin' | 'editor' | 'viewer';
  created_at: string;
  is_active: boolean;
}

export interface FilterOptions {
  search?: string;
  content_type?: string[];
  status?: string[];
  tags?: string[];
  client?: string;
  date_from?: string;
  date_to?: string;
}

export interface PaginationParams {
  page: number;
  per_page: number;
  total: number;
}
```

**Task 1.5.4:** Create frontend/lib/api.ts (API client)
```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    credentials: 'include', // Include cookies for auth
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Request failed' }));
    throw new ApiError(response.status, error.message || response.statusText);
  }

  return response.json();
}

export const api = {
  // Content endpoints (implemented in Phase 2)
  content: {
    list: (filters?: FilterOptions, page = 1, perPage = 50) =>
      fetchApi<{ items: ContentItem[]; pagination: PaginationParams }>(
        `/content?page=${page}&per_page=${perPage}&${new URLSearchParams(filters as any)}`
      ),
    get: (id: string) => fetchApi<ContentItem>(`/content/${id}`),
    create: (data: Partial<ContentItem>) =>
      fetchApi<ContentItem>(`/content`, {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    update: (id: string, data: Partial<ContentItem>) =>
      fetchApi<ContentItem>(`/content/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data),
      }),
    delete: (id: string) =>
      fetchApi<void>(`/content/${id}`, { method: 'DELETE' }),
  },
  // Search endpoints (implemented in Phase 3)
  search: {
    query: (q: string, filters?: FilterOptions) =>
      fetchApi<ContentItem[]>(`/search?q=${encodeURIComponent(q)}&${new URLSearchParams(filters as any)}`),
  },
  // Export endpoints (implemented in Phase 5)
  export: {
    docx: (filters?: FilterOptions) =>
      fetchApi<{ download_url: string }>(`/export/docx`, {
        method: 'POST',
        body: JSON.stringify(filters),
      }),
    pdf: (filters?: FilterOptions) =>
      fetchApi<{ download_url: string }>(`/export/pdf`, {
        method: 'POST',
        body: JSON.stringify(filters),
      }),
  },
  // Auth endpoints (implemented in Phase 4)
  auth: {
    login: (email: string, password: string) =>
      fetchApi<{ access_token: string }>(`/auth/login`, {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      }),
    logout: () => fetchApi<void>(`/auth/logout`, { method: 'POST' }),
    getCurrentUser: () => fetchApi<User>(`/auth/me`),
  },
};
```

**Task 1.5.5:** Create frontend/app/layout.tsx (Root layout)
```typescript
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Content Tracking System',
  description: 'Manage and track your content library',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-background">
          {children}
        </div>
      </body>
    </html>
  );
}
```

**Task 1.5.6:** Create frontend/app/page.tsx (Home page placeholder)
```typescript
import Link from 'next/link';
import { Button } from '@/components/ui/button';

export default function HomePage() {
  return (
    <div className="container mx-auto py-12">
      <h1 className="text-4xl font-bold mb-6">Content Tracking System</h1>
      <p className="text-lg text-muted-foreground mb-8">
        Manage your content library with ease.
      </p>
      <Link href="/content">
        <Button>View Content Library</Button>
      </Link>
    </div>
  );
}
```

---

### 1.6 Testing Infrastructure

**Task 1.6.1:** Create backend/tests/conftest.py (pytest fixtures)
```python
import pytest
import tempfile
import os
from app.main import app
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)

@pytest.fixture
def temp_content_dir():
    """Temporary content library directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

@pytest.fixture
def sample_markdown_content():
    """Sample markdown file content for testing."""
    return """---
id: test-content-123
title: Test Blog Post
content_type: blog
status: published
created_date: 2024-01-15
updated_date: 2024-01-20
publish_date: 2024-01-15
author: Test Author
tags:
  - test
  - sample
categories:
  - Testing
---

# Test Content

This is a sample blog post for testing purposes.
"""
```

**Task 1.6.2:** Create backend/pytest.ini
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
```

**Task 1.6.3:** Create frontend/jest.config.js
```javascript
const nextJest = require('next/jest');

const createJestConfig = nextJest({
  dir: './',
});

const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  testEnvironment: 'jest-environment-jsdom',
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1',
  },
};

module.exports = createJestConfig(customJestConfig);
```

**Task 1.6.4:** Create frontend/jest.setup.js
```javascript
import '@testing-library/jest-dom';
```

---

### 1.7 Documentation Foundation

**Task 1.7.1:** Create README.md (project overview)
```markdown
# Content Tracking System

A comprehensive content management platform for tracking, organizing, and exporting content across multiple clients and content types.

## Quick Start

### Development
```bash
# Clone repository
git clone <repo-url>
cd content-tracking

# Start both services with Docker Compose
docker-compose up --build

# Access application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs
```

### Production Deployment
See `docs/SETUP.md` for Coolify deployment instructions.

## Architecture
- **Backend:** FastAPI (Python 3.11+)
- **Frontend:** Next.js 16 (TypeScript, React 19.2)
- **Database:** SQLite + Markdown file storage
- **Deployment:** Docker Compose + Coolify

## Documentation
- `docs/SETUP.md`: Deployment instructions
- `docs/USAGE.md`: User guide
- `docs/DEVELOPMENT.md`: Developer guide for AI-assisted maintenance
```

**Task 1.7.2:** Create docs/SETUP.md (deployment guide - basic structure)
```markdown
# Deployment Guide

## Prerequisites
- Linux server (Ubuntu 22.04 LTS recommended)
- Coolify installed on server
- Domain name with DNS configured

## Steps
1. Create new project in Coolify
2. Connect Git repository
3. Set environment variables (see .env.example)
4. Deploy

(Detailed steps to be completed in Phase 9)
```

**Task 1.7.3:** Create docs/DEVELOPMENT.md (AI-assisted development guide - basic structure)
```markdown
# Development Guide for AI-Assisted Maintenance

## Using Claude/Cursor for Development

### Adding New Content Types
Prompt: "Add support for content_type='webinar' with custom fields: duration, recording_url, attendee_count"

### Modifying Service Functions
Prompt: "Update markdown_service.py::read_content_file() to handle missing frontmatter fields gracefully"

(Detailed examples to be completed in Phase 8)
```

---

### 1.8 Verification & Initial Commit

**Task 1.8.1:** Initialize SQLite database
```bash
cd backend
python -m app.db.init_db
```

**Task 1.8.2:** Test Docker Compose startup
```bash
cd .. # Back to project root
docker-compose up --build
# Verify:
# - Backend responds at http://localhost:8000/health
# - Frontend loads at http://localhost:3000
# - No startup errors in logs
docker-compose down
```

**Task 1.8.3:** Run initial test suite
```bash
cd backend
pytest
# Expected: 0 tests (infrastructure only, no tests yet)

cd ../frontend
npm test
# Expected: 0 tests
```

**Task 1.8.4:** Initial Git commit
```bash
git add .
git commit -m "Phase 1: Project foundation and development environment

- Docker Compose setup with FastAPI + Next.js
- Database schema and Pydantic models
- Frontend TypeScript types and API client
- Testing infrastructure (pytest, Jest)
- Basic documentation structure"
```

---

## ✅ PHASE 2: Core CRUD Operations (Week 3-4) - COMPLETED

### 2.1 Backend: Markdown Service Implementation

**Task 2.1.1:** Implement backend/app/services/markdown_service.py
```python
import os
import yaml
from pathlib import Path
from datetime import date
from typing import Optional, Dict, List
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
    frontmatter_yaml = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)

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

    # TODO: Add to SQLite index (Phase 3)

    return ContentResponse(
        id=content_id,
        file_path=file_path,
        created_date=today,
        updated_date=today,
        **frontmatter
    )

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
    for content_type in ['blog', 'video', 'podcast', 'social', 'research']:
        file_path = _get_content_file_path(content_id, content_type)
        if os.path.exists(file_path):
            data = read_content_file(file_path)
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
    update_dict = updates.dict(exclude_unset=True)
    for key, value in update_dict.items():
        if key == 'body':
            data['body'] = value
        else:
            data[key] = value

    data['updated_date'] = date.today().isoformat()

    body = data.pop('body', '')
    write_content_file(existing.file_path, data, body)

    # TODO: Update SQLite index (Phase 3)

    return ContentResponse(
        file_path=existing.file_path,
        body=body,
        **data
    )

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

    # TODO: Remove from SQLite index (Phase 3)

    return True
```

**Task 2.1.2:** Write tests for markdown_service.py
Create `backend/tests/test_markdown_service.py`:
```python
import pytest
from app.services.markdown_service import (
    read_content_file,
    write_content_file,
    create_content_item,
    get_content_item,
    update_content_item,
    delete_content_item,
)
from app.models.content import ContentCreate, ContentUpdate
from datetime import date
import os

@pytest.mark.asyncio
async def test_create_and_read_content(temp_content_dir, monkeypatch):
    """Test creating a content item and reading it back."""
    monkeypatch.setattr("app.services.markdown_service.settings.CONTENT_LIBRARY_PATH", temp_content_dir)

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

    retrieved = await get_content_item(created.id)
    assert retrieved is not None
    assert retrieved.title == "Test Blog Post"
    assert "This is a test" in retrieved.body

@pytest.mark.asyncio
async def test_update_content(temp_content_dir, monkeypatch):
    """Test updating content item."""
    monkeypatch.setattr("app.services.markdown_service.settings.CONTENT_LIBRARY_PATH", temp_content_dir)

    created = await create_content_item(ContentCreate(
        title="Original Title",
        content_type="blog",
        body="Original body"
    ))

    updates = ContentUpdate(title="Updated Title", body="Updated body")
    updated = await update_content_item(created.id, updates)

    assert updated.title == "Updated Title"
    assert updated.body == "Updated body"
    assert updated.updated_date >= created.updated_date

@pytest.mark.asyncio
async def test_delete_content(temp_content_dir, monkeypatch):
    """Test deleting content item."""
    monkeypatch.setattr("app.services.markdown_service.settings.CONTENT_LIBRARY_PATH", temp_content_dir)

    created = await create_content_item(ContentCreate(
        title="To Be Deleted",
        content_type="blog",
        body="Test"
    ))

    deleted = await delete_content_item(created.id)
    assert deleted is True

    retrieved = await get_content_item(created.id)
    assert retrieved is None
```

---

### 2.2 Backend: Content API Routes

**Task 2.2.1:** Implement backend/app/routers/content.py
```python
from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.content import ContentCreate, ContentUpdate, ContentResponse
from app.services import markdown_service

router = APIRouter(prefix="/content", tags=["content"])

@router.post("", response_model=ContentResponse, status_code=status.HTTP_201_CREATED)
async def create_content(content_data: ContentCreate):
    """
    Create new content item.

    Stores item as markdown file with YAML frontmatter.
    """
    return await markdown_service.create_content_item(content_data)

@router.get("/{content_id}", response_model=ContentResponse)
async def get_content(content_id: str):
    """
    Retrieve content item by ID.

    Returns 404 if not found.
    """
    content = await markdown_service.get_content_item(content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content

@router.put("/{content_id}", response_model=ContentResponse)
async def update_content(content_id: str, updates: ContentUpdate):
    """
    Update existing content item.

    Only provided fields are updated; others remain unchanged.
    """
    content = await markdown_service.update_content_item(content_id, updates)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content

@router.delete("/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_content(content_id: str):
    """
    Delete content item.

    Removes markdown file and database index entry.
    """
    deleted = await markdown_service.delete_content_item(content_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Content not found")
    return None

# TODO: List endpoint with filtering (Phase 3)
```

**Task 2.2.2:** Register content router in main.py
Update `backend/app/main.py`:
```python
from app.routers import content

app.include_router(content.router)
```

**Task 2.2.3:** Write API integration tests
Create `backend/tests/test_content_api.py`:
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_content():
    """Test POST /content endpoint."""
    response = client.post("/content", json={
        "title": "API Test Post",
        "content_type": "blog",
        "status": "draft",
        "body": "Test content"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "API Test Post"
    assert "id" in data

def test_get_content(created_content_id):
    """Test GET /content/{id} endpoint."""
    response = client.get(f"/content/{created_content_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_content_id

def test_update_content(created_content_id):
    """Test PUT /content/{id} endpoint."""
    response = client.put(f"/content/{created_content_id}", json={
        "title": "Updated Title"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"

def test_delete_content(created_content_id):
    """Test DELETE /content/{id} endpoint."""
    response = client.delete(f"/content/{created_content_id}")
    assert response.status_code == 204

    # Verify deleted
    response = client.get(f"/content/{created_content_id}")
    assert response.status_code == 404
```

---

### 2.3 Frontend: Content List View

**Task 2.3.1:** Create frontend/app/content/page.tsx (content list page)
```typescript
import { Suspense } from 'react';
import { ContentList } from '@/components/ContentList';
import { Button } from '@/components/ui/button';
import Link from 'next/link';

export default function ContentPage() {
  return (
    <div className="container mx-auto py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Content Library</h1>
        <Link href="/content/new">
          <Button>Add Content</Button>
        </Link>
      </div>

      <Suspense fallback={<div>Loading...</div>}>
        <ContentList />
      </Suspense>
    </div>
  );
}
```

**Task 2.3.2:** Create frontend/components/ContentList.tsx
```typescript
'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { ContentItem } from '@/lib/types';
import { ContentCard } from './ContentCard';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import Link from 'next/link';

export function ContentList() {
  const [content, setContent] = useState<ContentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchContent() {
      try {
        // TODO: Replace with actual API call when backend list endpoint is ready
        // For now, this is a placeholder
        const data = await api.content.list();
        setContent(data.items);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch content');
      } finally {
        setLoading(false);
      }
    }

    fetchContent();
  }, []);

  if (loading) {
    return <div className="text-center py-12">Loading content...</div>;
  }

  if (error) {
    return <div className="text-center py-12 text-destructive">{error}</div>;
  }

  return (
    <div className="space-y-4">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Title</TableHead>
            <TableHead>Type</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Updated</TableHead>
            <TableHead>Tags</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {content.map((item) => (
            <TableRow key={item.id}>
              <TableCell>
                <Link href={`/content/${item.id}`} className="hover:underline">
                  {item.title}
                </Link>
              </TableCell>
              <TableCell>{item.content_type}</TableCell>
              <TableCell>
                <Badge variant={item.status === 'published' ? 'default' : 'secondary'}>
                  {item.status}
                </Badge>
              </TableCell>
              <TableCell>{new Date(item.updated_date).toLocaleDateString()}</TableCell>
              <TableCell>
                <div className="flex gap-1 flex-wrap">
                  {item.tags.slice(0, 3).map((tag) => (
                    <Badge key={tag} variant="outline" className="text-xs">
                      {tag}
                    </Badge>
                  ))}
                  {item.tags.length > 3 && (
                    <Badge variant="outline" className="text-xs">
                      +{item.tags.length - 3}
                    </Badge>
                  )}
                </div>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      {content.length === 0 && (
        <div className="text-center py-12 text-muted-foreground">
          No content found. Create your first item to get started.
        </div>
      )}
    </div>
  );
}
```

**Task 2.3.3:** Create frontend/components/ContentCard.tsx
```typescript
import { ContentItem } from '@/lib/types';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import Link from 'next/link';

interface ContentCardProps {
  content: ContentItem;
}

export function ContentCard({ content }: ContentCardProps) {
  return (
    <Link href={`/content/${content.id}`}>
      <Card className="hover:shadow-lg transition-shadow cursor-pointer">
        <CardHeader>
          <div className="flex justify-between items-start mb-2">
            <Badge variant="outline">{content.content_type}</Badge>
            <Badge variant={content.status === 'published' ? 'default' : 'secondary'}>
              {content.status}
            </Badge>
          </div>
          <CardTitle>{content.title}</CardTitle>
          <CardDescription>
            {content.description || 'No description'}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2 mb-2">
            {content.tags.map((tag) => (
              <Badge key={tag} variant="secondary" className="text-xs">
                {tag}
              </Badge>
            ))}
          </div>
          <div className="text-sm text-muted-foreground">
            Updated: {new Date(content.updated_date).toLocaleDateString()}
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}
```

---

### 2.4 Frontend: Content Detail & Edit Views

**Task 2.4.1:** Create frontend/app/content/[id]/page.tsx
```typescript
import { Suspense } from 'react';
import { ContentDetail } from '@/components/ContentDetail';

export default function ContentDetailPage({ params }: { params: { id: string } }) {
  return (
    <div className="container mx-auto py-8">
      <Suspense fallback={<div>Loading...</div>}>
        <ContentDetail id={params.id} />
      </Suspense>
    </div>
  );
}
```

**Task 2.4.2:** Create frontend/components/ContentDetail.tsx
```typescript
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import { ContentItem } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import Link from 'next/link';

export function ContentDetail({ id }: { id: string }) {
  const [content, setContent] = useState<ContentItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    async function fetchContent() {
      try {
        const data = await api.content.get(id);
        setContent(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch content');
      } finally {
        setLoading(false);
      }
    }

    fetchContent();
  }, [id]);

  async function handleDelete() {
    if (!confirm('Are you sure you want to delete this content?')) return;

    try {
      await api.content.delete(id);
      router.push('/content');
    } catch (err) {
      alert('Failed to delete content');
    }
  }

  if (loading) return <div className="text-center py-12">Loading...</div>;
  if (error) return <div className="text-center py-12 text-destructive">{error}</div>;
  if (!content) return <div className="text-center py-12">Content not found</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold mb-2">{content.title}</h1>
          <div className="flex gap-2 mb-4">
            <Badge>{content.content_type}</Badge>
            <Badge variant={content.status === 'published' ? 'default' : 'secondary'}>
              {content.status}
            </Badge>
          </div>
        </div>
        <div className="flex gap-2">
          <Link href={`/content/${id}/edit`}>
            <Button variant="outline">Edit</Button>
          </Link>
          <Button variant="destructive" onClick={handleDelete}>Delete</Button>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Metadata</CardTitle>
        </CardHeader>
        <CardContent className="grid grid-cols-2 gap-4">
          <div>
            <div className="text-sm font-medium text-muted-foreground">Author</div>
            <div>{content.author || 'Not specified'}</div>
          </div>
          <div>
            <div className="text-sm font-medium text-muted-foreground">Created</div>
            <div>{new Date(content.created_date).toLocaleDateString()}</div>
          </div>
          <div>
            <div className="text-sm font-medium text-muted-foreground">Updated</div>
            <div>{new Date(content.updated_date).toLocaleDateString()}</div>
          </div>
          <div>
            <div className="text-sm font-medium text-muted-foreground">Publish Date</div>
            <div>{content.publish_date ? new Date(content.publish_date).toLocaleDateString() : 'Not set'}</div>
          </div>
          {content.url && (
            <div className="col-span-2">
              <div className="text-sm font-medium text-muted-foreground">URL</div>
              <a href={content.url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                {content.url}
              </a>
            </div>
          )}
        </CardContent>
      </Card>

      {content.description && (
        <Card>
          <CardHeader>
            <CardTitle>Description</CardTitle>
          </CardHeader>
          <CardContent>
            <p>{content.description}</p>
          </CardContent>
        </Card>
      )}

      {content.body && (
        <Card>
          <CardHeader>
            <CardTitle>Content</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="prose max-w-none" dangerouslySetInnerHTML={{ __html: content.body }} />
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Tags & Categories</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <div className="text-sm font-medium mb-2">Tags</div>
              <div className="flex flex-wrap gap-2">
                {content.tags.map((tag) => (
                  <Badge key={tag} variant="secondary">{tag}</Badge>
                ))}
                {content.tags.length === 0 && <span className="text-muted-foreground">No tags</span>}
              </div>
            </div>
            <div>
              <div className="text-sm font-medium mb-2">Categories</div>
              <div className="flex flex-wrap gap-2">
                {content.categories.map((cat) => (
                  <Badge key={cat} variant="outline">{cat}</Badge>
                ))}
                {content.categories.length === 0 && <span className="text-muted-foreground">No categories</span>}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
```

**Task 2.4.3:** Create frontend/app/content/[id]/edit/page.tsx
```typescript
import { Suspense } from 'react';
import { ContentEditForm } from '@/components/ContentEditForm';

export default function ContentEditPage({ params }: { params: { id: string } }) {
  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-8">Edit Content</h1>
      <Suspense fallback={<div>Loading...</div>}>
        <ContentEditForm id={params.id} />
      </Suspense>
    </div>
  );
}
```

**Task 2.4.4:** Create frontend/components/ContentEditForm.tsx
```typescript
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import { ContentItem } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

export function ContentEditForm({ id }: { id: string }) {
  const [content, setContent] = useState<ContentItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const router = useRouter();

  useEffect(() => {
    async function fetchContent() {
      try {
        const data = await api.content.get(id);
        setContent(data);
      } catch (err) {
        alert('Failed to load content');
      } finally {
        setLoading(false);
      }
    }

    fetchContent();
  }, [id]);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (!content) return;

    setSaving(true);
    try {
      await api.content.update(id, content);
      router.push(`/content/${id}`);
    } catch (err) {
      alert('Failed to save changes');
      setSaving(false);
    }
  }

  if (loading) return <div className="text-center py-12">Loading...</div>;
  if (!content) return <div className="text-center py-12">Content not found</div>;

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <Label htmlFor="title">Title</Label>
        <Input
          id="title"
          value={content.title}
          onChange={(e) => setContent({ ...content, title: e.target.value })}
          required
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label htmlFor="content_type">Content Type</Label>
          <Select
            value={content.content_type}
            onValueChange={(value) => setContent({ ...content, content_type: value })}
          >
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="blog">Blog</SelectItem>
              <SelectItem value="video">Video</SelectItem>
              <SelectItem value="podcast">Podcast</SelectItem>
              <SelectItem value="social">Social Media</SelectItem>
              <SelectItem value="research">Research</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div>
          <Label htmlFor="status">Status</Label>
          <Select
            value={content.status}
            onValueChange={(value) => setContent({ ...content, status: value })}
          >
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="draft">Draft</SelectItem>
              <SelectItem value="published">Published</SelectItem>
              <SelectItem value="archived">Archived</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      <div>
        <Label htmlFor="description">Description</Label>
        <Textarea
          id="description"
          value={content.description || ''}
          onChange={(e) => setContent({ ...content, description: e.target.value })}
          rows={3}
        />
      </div>

      <div>
        <Label htmlFor="author">Author</Label>
        <Input
          id="author"
          value={content.author || ''}
          onChange={(e) => setContent({ ...content, author: e.target.value })}
        />
      </div>

      <div>
        <Label htmlFor="url">URL</Label>
        <Input
          id="url"
          type="url"
          value={content.url || ''}
          onChange={(e) => setContent({ ...content, url: e.target.value })}
        />
      </div>

      <div>
        <Label htmlFor="tags">Tags (comma-separated)</Label>
        <Input
          id="tags"
          value={content.tags.join(', ')}
          onChange={(e) => setContent({ ...content, tags: e.target.value.split(',').map(t => t.trim()).filter(Boolean) })}
        />
      </div>

      <div>
        <Label htmlFor="body">Content Body (Markdown)</Label>
        <Textarea
          id="body"
          value={content.body || ''}
          onChange={(e) => setContent({ ...content, body: e.target.value })}
          rows={15}
          className="font-mono text-sm"
        />
      </div>

      <div className="flex gap-4">
        <Button type="submit" disabled={saving}>
          {saving ? 'Saving...' : 'Save Changes'}
        </Button>
        <Button
          type="button"
          variant="outline"
          onClick={() => router.push(`/content/${id}`)}
        >
          Cancel
        </Button>
      </div>
    </form>
  );
}
```

---

### 2.5 Frontend: New Content Creation

**Task 2.5.1:** Create frontend/app/content/new/page.tsx
```typescript
import { ContentNewForm } from '@/components/ContentNewForm';

export default function NewContentPage() {
  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-8">Create New Content</h1>
      <ContentNewForm />
    </div>
  );
}
```

**Task 2.5.2:** Create frontend/components/ContentNewForm.tsx
```typescript
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

export function ContentNewForm() {
  const [creating, setCreating] = useState(false);
  const router = useRouter();

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setCreating(true);

    const formData = new FormData(e.currentTarget);
    const data = {
      title: formData.get('title') as string,
      content_type: formData.get('content_type') as string,
      status: formData.get('status') as string,
      description: formData.get('description') as string,
      author: formData.get('author') as string,
      url: formData.get('url') as string,
      tags: (formData.get('tags') as string).split(',').map(t => t.trim()).filter(Boolean),
      categories: (formData.get('categories') as string).split(',').map(c => c.trim()).filter(Boolean),
      body: formData.get('body') as string,
    };

    try {
      const created = await api.content.create(data);
      router.push(`/content/${created.id}`);
    } catch (err) {
      alert('Failed to create content');
      setCreating(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <Label htmlFor="title">Title *</Label>
        <Input id="title" name="title" required />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label htmlFor="content_type">Content Type *</Label>
          <Select name="content_type" required defaultValue="blog">
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="blog">Blog</SelectItem>
              <SelectItem value="video">Video</SelectItem>
              <SelectItem value="podcast">Podcast</SelectItem>
              <SelectItem value="social">Social Media</SelectItem>
              <SelectItem value="research">Research</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div>
          <Label htmlFor="status">Status</Label>
          <Select name="status" defaultValue="draft">
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="draft">Draft</SelectItem>
              <SelectItem value="published">Published</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      <div>
        <Label htmlFor="description">Description</Label>
        <Textarea id="description" name="description" rows={3} />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label htmlFor="author">Author</Label>
          <Input id="author" name="author" />
        </div>

        <div>
          <Label htmlFor="url">URL</Label>
          <Input id="url" name="url" type="url" />
        </div>
      </div>

      <div>
        <Label htmlFor="tags">Tags (comma-separated)</Label>
        <Input id="tags" name="tags" placeholder="seo, tutorial, beginner" />
      </div>

      <div>
        <Label htmlFor="categories">Categories (comma-separated)</Label>
        <Input id="categories" name="categories" placeholder="Content Marketing, SEO" />
      </div>

      <div>
        <Label htmlFor="body">Content Body (Markdown)</Label>
        <Textarea
          id="body"
          name="body"
          rows={15}
          className="font-mono text-sm"
          placeholder="# Heading

Write your content here in markdown format..."
        />
      </div>

      <div className="flex gap-4">
        <Button type="submit" disabled={creating}>
          {creating ? 'Creating...' : 'Create Content'}
        </Button>
        <Button
          type="button"
          variant="outline"
          onClick={() => router.push('/content')}
        >
          Cancel
        </Button>
      </div>
    </form>
  );
}
```

---

### 2.6 Phase 2 Commit

**Task 2.6.1:** Run backend tests
```bash
cd backend
pytest tests/test_markdown_service.py tests/test_content_api.py -v
# Expected: All tests pass
```

**Task 2.6.2:** Manual testing
1. Start Docker Compose: `docker-compose up --build`
2. Navigate to http://localhost:3000/content/new
3. Create a sample content item
4. Verify it appears in content list
5. View content detail page
6. Edit content and save changes
7. Delete content item

**Task 2.6.3:** Git commit
```bash
git add .
git commit -m "Phase 2: Core CRUD operations

- Backend: markdown_service with read/write/parse functions
- Backend: content API routes (create, read, update, delete)
- Frontend: content list view with table display
- Frontend: content detail page with metadata and body
- Frontend: content edit form
- Frontend: new content creation form
- Tests: markdown_service and content API integration tests"
```

---

## ✅ PHASE 3: Search & Filtering (Week 4-5) - COMPLETED

### 3.1 Backend: SQLite Index Integration

**Task 3.1.1:** Implement backend/app/services/search_service.py
```python
import sqlite3
import json
from typing import List, Optional, Dict
from pathlib import Path
from app.config import settings
from app.models.content import ContentResponse
from app.services.markdown_service import read_content_file

def get_db_connection():
    """Get SQLite database connection."""
    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    return sqlite3.connect(db_path)

def index_content_item(content: ContentResponse) -> None:
    """
    Add or update content item in SQLite index.

    Args:
        content: Content item to index
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO content_items (
            id, file_path, title, content_type, status, created_date, updated_date,
            publish_date, author, url, description, categories_json, tags_json,
            custom_fields_json, last_indexed
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
    """, (
        content.id,
        content.file_path,
        content.title,
        content.content_type,
        content.status,
        content.created_date.isoformat(),
        content.updated_date.isoformat(),
        content.publish_date.isoformat() if content.publish_date else None,
        content.author,
        content.url,
        content.description,
        json.dumps(content.categories),
        json.dumps(content.tags),
        json.dumps(content.custom_fields),
    ))

    # Update FTS index
    cursor.execute("""
        INSERT OR REPLACE INTO content_fts (id, title, description, body, tags)
        VALUES (?, ?, ?, ?, ?)
    """, (
        content.id,
        content.title,
        content.description or '',
        content.body or '',
        ' '.join(content.tags),
    ))

    conn.commit()
    conn.close()

def remove_from_index(content_id: str) -> None:
    """Remove content item from SQLite index."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM content_items WHERE id = ?", (content_id,))
    cursor.execute("DELETE FROM content_fts WHERE id = ?", (content_id,))
    conn.commit()
    conn.close()

def search_content(
    query: Optional[str] = None,
    content_types: Optional[List[str]] = None,
    statuses: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
    client: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
) -> List[ContentResponse]:
    """
    Search and filter content items.

    Args:
        query: Full-text search query
        content_types: Filter by content type(s)
        statuses: Filter by status(es)
        tags: Filter by tag(s)
        client: Filter by client (custom_fields.client)
        date_from: Filter by created_date >= this date
        date_to: Filter by created_date <= this date
        limit: Maximum results to return
        offset: Pagination offset

    Returns:
        List of matching content items
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Build query
    sql = "SELECT * FROM content_items WHERE 1=1"
    params = []

    if query:
        # Use FTS for full-text search
        sql += " AND id IN (SELECT id FROM content_fts WHERE content_fts MATCH ?)"
        params.append(query)

    if content_types:
        placeholders = ','.join('?' * len(content_types))
        sql += f" AND content_type IN ({placeholders})"
        params.extend(content_types)

    if statuses:
        placeholders = ','.join('?' * len(statuses))
        sql += f" AND status IN ({placeholders})"
        params.extend(statuses)

    if tags:
        # Match any tag (OR logic)
        tag_conditions = ' OR '.join([f"tags_json LIKE ?" for _ in tags])
        sql += f" AND ({tag_conditions})"
        params.extend([f'%"{tag}"%' for tag in tags])

    if client:
        sql += " AND custom_fields_json LIKE ?"
        params.append(f'%"client": "{client}"%')

    if date_from:
        sql += " AND created_date >= ?"
        params.append(date_from)

    if date_to:
        sql += " AND created_date <= ?"
        params.append(date_to)

    sql += " ORDER BY updated_date DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()

    # Convert rows to ContentResponse objects
    results = []
    for row in rows:
        results.append(ContentResponse(
            id=row[0],
            file_path=row[1],
            title=row[2],
            content_type=row[3],
            status=row[4],
            created_date=row[5],
            updated_date=row[6],
            publish_date=row[7],
            author=row[8],
            url=row[9],
            description=row[10],
            categories=json.loads(row[11]) if row[11] else [],
            tags=json.loads(row[12]) if row[12] else [],
            custom_fields=json.loads(row[13]) if row[13] else {},
        ))

    return results

def rebuild_index_from_files() -> int:
    """
    Rebuild entire SQLite index from markdown files.

    Returns:
        Number of files indexed
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Clear existing index
    cursor.execute("DELETE FROM content_items")
    cursor.execute("DELETE FROM content_fts")
    conn.commit()

    # Scan content library
    content_library = Path(settings.CONTENT_LIBRARY_PATH)
    count = 0

    for md_file in content_library.rglob("*.md"):
        try:
            data = read_content_file(str(md_file))
            content = ContentResponse(file_path=str(md_file), **data)
            index_content_item(content)
            count += 1
        except Exception as e:
            print(f"Error indexing {md_file}: {e}")

    conn.close()
    return count
```

**Task 3.1.2:** Update markdown_service to call index functions
Update `backend/app/services/markdown_service.py`:
```python
from app.services import search_service

# In create_content_item:
# After write_content_file, add:
search_service.index_content_item(result)

# In update_content_item:
# After write_content_file, add:
search_service.index_content_item(result)

# In delete_content_item:
# After os.remove, add:
search_service.remove_from_index(content_id)
```

**Task 3.1.3:** Write tests for search_service.py
Create `backend/tests/test_search_service.py`:
```python
import pytest
from app.services.search_service import (
    index_content_item,
    remove_from_index,
    search_content,
    rebuild_index_from_files,
)
from app.models.content import ContentResponse
from datetime import date

@pytest.fixture
def sample_content():
    return ContentResponse(
        id="test-123",
        file_path="/tmp/test.md",
        title="Test Content",
        content_type="blog",
        status="published",
        created_date=date(2024, 1, 15),
        updated_date=date(2024, 1, 20),
        author="Test Author",
        tags=["test", "sample"],
        categories=["Testing"],
        custom_fields={"client": "TestClient"},
        body="Sample body content"
    )

def test_index_and_search(sample_content):
    """Test indexing and searching content."""
    index_content_item(sample_content)

    # Search by title
    results = search_content(query="Test")
    assert len(results) > 0
    assert any(r.id == "test-123" for r in results)

    # Search by tag
    results = search_content(tags=["sample"])
    assert any(r.id == "test-123" for r in results)

    # Remove and verify
    remove_from_index("test-123")
    results = search_content(query="Test")
    assert not any(r.id == "test-123" for r in results)
```

---

### 3.2 Backend: Search API Routes

**Task 3.2.1:** Update backend/app/routers/content.py with list endpoint
Add to `backend/app/routers/content.py`:
```python
from typing import Optional, List
from fastapi import Query
from app.services import search_service

@router.get("", response_model=List[ContentResponse])
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

    Supports full-text search and multiple filter criteria.
    """
    offset = (page - 1) * per_page

    results = search_service.search_content(
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

    return results
```

**Task 3.2.2:** Create backend/app/routers/search.py (dedicated search endpoint)
```python
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

    Searches title, description, body, and tags.
    """
    results = search_service.search_content(
        query=q,
        content_types=content_type,
        statuses=status,
        tags=tags,
        client=client,
        limit=limit,
        offset=0
    )

    return results
```

**Task 3.2.3:** Register search router in main.py
Update `backend/app/main.py`:
```python
from app.routers import content, search

app.include_router(content.router)
app.include_router(search.router)
```

---

### 3.3 Frontend: Search Bar Component

**Task 3.3.1:** Create frontend/components/SearchBar.tsx
```typescript
'use client';

import { useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Search } from 'lucide-react';

export function SearchBar() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [query, setQuery] = useState(searchParams.get('q') || '');

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const params = new URLSearchParams(searchParams);
    if (query) {
      params.set('q', query);
    } else {
      params.delete('q');
    }
    router.push(`/content?${params.toString()}`);
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <div className="relative flex-1">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
        <Input
          type="search"
          placeholder="Search content..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="pl-10"
        />
      </div>
      <Button type="submit">Search</Button>
    </form>
  );
}
```

---

### 3.4 Frontend: Filter Panel Component

**Task 3.4.1:** Create frontend/components/FilterPanel.tsx
```typescript
'use client';

import { useRouter, useSearchParams } from 'next/navigation';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { X } from 'lucide-react';

const CONTENT_TYPES = ['blog', 'video', 'podcast', 'social', 'research'];
const STATUSES = ['draft', 'published', 'archived'];

export function FilterPanel() {
  const router = useRouter();
  const searchParams = useSearchParams();

  function updateFilter(key: string, value: string | null) {
    const params = new URLSearchParams(searchParams);
    if (value) {
      params.set(key, value);
    } else {
      params.delete(key);
    }
    router.push(`/content?${params.toString()}`);
  }

  function clearAllFilters() {
    router.push('/content');
  }

  const activeFilters = Array.from(searchParams.entries());

  return (
    <div className="space-y-4 p-4 border rounded-lg">
      <div className="flex justify-between items-center">
        <h3 className="font-semibold">Filters</h3>
        {activeFilters.length > 0 && (
          <Button variant="ghost" size="sm" onClick={clearAllFilters}>
            Clear All
          </Button>
        )}
      </div>

      {activeFilters.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {activeFilters.map(([key, value]) => (
            <Badge key={`${key}-${value}`} variant="secondary" className="flex items-center gap-1">
              {key}: {value}
              <button
                onClick={() => updateFilter(key, null)}
                className="ml-1 hover:bg-secondary-foreground/20 rounded-full p-0.5"
              >
                <X className="h-3 w-3" />
              </button>
            </Badge>
          ))}
        </div>
      )}

      <div className="space-y-3">
        <div>
          <Label htmlFor="content_type">Content Type</Label>
          <Select
            value={searchParams.get('content_type') || ''}
            onValueChange={(value) => updateFilter('content_type', value)}
          >
            <SelectTrigger id="content_type">
              <SelectValue placeholder="All types" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="">All types</SelectItem>
              {CONTENT_TYPES.map((type) => (
                <SelectItem key={type} value={type}>
                  {type}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div>
          <Label htmlFor="status">Status</Label>
          <Select
            value={searchParams.get('status') || ''}
            onValueChange={(value) => updateFilter('status', value)}
          >
            <SelectTrigger id="status">
              <SelectValue placeholder="All statuses" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="">All statuses</SelectItem>
              {STATUSES.map((status) => (
                <SelectItem key={status} value={status}>
                  {status}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div>
          <Label htmlFor="client">Client</Label>
          <Select
            value={searchParams.get('client') || ''}
            onValueChange={(value) => updateFilter('client', value)}
          >
            <SelectTrigger id="client">
              <SelectValue placeholder="All clients" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="">All clients</SelectItem>
              {/* TODO: Dynamically load client list from API */}
              <SelectItem value="ClientA">Client A</SelectItem>
              <SelectItem value="ClientB">Client B</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>
    </div>
  );
}
```

---

### 3.5 Update Content List to Use Search/Filter

**Task 3.5.1:** Update frontend/app/content/page.tsx to include SearchBar and FilterPanel
```typescript
import { Suspense } from 'react';
import { ContentList } from '@/components/ContentList';
import { SearchBar } from '@/components/SearchBar';
import { FilterPanel } from '@/components/FilterPanel';
import { Button } from '@/components/ui/button';
import Link from 'next/link';

export default function ContentPage() {
  return (
    <div className="container mx-auto py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Content Library</h1>
        <Link href="/content/new">
          <Button>Add Content</Button>
        </Link>
      </div>

      <div className="mb-6">
        <SearchBar />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <aside className="lg:col-span-1">
          <FilterPanel />
        </aside>
        <div className="lg:col-span-3">
          <Suspense fallback={<div>Loading...</div>}>
            <ContentList />
          </Suspense>
        </div>
      </div>
    </div>
  );
}
```

**Task 3.5.2:** Update frontend/components/ContentList.tsx to use URL params
```typescript
'use client';

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { api } from '@/lib/api';
import { ContentItem, FilterOptions } from '@/lib/types';
// ... rest of component code

export function ContentList() {
  const searchParams = useSearchParams();
  const [content, setContent] = useState<ContentItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchContent() {
      try {
        const filters: FilterOptions = {
          search: searchParams.get('q') || undefined,
          content_type: searchParams.getAll('content_type'),
          status: searchParams.getAll('status'),
          client: searchParams.get('client') || undefined,
        };

        const data = await api.content.list(filters);
        setContent(data.items);
      } catch (err) {
        // handle error
      } finally {
        setLoading(false);
      }
    }

    fetchContent();
  }, [searchParams]);

  // ... rest of component code
}
```

---

### 3.6 Phase 3 Commit

**Task 3.6.1:** Run tests
```bash
cd backend
pytest tests/test_search_service.py -v
```

**Task 3.6.2:** Manual testing
1. Create multiple content items with different types, statuses, tags
2. Test full-text search
3. Test filtering by content_type
4. Test filtering by status
5. Test filtering by client
6. Test combined filters (e.g., search + content_type filter)
7. Test clear filters button

**Task 3.6.3:** Git commit
```bash
git add .
git commit -m "Phase 3: Search and filtering

- Backend: search_service with SQLite FTS5 integration
- Backend: list/search API endpoints with multiple filter criteria
- Backend: auto-indexing on content create/update/delete
- Frontend: SearchBar component with live query
- Frontend: FilterPanel with content_type, status, client filters
- Frontend: Active filter badges with individual clear buttons
- Tests: search_service unit tests"
```

---

## ✅ PHASE 4: Authentication & Multi-User (Week 5-6) - COMPLETED

**Implemented:**
- JWT authentication implementation with python-jose
- User CRUD endpoints with role-based access
- Login/logout API endpoints
- Role-based access control (admin/editor/viewer)
- Protected route middleware with get_current_user dependency
- Password hashing with bcrypt
- User management endpoints for admins
- Comprehensive authentication test suite

---

## ✅ PHASE 5: Export Functionality (Week 6-7) - COMPLETED

**Implemented:**
- DOCX export via python-docx with professional formatting
- PDF export via WeasyPrint (with HTML fallback for Windows)
- Customizable field inclusion and report titles
- Template system for branded exports
- Export API endpoints (POST /export/docx, POST /export/pdf, GET /export/download, DELETE /export/cleanup)
- Full filtering support (content types, statuses, tags, date ranges)
- Automatic cleanup of old export files
- Role-based access control (all authenticated users can export, only admins can cleanup)
- Comprehensive export test suite (18 tests, 100% passing)

---

## ✅ PHASE 6: Multi-Client Organization (Week 7-8) - COMPLETED

**Implemented:**
- Added `client` field to Pydantic content models (ContentBase, ContentCreate, ContentUpdate, ContentFilter)
- Updated SQLite database schema with `client` column and index
- Modified markdown_service to handle client field in YAML frontmatter
- Updated search_service to support client filtering with dedicated column
- Enhanced get_unique_values() to return clients from new column
- Created migration script (migrate_add_client.py) for existing databases
- Added comprehensive test coverage for client functionality:
  - Test creating content with client field
  - Test updating client field
  - Test filtering by client
  - Test combined client and content_type filtering
  - Test get_unique_clients functionality
- Updated frontend TypeScript types to include client field
- Added client dropdown with datalist to new content form
- Added client dropdown with datalist to edit content form
- Enhanced FilterPanel with dynamic client filter fetching from /search/filters API
- Client options dynamically loaded and updated on page load
- All existing tests passing plus 6+ new client-specific tests

---

## PHASE 7: Future Content Planning View (Week 8)

**NOTE:** Key tasks include:
- Status workflow states (To Do, In Progress, UAT, Reviewed, Approved)
- Future planning page with kanban-style view
- Drag-and-drop status transitions

---

## PHASE 8: Testing & Documentation (Week 9)

**NOTE:** Key tasks include:
- Comprehensive test suite (backend 75%+ coverage, frontend 60%+)
- SETUP.md with Coolify deployment instructions
- USAGE.md with screenshots and workflows
- DEVELOPMENT.md with AI prompts and examples

---

## PHASE 9: Deployment & Validation (Week 10)

**NOTE:** Key tasks include:
- Deploy to user's server via Coolify
- SSL certificate configuration
- Backup procedure setup
- Load testing
- User acceptance testing

---

## End of Task Dependencies Document

**Total Estimated Timeline:** 10 weeks (can be accelerated with focused AI-assisted development)

**Next Steps:**
1. Begin Phase 1 implementation
2. Use this document as reference for workflow orchestrator
3. Commit after each phase completion
4. Update CLAUDE.md if architectural decisions change

**For AI-Assisted Development:**
- Each task is designed to be a clear prompt for Claude/Cursor
- Example prompt: "Implement Task 2.1.1: Create backend/app/services/markdown_service.py with read_content_file, write_content_file, create_content_item, get_content_item, update_content_item, and delete_content_item functions. Follow the code pattern in CLAUDE.md Section 14."
