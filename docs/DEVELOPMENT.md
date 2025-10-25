# Content Tracking System - Development Guide

## Architecture Overview

The Content Tracking System uses a modern, AI-maintainable architecture:

- **Backend**: FastAPI (Python) with markdown file storage
- **Frontend**: Next.js 14 with TypeScript and Tailwind CSS
- **Storage**: Markdown files + SQLite index
- **Deployment**: Docker containers orchestrated by docker-compose

## Project Structure

```
content-tracking/
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── main.py          # Application entry point
│   │   ├── config.py        # Settings and configuration
│   │   ├── models/          # Pydantic data models
│   │   ├── routers/         # API route handlers
│   │   ├── services/        # Business logic layer
│   │   └── db/              # Database initialization
│   └── tests/         # Backend test suite
│
├── frontend/          # Next.js application
│   ├── app/           # Next.js App Router pages
│   ├── components/    # React components
│   └── lib/           # Utilities and API client
│
├── content_library/   # Markdown file storage
└── data/             # SQLite databases
```

## Development Workflow

### Backend Development

1. **Make changes to code**
   - Edit files in `backend/app/`
   - Follow Python PEP 8 style guidelines
   - Add docstrings to all functions/classes

2. **Run tests**
   ```bash
   cd backend
   pytest
   pytest --cov=app  # With coverage
   ```

3. **Format code**
   ```bash
   black app/
   isort app/
   ```

4. **Type checking**
   ```bash
   mypy app/
   ```

### Frontend Development

1. **Make changes to code**
   - Edit files in `frontend/app/` or `frontend/components/`
   - Follow TypeScript strict mode conventions
   - Use Tailwind CSS for styling

2. **Run tests**
   ```bash
   cd frontend
   npm run test
   ```

3. **Lint code**
   ```bash
   npm run lint
   ```

4. **Build for production**
   ```bash
   npm run build
   ```

## Adding New Features

### Backend: Adding a New API Endpoint

1. **Create router file** (if new resource)
   ```python
   # backend/app/routers/content.py
   from fastapi import APIRouter, Depends
   from app.models.content import ContentResponse

   router = APIRouter()

   @router.get("/content/{content_id}")
   async def get_content(content_id: str) -> ContentResponse:
       # Implementation
       pass
   ```

2. **Implement service layer**
   ```python
   # backend/app/services/content_service.py
   async def get_content_by_id(content_id: str) -> dict:
       # Business logic
       pass
   ```

3. **Register router in main.py**
   ```python
   from app.routers import content
   app.include_router(content.router, prefix="/api", tags=["content"])
   ```

4. **Write tests**
   ```python
   # backend/tests/test_content_api.py
   def test_get_content(client):
       response = client.get("/api/content/test-id")
       assert response.status_code == 200
   ```

### Frontend: Adding a New Page

1. **Create page file**
   ```typescript
   // frontend/app/content/page.tsx
   export default function ContentPage() {
     return <div>Content List</div>
   }
   ```

2. **Add API integration**
   ```typescript
   // frontend/lib/api.ts
   export const api = {
     content: {
       list: () => apiFetch<ContentListResponse>("/api/content"),
     }
   }
   ```

3. **Create components**
   ```typescript
   // frontend/components/ContentList.tsx
   export function ContentList({ items }: { items: ContentItem[] }) {
     return <div>{/* Component JSX */}</div>
   }
   ```

## Testing Guidelines

### Backend Tests

- Use pytest fixtures for test data
- Test service layer independently of routers
- Mock file system operations in unit tests
- Aim for 80%+ code coverage

### Frontend Tests

- Use React Testing Library
- Test component behavior, not implementation
- Mock API calls with MSW or similar
- Test user interactions and accessibility

## Working with Markdown Files

### File Format

Each content item is stored as:
```markdown
---
id: "unique-id"
title: "Content Title"
content_type: "blog"
status: "published"
created_date: "2024-01-15"
updated_date: "2024-01-15"
categories: ["Marketing"]
tags: ["seo", "content"]
---

# Content Body

Markdown content goes here...
```

### Reading Markdown Files

```python
import frontmatter

with open(file_path, 'r', encoding='utf-8') as f:
    post = frontmatter.load(f)
    metadata = post.metadata
    body = post.content
```

### Writing Markdown Files

```python
import frontmatter

post = frontmatter.Post(content=body, **metadata)
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(frontmatter.dumps(post))
```

## AI-Assisted Development Tips

This codebase is optimized for AI coding assistants (Claude, Cursor, GitHub Copilot):

1. **Use comprehensive prompts**
   - Reference CLAUDE.md for project context
   - Specify desired file structure and patterns
   - Request tests alongside implementation

2. **Leverage type hints**
   - Python type hints and TypeScript help AI understand code
   - Models are fully typed with Pydantic/TypeScript

3. **Follow established patterns**
   - AI works best with consistent code patterns
   - Copy existing files as templates for new features

4. **Ask for documentation**
   - Request docstrings and comments
   - Ask AI to update relevant docs

## Common Tasks

### Rebuild Search Index
```bash
cd backend
python -m app.services.search_service --rebuild-index
```

### Backup Data
```bash
tar -czf backup-$(date +%Y%m%d).tar.gz content_library/ data/
```

### Reset Database
```bash
rm -rf data/*.db
cd backend
python -m app.db.init_db
```

## Troubleshooting Development Issues

### Import errors
- Ensure virtual environment is activated
- Check PYTHONPATH includes backend directory
- Verify all dependencies installed

### Type checking failures
- Update type stubs: `pip install types-*`
- Check mypy configuration in pyproject.toml

### Frontend build errors
- Clear Next.js cache: `rm -rf .next`
- Reinstall dependencies: `rm -rf node_modules && npm install`

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
