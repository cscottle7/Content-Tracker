# Project Constitution: Content Tracking System

---
## Part A: Strategic & Product Definition
---

### 1. The Press Release
*FOR IMMEDIATE RELEASE*

**New Content Tracking System Revolutionizes How Media Professionals Manage and Analyze Their Content Libraries**

Asheville, NC – Content creators, marketers, and media teams can now effortlessly track, categorize, and analyze their entire content library with the launch of Content Tracking System, a comprehensive content management platform designed for professionals managing multiple content types across various channels.

Gone are the days of scattered spreadsheets, lost content assets, and unclear performance metrics. Content Tracking System provides a centralized hub where teams can track blog posts, videos, podcasts, social media content, and more—all in one intuitive interface. With powerful metadata management, automatic markdown-based storage, and flexible export capabilities, content professionals finally have the visibility and control they need to make data-driven decisions about their content strategy.

Whether you're a content marketer tracking campaign performance, a podcast producer managing episode metadata, or a creative team coordinating multi-channel content releases, Content Tracking System transforms chaotic content management into a streamlined, professional workflow.

### 2. Customer FAQ

* **Q: What types of content can I track with this system?**
  A: You can track any type of content you create or publish—blog posts, videos, podcasts, social media posts, newsletters, webinars, case studies, whitepapers, and more. The system uses flexible metadata fields that you can customize to match your specific content types and workflows.

* **Q: How does the markdown storage work, and why is it beneficial?**
  A: Each content item is stored as a markdown file with YAML frontmatter containing all metadata (title, dates, tags, categories, performance metrics, etc.). This approach gives you several advantages: your data is future-proof and portable, you can edit files directly in any text editor, you can version control your content library with Git, and you're never locked into a proprietary database format.

* **Q: Can I export my content reports and share them with stakeholders?**
  A: Absolutely. The system includes robust export capabilities to DOCX and PDF formats, allowing you to generate professional reports with customizable templates. You can filter content by date ranges, categories, or performance metrics, then export exactly what you need for client reports, team reviews, or strategic planning sessions.

* **Q: Is this a cloud service or do I need to host it myself?**
  A: Content Tracking System is designed for self-hosting on your own server, giving you complete control over your content data and privacy. The system includes straightforward deployment instructions and is optimized for AI-assisted maintenance, even if you're not a professional developer.

* **Q: How do I search and filter through large content libraries?**
  A: The system features powerful full-text search across all content metadata and body text, plus advanced filtering by date ranges, tags, categories, content types, authors, and custom fields. You can combine multiple filters to quickly find exactly what you're looking for, even in libraries with thousands of content items.

### 3. Internal FAQ

* **Q: What's the technical complexity level for maintaining this system?**
  A: The architecture is designed for AI-assisted development and maintenance. With clean separation of concerns, comprehensive documentation, and modern best practices, non-technical builders can maintain and extend the system using AI coding assistants (Claude, Cursor, etc.). The tech stack prioritizes simplicity and clarity over clever abstractions.

* **Q: How scalable is the markdown-based storage approach?**
  A: For typical content team use cases (hundreds to low thousands of content items), markdown file storage performs excellently and offers unmatched simplicity. The system uses efficient indexing and caching strategies. If you eventually scale to tens of thousands of items, the architecture allows for migration to a database while maintaining the same markdown-based editing workflow.

* **Q: What's the MVP scope vs. post-MVP roadmap?**
  A: MVP focuses on core CRUD operations for content items, markdown-based storage with YAML frontmatter, basic web UI for browsing/editing, search and filtering, and simple export to DOCX/PDF. Post-MVP enhancements include analytics dashboards, automated content scheduling, API integrations with publishing platforms, collaborative editing features, and advanced reporting templates.

* **Q: Why this tech stack specifically?**
  A: The stack (Python/FastAPI + vanilla JS/modern CSS) is optimized for three critical factors: AI-assisted development (clear, readable code that AI models understand well), self-hosting simplicity (single server deployment with minimal dependencies), and non-technical maintainability (straightforward architecture without complex build chains or excessive abstraction layers).

* **Q: How are we handling authentication and multi-user access?**
  A: MVP includes basic session-based authentication with user accounts, role-based permissions (admin/editor/viewer), and secure password hashing. This allows team collaboration from day one while keeping complexity manageable. Post-MVP can add SSO, OAuth providers, and more granular permission controls if needed.

### 4. Project Goal & High-Level Requirements

**Jobs-to-be-Done (JTBD) Statement:**
When I create and publish content across multiple channels and formats, I want to centrally track all metadata, performance metrics, and categorization in a searchable system that stores everything as portable markdown files, so I can maintain visibility over my entire content library, make data-driven decisions about content strategy, and generate professional reports for stakeholders—all without being locked into proprietary formats or cloud services.

**Core Requirements:**
* **Multi-format content tracking:** Support diverse content types (blog, video, podcast, social, etc.) with flexible metadata schemas
* **Markdown-based storage:** Each content item stored as .md file with YAML frontmatter for maximum portability and future-proofing
* **Powerful search & filtering:** Full-text search plus advanced filtering by dates, categories, tags, custom fields
* **Professional export capabilities:** Generate DOCX and PDF reports with customizable templates and filtered content sets
* **Self-hosted architecture:** Deploy on user's existing server infrastructure with straightforward setup
* **Team collaboration:** Multi-user support with role-based access control from day one
* **AI-maintainable codebase:** Clean, well-documented code optimized for AI-assisted development and maintenance

### 5. Success Metrics & Measurement Plan

* **Content Library Coverage:**
  Success = 100% of team's content items migrated into system within 60 days of deployment. Measured by: count of content items in system vs. total known content inventory. Indicates adoption and utility.

* **User Engagement & Retention:**
  Success = 80%+ of team members actively using system weekly (viewing, editing, or adding content). Measured by: weekly active user count / total registered users. Indicates the system has become the single source of truth for content tracking.

* **Export Usage:**
  Success = At least 2 reports exported per week during first 3 months. Measured by: export action count in application logs. Indicates the reporting functionality delivers real value for stakeholder communication.

* **Search Effectiveness:**
  Success = Users find target content within 3 search attempts 90%+ of the time. Measured by: user surveys and search-to-view conversion tracking (if implemented). Indicates metadata structure and search functionality meet user needs.

* **System Stability:**
  Success = 99%+ uptime over 30-day rolling window. Measured by: server uptime monitoring. Indicates the self-hosted deployment is reliable and maintainable.

### 6. Core Features & Scope

#### In Scope (MVP)

* **Content Item CRUD Operations**
  - As a user, I can create new content items with fields: title, content type, publish date, URL, description, tags, categories, author, status
  - As a user, I can edit existing content item metadata and save changes
  - As a user, I can delete content items (with confirmation prompt)
  - As a user, I can view individual content item detail pages showing all metadata

* **Markdown File Storage**
  - As a system, I store each content item as a markdown file with YAML frontmatter in organized directory structure
  - As a user, I can directly edit markdown files in filesystem and have changes reflected in web UI (manual sync/refresh)
  - As a system, I automatically parse YAML frontmatter on file read and update frontmatter on content edits via UI

* **Content Library Browse & List**
  - As a user, I can view a table/list of all content items with sortable columns (title, date, type, status)
  - As a user, I can paginate through large content libraries (20-50 items per page)
  - As a user, I can see content counts by category and type in sidebar/dashboard

* **Search & Filtering**
  - As a user, I can perform full-text search across all content item fields (title, description, tags, body text)
  - As a user, I can filter by: date ranges, content type, category, tags, author, status
  - As a user, I can combine multiple filters and see live-updated result counts
  - As a user, I can save common filter combinations as bookmarks/presets

* **Export Functionality**
  - As a user, I can export current filtered content set to DOCX format with basic professional template
  - As a user, I can export current filtered content set to PDF format with basic professional template
  - As a user, I can select which metadata fields to include in exports
  - As a system, I generate exports with formatted tables, headings, and proper typography

* **User Authentication & Multi-User Support**
  - As a user, I can register an account and log in with email/password
  - As an admin, I can manage user accounts (create, deactivate, assign roles)
  - As a system, I implement role-based access: Admin (full control), Editor (create/edit content), Viewer (read-only)
  - As a user, I remain securely logged in across sessions until explicit logout

* **Basic Configuration**
  - As an admin, I can define custom content types (beyond default: blog, video, podcast, social)
  - As an admin, I can define custom categories and tags for content organization
  - As a system, I store configuration in simple YAML/JSON config files for easy editing

#### Out of Scope (Deferred to Post-MVP)

* **Advanced Analytics Dashboard:** Visual charts, performance trending, comparative analytics (can analyze markdown files manually in MVP)
* **Automated Publishing Integrations:** Direct posting to WordPress, social platforms, YouTube via APIs
* **Content Scheduling & Calendar:** Built-in editorial calendar with scheduled publish dates and reminders
* **Collaborative Editing:** Real-time multi-user editing, comments, approval workflows
* **Advanced Reporting Templates:** Custom report builders, branded templates, automated report distribution
* **Mobile App:** Native iOS/Android apps (web UI is responsive for mobile browsers)
* **Version History:** Built-in content versioning and rollback (can use Git for markdown files externally)
* **Media Asset Management:** Direct upload/storage of images, videos, audio files (MVP stores metadata and links only)
* **AI Content Analysis:** Automated tagging, sentiment analysis, readability scoring
* **Performance Metrics Integration:** Automatic import of analytics from Google Analytics, social platforms, etc.

---
## Part B: Technical & Operational Framework
---

### 7. Strategic Constraint Tags for AI Architect

* **Philosophy Tag:** `[Philosophy:Pragmatism]`
  _Prioritize working solutions over architectural purity. Choose boring, proven technology over cutting-edge. Value simplicity and maintainability over clever abstractions._

* **Constraint Tags:**
  - `[Constraint:Simplicity]` — Optimize for AI-assisted maintenance by non-technical builder
  - `[Constraint:Portability]` — Markdown-based storage ensures data portability and future-proofing
  - `[Constraint:Self-Hosted]` — Must deploy easily on user's existing server infrastructure
  - `[Constraint:Documentation]` — Comprehensive inline comments and setup documentation required

### 8. Tech Stack & Key Libraries

**Backend:**
* **Language:** Python 3.11+
* **Framework:** FastAPI 0.104+ (async web framework with automatic OpenAPI docs, type hints, easy deployment)
* **Markdown Processing:** `python-markdown` 3.5+ with extensions for YAML frontmatter parsing
* **YAML Handling:** `PyYAML` 6.0+ for frontmatter parsing and writing
* **Authentication:** `python-jose[cryptography]` for JWT tokens, `passlib[bcrypt]` for password hashing (deferred to post-MVP)
* **Document Export:**
  - **DOCX (Priority):** `docxtemplater` (Node.js) or `pandoc` with `pypandoc` for template-based branded exports
  - **PDF (Lower Priority):** `WeasyPrint` 60+ for HTML-to-PDF conversion with CSS styling
* **Search:** Simple filesystem-based full-text search (Python built-in `str` operations + metadata indexing) for MVP

**Frontend:**
* **Framework:** Next.js 16+ (React 19.2-based full-stack framework with App Router, Turbopack bundler)
* **Language:** TypeScript 5.1+ (strict mode, type-safe, superior AI code generation support)
* **Markdown Editor:** MDXEditor (WYSIWYG markdown editing with TypeScript-first design)
* **UI Component Library:** shadcn/ui (recommended - modern, accessible, customizable components)
* **Styling:** Tailwind CSS 4+ (utility-first CSS, mobile-first responsive design)
* **Icons:** Lucide Icons (modern SVG icon set, tree-shakeable)

**Database:**
* **Primary Storage:** Filesystem-based (markdown files organized in directories)
* **Metadata Index:** SQLite database for fast search/filtering (stores parsed frontmatter, regenerated on app start or manual sync)
* **Future Migration Path:** PostgreSQL if scaling beyond thousands of items

**Deployment & Infrastructure:**
* **Platform:** Coolify (self-hosted PaaS - easiest for non-technical users)
* **Containerization:** Docker + Docker Compose (for Next.js frontend + FastAPI backend)
* **Web Server:** Nginx (reverse proxy, handles SSL/HTTPS with Let's Encrypt)
* **Process Management:** Docker containers managed by Coolify
* **Server OS:** Linux (Ubuntu 22.04 LTS or similar)

**Key Library Purposes:**
* **FastAPI:** Async REST API backend, handles data processing and file operations
* **Next.js:** Modern React framework with excellent AI code generation support, server-side rendering, and built-in optimization
* **MDXEditor/TipTap:** Professional WYSIWYG markdown editor with clean output and TypeScript support
* **python-markdown + PyYAML:** Parse and write markdown files with YAML frontmatter (the core data format)
* **docxtemplater/pandoc:** Template-based DOCX generation with branded styling and multi-template support
* **WeasyPrint:** HTML-to-PDF conversion with CSS styling for professional reports
* **SQLite:** Lightweight metadata index for fast search/filter queries without full markdown file scanning
* **Coolify:** Self-hosted platform-as-a-service for simplified deployment, SSL management, and monitoring

**Tech Stack Rationale:**
* **Next.js 16 + TypeScript:** Latest version with React 19.2, Turbopack bundler (5-10x faster), superior AI-assisted development (GitHub Copilot, Claude, Cursor support), App Router with Partial Pre-Rendering (PPR), extensive ecosystem
* **shadcn/ui:** Component library that's copied into your project (full control), built on Radix UI primitives, excellent accessibility, highly customizable
* **MDXEditor:** Best balance of WYSIWYG editing and clean markdown output, TypeScript-first design, React component-based
* **Tailwind CSS 4:** Latest version with native CSS variables, improved performance, better DX
* **docxtemplater/pandoc:** Industry-standard for template-based document generation with full branding control
* **Coolify:** Dramatically simplifies self-hosting for non-technical users while maintaining full control over infrastructure

### 9. Project File Structure

```
content-tracking/
├── frontend/                   # Next.js application
│   ├── app/                    # Next.js 14+ app directory
│   │   ├── layout.tsx          # Root layout component
│   │   ├── page.tsx            # Home page
│   │   ├── dashboard/
│   │   │   ├── page.tsx        # Main dashboard
│   │   │   └── layout.tsx
│   │   ├── content/
│   │   │   ├── page.tsx        # Content list view
│   │   │   ├── [id]/           # Dynamic content detail routes
│   │   │   │   ├── page.tsx    # Content detail page
│   │   │   │   └── edit/
│   │   │   │       └── page.tsx # Content edit page
│   │   │   └── new/
│   │   │       └── page.tsx    # New content form
│   │   ├── future-planning/
│   │   │   └── page.tsx        # Future content planning view
│   │   └── login/
│   │       └── page.tsx        # Login page (post-MVP)
│   ├── components/             # React components
│   │   ├── ui/                 # shadcn/ui or base UI components
│   │   ├── ContentCard.tsx
│   │   ├── ContentList.tsx
│   │   ├── FilterPanel.tsx
│   │   ├── MarkdownEditor.tsx  # MDXEditor wrapper
│   │   ├── SearchBar.tsx
│   │   └── ExportButton.tsx
│   ├── lib/                    # Utility functions
│   │   ├── api.ts              # API client for backend
│   │   ├── types.ts            # TypeScript types/interfaces
│   │   └── utils.ts            # Helper functions
│   ├── public/                 # Static assets
│   ├── styles/                 # Global styles (if not using Tailwind)
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   └── .env.local.example
│
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI application entry point
│   │   ├── config.py           # Configuration settings
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── content.py      # Content item data models (Pydantic)
│   │   │   └── user.py         # User and auth data models
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── content.py      # Content CRUD API endpoints
│   │   │   ├── search.py       # Search and filter endpoints
│   │   │   ├── export.py       # Export to DOCX/PDF endpoints
│   │   │   ├── planning.py     # Future content planning endpoints
│   │   │   └── auth.py         # Authentication endpoints (post-MVP)
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── markdown_service.py  # Read/write markdown files
│   │   │   ├── search_service.py    # Search and filter logic
│   │   │   ├── export_service.py    # DOCX and PDF generation
│   │   │   └── auth_service.py      # User authentication (post-MVP)
│   │   └── db/
│   │       └── init_db.py      # SQLite database initialization
│   ├── tests/
│   │   ├── test_markdown_service.py
│   │   ├── test_search_service.py
│   │   ├── test_export_service.py
│   │   └── test_content_api.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── content_library/            # Markdown files storage (shared volume)
│   ├── blog/
│   ├── video/
│   ├── podcast/
│   ├── social/
│   ├── research/
│   ├── content-plans/
│   ├── website-content/
│   └── [other-content-types]/
│
├── data/
│   ├── content_index.db        # SQLite metadata index
│   └── users.db                # User accounts database (post-MVP)
│
├── exports/                    # Temporary directory for generated files
│   └── templates/              # DOCX/PDF templates for branding
│
├── docs/
│   ├── SETUP.md                # Deployment and installation guide
│   ├── USAGE.md                # User guide for content management
│   └── DEVELOPMENT.md          # Developer guide for AI-assisted maintenance
│
├── docker-compose.yml          # Docker services orchestration
├── .env.example                # Environment variables template
├── .gitignore
└── README.md                   # Project overview and quick start
```

**Directory Organization Notes:**
* **frontend/**: Next.js application with TypeScript, handles all UI and user interactions
* **backend/**: FastAPI REST API, handles data processing and file operations
* **content_library/**: Shared volume accessible by both frontend and backend, organized by content type
* **data/**: SQLite databases for metadata indexing and user management
* **exports/templates/**: Branded DOCX/PDF templates for multi-template export support
* **docker-compose.yml**: Orchestrates frontend, backend, and shared volumes for deployment

### 10. Key Commands

**Development Environment Setup:**

*Frontend (Next.js):*
```bash
cd frontend
npm install                      # Install Node.js dependencies
npm run dev                      # Run development server (http://localhost:3000)
npm run build                    # Build for production
npm run lint                     # Run ESLint
```

*Backend (FastAPI):*
```bash
cd backend
pip install -r requirements.txt  # Install Python dependencies
python -m app.db.init_db         # Initialize SQLite databases
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000  # Run dev server
```

**Docker Development:**
```bash
# Start both frontend and backend with Docker Compose
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f
```

**Production Deployment (Coolify):**
```bash
# Deploy to Coolify (push to Git, Coolify auto-deploys)
git push origin main

# Or manual Docker deployment
docker-compose -f docker-compose.prod.yml up -d
```

**Testing:**

*Frontend:*
```bash
cd frontend
npm run test                     # Run Jest tests
npm run test:coverage            # Run tests with coverage
```

*Backend:*
```bash
cd backend
pytest                           # Run all tests
pytest --cov=app --cov-report=html  # Run with coverage
pytest tests/test_markdown_service.py -v  # Run specific test
```

**Maintenance:**
```bash
# Rebuild search index from markdown files (backend)
cd backend
python -m app.services.search_service --rebuild-index

# Backup content library and databases
tar -czf backup-$(date +%Y%m%d).tar.gz content_library/ data/

# Import existing markdown files
python -m app.services.markdown_service --import /path/to/existing/content/
```

### 11. Code Style & Conventions

**General:**
* All new code must include comprehensive docstrings (Google style)
* Write unit tests for all service layer functions (target 80%+ coverage)
* Use type hints extensively for AI readability and IDE support
* Prefer explicit over implicit; clarity over cleverness

**Backend (Python/FastAPI):**
* Follow PEP 8 guidelines strictly (use `black` formatter, `isort` for imports)
* Use snake_case for functions, variables; PascalCase for classes
* Async/await patterns for all I/O operations (file reads, database queries)
* Pydantic models for all request/response validation and data transfer
* Keep routers thin—business logic belongs in services layer
* Use dependency injection for database connections and auth context

**Frontend (TypeScript/React/Next.js):**
* Use TypeScript strict mode; all components and functions must be typed
* Prefer functional components with hooks over class components
* Use Next.js App Router conventions (app directory structure)
* Follow React best practices: single responsibility, composition over inheritance
* Use Tailwind CSS utility classes or CSS modules for styling
* Implement responsive design with mobile-first approach
* Component naming: PascalCase for components, camelCase for functions/variables
* Use React Server Components where appropriate for performance
* Implement proper error boundaries and loading states

**Markdown Files (Content Storage):**
* YAML frontmatter must always include: title, content_type, created_date, updated_date
* Use ISO 8601 date format: YYYY-MM-DD for all dates
* Tags and categories stored as YAML arrays: `tags: [seo, tutorial, beginner]`
* File naming convention: `YYYY-MM-DD-slug-title.md` for date-based content types
* Use relative links for internal references between content items

**Documentation:**
* Every service module includes module-level docstring explaining purpose and usage
* Complex algorithms include inline comments explaining "why", not "what"
* README files in each major directory explaining structure and conventions
* API endpoints documented via FastAPI automatic OpenAPI generation (include examples)

### 12. Architectural Principles & Constraints

**Pattern: Layered Architecture with Service-Oriented Design**
* **Routers layer:** HTTP request/response handling only; thin controllers delegating to services
* **Services layer:** Core business logic, data transformations, file operations
* **Data layer:** Markdown file I/O and SQLite metadata index management
* Services must not know about HTTP concerns; should be testable in isolation

**Design Philosophy: Modern but Proven Technology Stack**
* Choose proven, well-documented libraries with active communities
* Leverage Next.js for optimized builds and server-side rendering
* Use TypeScript for type safety and better AI code generation
* Use SQLite over complex database setup for MVP scale
* Prioritize developer experience and AI-assisted maintainability

**State Management:**
* Backend services are stateless; all state stored in files or SQLite
* User sessions managed via JWT tokens (stateless auth)
* No in-memory caching in MVP (filesystem + SQLite is fast enough)

**Data Handling:**
* **Single Source of Truth:** Markdown files are canonical data source
* **Index Synchronization:** SQLite index is a performance optimization, regenerated from markdown on app start or on-demand
* **Data Transfer Objects (DTOs):** All API responses use Pydantic models, never raw database/file objects
* **Validation:** All user input validated at API boundary using Pydantic models before reaching services

**Error Handling:**
* All file I/O operations wrapped in try/except with specific error types
* Return structured error responses: `{"error": "error_code", "message": "human readable", "details": {...}}`
* Log all errors with context (user ID, file path, operation) for debugging
* Graceful degradation: if search index unavailable, fall back to slower file-based search

**Search & Performance:**
* SQLite full-text search (FTS5) for metadata fields in MVP
* File-based search for markdown body content (grep-style) for MVP simplicity
* Pagination mandatory for all list views (default 50 items per page)
* Lazy loading: load full markdown content only when viewing detail page

**Security Principles:**
* Password hashing with bcrypt (minimum 12 rounds)
* JWT tokens for stateless authentication (short expiry, refresh token pattern)
* Role-based access control (RBAC) enforced at service layer, not just routes
* Input sanitization for all user-provided content (especially markdown body)
* No direct file path exposure to users; use content item IDs only
* HTTPS required in production (configured at Nginx reverse proxy level)

**Export Architecture:**
* Export requests queued for async processing if large content sets (future enhancement)
* Generated files stored temporarily with auto-cleanup after 1 hour or download
* Export templates stored as Jinja2 HTML files (rendered to HTML, then converted to PDF/DOCX)
* Allow custom template selection (admin can add templates to exports/ directory)

### 13. Prohibitions (Forbidden Actions)

* **DO NOT** commit sensitive configuration (API keys, passwords, secret keys) to Git. Use .env files and environment variables exclusively.
* **DO NOT** allow users to upload executable files or scripts. Content library should contain markdown and linked media references only.
* **DO NOT** use complex frontend frameworks (React, Vue, Angular) for MVP. Stick to vanilla JS and server-side rendering.
* **DO NOT** implement custom authentication schemes. Use established libraries (python-jose, passlib) and standard JWT pattern.
* **DO NOT** expose raw file system paths in API responses or error messages. Always use content item IDs or slugs.
* **DO NOT** make breaking changes to markdown frontmatter schema without migration script and documentation.
* **DO NOT** add dependencies without documenting purpose in this file and ensuring they're compatible with self-hosted deployment.
* **DO NOT** store user passwords in plaintext or reversible encryption. Always use bcrypt hashing.
* **DO NOT** skip input validation. All user input must pass through Pydantic model validation before processing.
* **DO NOT** create overly abstract code patterns. Prefer simple, explicit code that AI assistants can easily understand and modify.
* **DO NOT** implement features outside MVP scope without explicit approval. Maintain focus on core functionality first.
* **DO NOT** assume cloud hosting. All architecture decisions must support self-hosted deployment on user's existing server.

---

## Part C: Development Guidelines for AI-Assisted Workflow
---

### 14. AI Assistant Collaboration Notes

**For Claude, Cursor, and other AI coding assistants working on this codebase:**

**Code Generation Priorities:**
1. **Clarity over Cleverness:** Write explicit, self-documenting code. Avoid complex one-liners or overly abstracted patterns.
2. **Comprehensive Comments:** Include docstrings for all functions/classes and inline comments for non-obvious logic.
3. **Type Hints Everywhere:** Use Python type hints extensively—they help both AI understanding and IDE support.
4. **Testable Design:** Structure code so each function can be tested in isolation with minimal mocking.
5. **Error Context:** Error messages should include enough context to debug without diving into logs.

**Common Patterns to Follow:**

* **Markdown File Operations:**
  ```python
  # Always use this pattern for reading markdown with frontmatter:
  def read_content_file(file_path: str) -> dict:
      """Read markdown file and parse YAML frontmatter."""
      try:
          with open(file_path, 'r', encoding='utf-8') as f:
              content = f.read()

          # Split frontmatter and body
          if content.startswith('---'):
              parts = content.split('---', 2)
              frontmatter = yaml.safe_load(parts[1])
              body = parts[2].strip()
              return {**frontmatter, 'body': body}
          else:
              return {'body': content}
      except Exception as e:
          logger.error(f"Failed to read {file_path}: {e}")
          raise
  ```

* **API Route Structure:**
  ```python
  @router.get("/content/{content_id}")
  async def get_content_item(
      content_id: str,
      current_user: User = Depends(get_current_user)
  ) -> ContentResponse:
      """Retrieve a single content item by ID.

      Requires authentication. Returns 404 if not found or user lacks permission.
      """
      content = await content_service.get_by_id(content_id, current_user)
      if not content:
          raise HTTPException(status_code=404, detail="Content not found")
      return ContentResponse.from_service_model(content)
  ```

**Debugging Assistance:**
* All logging should use Python's logging module with appropriate levels (DEBUG, INFO, WARNING, ERROR)
* Include request IDs in logs for tracing user actions across service layers
* When asking AI to debug: provide full error traceback, relevant code section, and steps to reproduce

**Extending the System:**
* Before adding new features, ask AI to review this CLAUDE.md file and confirm alignment with architecture principles
* Request AI to generate matching tests for any new service functions
* Ask AI to update relevant documentation sections when adding new endpoints or changing data schemas

### 15. Deployment Checklist

**Initial Server Setup:**
- [ ] Install Python 3.11+ on server
- [ ] Install Nginx and configure reverse proxy with SSL (Let's Encrypt)
- [ ] Create dedicated system user for application (e.g., `contenttrack`)
- [ ] Set up application directory structure: /var/www/content-tracking/
- [ ] Clone repository or transfer application files
- [ ] Create and configure .env file with production settings
- [ ] Create content_library/ directory with proper permissions
- [ ] Initialize SQLite databases with init_db script
- [ ] Create initial admin user account

**Application Configuration:**
- [ ] Set SECRET_KEY environment variable (generate with `openssl rand -hex 32`)
- [ ] Configure CONTENT_LIBRARY_PATH to point to markdown storage directory
- [ ] Set DATABASE_URL for SQLite connection
- [ ] Configure ALLOWED_HOSTS for production domain
- [ ] Set up log file paths and rotation

**Systemd Service Setup:**
- [ ] Create systemd service file: /etc/systemd/system/content-tracking.service
- [ ] Configure service to run Uvicorn with 4 workers
- [ ] Enable auto-restart on failure
- [ ] Enable service to start on boot

**Nginx Configuration:**
- [ ] Configure SSL certificates (Let's Encrypt recommended)
- [ ] Set up proxy_pass to Uvicorn (127.0.0.1:8000)
- [ ] Configure static file serving for /static/ and /exports/ paths
- [ ] Set appropriate headers (HSTS, CSP, etc.)
- [ ] Configure request size limits for exports

**Testing & Validation:**
- [ ] Run test suite on server: `pytest`
- [ ] Verify markdown file read/write permissions
- [ ] Test user login and authentication flow
- [ ] Create sample content item via web UI
- [ ] Verify content appears in filesystem as markdown file
- [ ] Test search and filter functionality
- [ ] Test DOCX export generation
- [ ] Test PDF export generation
- [ ] Verify multi-user access and permissions

**Post-Deployment Monitoring:**
- [ ] Set up server monitoring (uptime, disk space, memory)
- [ ] Configure application log monitoring
- [ ] Schedule regular backups of content_library/ directory
- [ ] Schedule regular backups of SQLite databases
- [ ] Document backup restoration procedure

---

## Part D: Quick Reference
---

### 16. Core User Workflows

**Workflow 1: Add New Content Item**
1. User logs in and navigates to "Add Content" page
2. Fills out form: title, content type (dropdown), publish date, URL, description, tags, categories
3. Optionally adds markdown body content in text area
4. Clicks "Save"
5. System validates input, generates markdown file in content_library/{content_type}/YYYY-MM-DD-slug.md
6. System updates SQLite search index
7. User redirected to content detail page showing saved item

**Workflow 2: Search and Filter Content**
1. User enters search query in main search bar (searches title, description, tags, body)
2. System returns initial results in content list view
3. User applies filters: date range, content type, category (sidebar or filter panel)
4. Results update dynamically as filters applied
5. User clicks content item to view details or edit

**Workflow 3: Generate Export Report**
1. User applies filters to get desired content set (e.g., "all blog posts from Q1 2024")
2. User clicks "Export" button and selects format (DOCX or PDF)
3. User selects which metadata fields to include in export
4. System generates formatted document with professional template
5. Download link appears; user downloads report file
6. Use case: share quarterly content report with stakeholders

**Workflow 4: Team Collaboration**
1. Admin creates user accounts for team members with appropriate roles
2. Editor logs in, creates/edits content items within their permissions
3. Viewer logs in, browses and searches content library, can export but not edit
4. All changes tracked implicitly via markdown file modification timestamps
5. Team uses external Git repository for markdown files (optional) to enable version control

### 17. Data Schema Reference

**Content Item YAML Frontmatter (Markdown File Header):**
```yaml
---
id: "unique-content-id-uuid"
title: "Blog Post Title: How to Track Content Effectively"
content_type: "blog"  # blog, video, podcast, social, whitepaper, case_study, etc.
status: "published"   # draft, published, archived
created_date: "2024-01-15"
updated_date: "2024-01-20"
publish_date: "2024-01-15"
author: "Jane Smith"
url: "https://example.com/blog/how-to-track-content"
description: "A comprehensive guide to content tracking strategies for marketing teams."
categories:
  - "Content Marketing"
  - "Productivity"
tags:
  - "content strategy"
  - "tracking"
  - "analytics"
custom_fields:
  target_audience: "Marketing Managers"
  word_count: 2500
  read_time: "12 minutes"
---

# Markdown body content starts here

This is the actual content body, which can include full markdown formatting...
```

**User Account Schema (SQLite Database):**
```sql
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT,
    role TEXT NOT NULL,  -- 'admin', 'editor', 'viewer'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
);
```

**Content Index Schema (SQLite Database with FTS5):**
```sql
-- Main content metadata table
CREATE TABLE content_items (
    id TEXT PRIMARY KEY,
    file_path TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    content_type TEXT NOT NULL,
    status TEXT,
    created_date DATE,
    updated_date DATE,
    publish_date DATE,
    author TEXT,
    url TEXT,
    description TEXT,
    categories_json TEXT,  -- JSON array
    tags_json TEXT,        -- JSON array
    custom_fields_json TEXT,  -- JSON object
    last_indexed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Full-text search index
CREATE VIRTUAL TABLE content_fts USING fts5(
    id UNINDEXED,
    title,
    description,
    body,
    tags,
    content='content_items',
    content_rowid='id'
);
```

---

## Part E: Success Criteria & Definition of Done
---

### 18. MVP Acceptance Criteria

**Feature Completeness:**
- [ ] Can create, read, update, delete content items via web UI
- [ ] All content stored as markdown files with YAML frontmatter
- [ ] Can search content by text query (title, description, tags, body)
- [ ] Can filter content by date range, content type, category, tags, author, status
- [ ] Can combine multiple filters and see accurate results
- [ ] Can export filtered content set to DOCX with professional formatting
- [ ] Can export filtered content set to PDF with professional formatting
- [ ] Multi-user authentication working (login, logout, session management)
- [ ] Role-based permissions enforced (admin, editor, viewer)
- [ ] Admin can manage user accounts (create, deactivate, change roles)

**Technical Quality:**
- [ ] Test coverage ≥75% for service layer functions
- [ ] All API endpoints have proper error handling and validation
- [ ] No security vulnerabilities in authentication flow
- [ ] Markdown files correctly parse and write YAML frontmatter
- [ ] SQLite index stays synchronized with markdown files
- [ ] Application handles file system errors gracefully
- [ ] No sensitive data exposed in logs or error messages

**Documentation Quality:**
- [ ] SETUP.md includes step-by-step deployment instructions for non-technical user
- [ ] USAGE.md includes screenshots and user workflows for all core features
- [ ] DEVELOPMENT.md includes guidance for AI-assisted maintenance and extension
- [ ] All service modules have comprehensive docstrings
- [ ] API automatically documented via FastAPI OpenAPI spec

**User Experience:**
- [ ] Clean, professional visual design (no "prototype" appearance)
- [ ] Responsive layout works on mobile, tablet, desktop
- [ ] Forms have clear validation messages and error states
- [ ] Search results appear within 2 seconds for libraries <1000 items
- [ ] Export generation completes within 10 seconds for <100 items
- [ ] Navigation is intuitive; user can accomplish tasks without documentation

**Deployment Readiness:**
- [ ] Application successfully deploys on Linux server (Ubuntu 22.04 LTS tested)
- [ ] Runs as systemd service with auto-restart on failure
- [ ] Nginx reverse proxy configured with SSL
- [ ] Backup procedure documented and tested
- [ ] Application remains stable for 7 days of continuous operation
- [ ] No memory leaks or resource exhaustion under normal usage

### 19. Post-MVP Roadmap Priorities

**Phase 2: Enhanced Analytics (Months 2-3)**
- Visual dashboard with content metrics: total items by type, publishing frequency, top categories
- Trend charts: content creation over time, tags frequency analysis
- Performance metrics integration: if user adds view counts/engagement to frontmatter, visualize trends

**Phase 3: Publishing Integrations (Months 4-5)**
- WordPress publishing: create/update posts directly from content tracking system
- Social media scheduling: connect to Buffer/Hootsuite API for scheduled posting
- Email newsletter integration: Mailchimp/SendGrid template generation from markdown

**Phase 4: Collaboration Features (Months 5-6)**
- Content approval workflows: draft → review → approved states with notifications
- Comments/notes on content items (stored as separate JSON or in markdown)
- Activity feed: who created/edited what content when
- Email notifications for content updates and status changes

**Phase 5: Advanced Reporting (Months 6-7)**
- Custom report builder: drag-and-drop fields to include in exports
- Scheduled reports: automatically generate and email reports weekly/monthly
- Branded templates: custom DOCX/PDF templates with client logos and styling
- Comparison reports: content performance vs. previous periods

**Future Enhancements (Backlog):**
- Mobile native apps (iOS/Android) for on-the-go content management
- AI-assisted content analysis: auto-tagging, readability scoring, SEO suggestions
- Media asset management: upload and track images, videos, PDFs associated with content
- Version control UI: browse markdown file history via Git integration
- Multi-language support: content tracking for translated content variants
- Public API with rate limiting: allow third-party integrations

---

## Document Version & Maintenance
**Version:** 1.0
**Last Updated:** 2025-10-25
**Maintained By:** Project Owner (AI-assisted)
**Review Cycle:** Update quarterly or when major features added

**Amendment Process:**
When new features or changes are proposed, update relevant sections of this document BEFORE implementation. Use AI assistant to ensure new additions align with established principles and constraints. Sections 1-6 (strategic) should remain stable; sections 7-13 (technical) may evolve as implementation proceeds.

---

**End of CLAUDE.md Project Brief**
