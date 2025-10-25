# Architects Rationale Document
## Content Tracking System - Implementation Plan

**Date:** 2025-10-25
**Project:** Content Tracking System
**Architect:** Chief Software Architect (Claude Agent SDK)
**Document Version:** 1.0

---

## Executive Summary

This document records the architectural decision-making process for the Content Tracking System, a multi-client content management platform optimized for AI-assisted development by a non-technical builder. The chosen architecture balances pragmatic simplicity with maintainability and security requirements, synthesizing insights from three specialist developer personas.

**Final Architecture Decision:** Layered FastAPI Backend + Next.js Frontend with Docker Compose orchestration, deployed via Coolify (self-hosted PaaS).

---

## 1. Cognitive Squad Assembly

Based on the Strategic Constraint Tags in `CLAUDE.md`, the following three-person cognitive squad was assembled:

### Selected Personas:

1. **@dev_pragmatist**
   - **Selection Rationale:** The `[Philosophy:Pragmatism]` tag explicitly mandates this persona. User is a non-technical builder using AI-assisted development tools (Claude, Cursor) with no hard deadlines, requiring the fastest path to a working MVP without unnecessary complexity.
   - **Core Focus:** Ship simple, functional solution; minimize time-to-first-deployment; accept strategic technical debt.

2. **@dev_custodian**
   - **Selection Rationale:** The `[Constraint:Simplicity]` and `[Constraint:Documentation]` tags require code optimized for AI-assisted maintenance. This persona ensures comprehensive docstrings, clear service boundaries, and self-documenting code that AI models can easily parse and modify.
   - **Core Focus:** Long-term maintainability; extensive testing and documentation; clear architectural patterns.

3. **@dev_security_hawk**
   - **Selection Rationale:** Multi-user system with role-based access from day one, multi-client data separation, file system operations (markdown import/export), and self-hosted deployment create significant security surface area. This persona proactively identifies vulnerabilities.
   - **Core Focus:** Authentication security; input validation; access control; preventing injection attacks and unauthorized file access.

---

## 2. Core Architectural Conflict

### The Central Tension:
**Monolithic Simplicity vs. Layered Maintainability & Security**

### Competing Proposals:

#### **@dev_pragmatist's Position: Next.js-Only Monolith**

**Architecture:**
- Single Next.js 16 application using App Router API routes for backend logic
- SQLite database as sole data store (no dual markdown+database storage)
- File operations handled directly in API routes
- Export generation using client-side libraries (docx.js, react-pdf)

**Advantages:**
- Single codebase → faster development
- No Docker orchestration complexity for local dev
- Fewer moving parts → easier initial deployment
- Simpler mental model for non-technical builder

**Disadvantages:**
- Mixing frontend and backend concerns in API routes reduces clarity
- Harder to enforce security boundaries (direct filesystem access from API routes)
- File operations and markdown parsing logic scattered across route handlers
- AI assistants struggle more with mixed-concern code than layered services

---

#### **@dev_custodian + @dev_security_hawk's Position: Layered Backend + Frontend**

**Architecture:**
- FastAPI backend: dedicated service layer for business logic, file operations, security
- Next.js frontend: pure UI layer with API client
- Markdown files as source of truth + SQLite index for performance
- Strong API boundary for authentication, validation, and access control

**Advantages:**
- Clear separation of concerns → easier AI-assisted maintenance
- Service layer functions are testable in isolation
- Explicit API contracts (Pydantic models) enforce validation
- Security boundaries: all file operations behind authenticated API
- Comprehensive docstrings and type hints guide AI code generation

**Disadvantages:**
- Two separate applications require Docker Compose orchestration
- More configuration overhead (CORS, environment variables for both services)
- Slightly longer initial setup time
- Requires understanding of client-server architecture

---

## 3. Synthesized Architectural Decision

### **Decision: Layered FastAPI + Next.js Architecture with Pragmatic Optimizations**

### Justification:

**Security Requirements Mandate Backend Separation:**
- Multi-client content requires strict data isolation (client A cannot access client B's files)
- File system operations (import .md files, write exports) must be validated server-side before execution
- Markdown file paths must never be directly exposed to frontend (use content IDs only)
- A dedicated API layer with authentication middleware is the most auditable approach for these security concerns

**AI-Assisted Maintainability Favors Layered Services:**
- The `[Constraint:Simplicity]` tag explicitly optimizes for "AI-assisted maintenance by non-technical builder"
- Counter-intuitively, a **layered architecture with clear service boundaries is MORE understandable for AI tools** than a monolithic Next.js app mixing concerns
- Explicit service functions with comprehensive docstrings (e.g., `markdown_service.py::read_content_file()`) are easier for AI to locate, understand, and modify than route handlers with embedded business logic
- Pydantic models provide self-documenting API contracts that AI assistants can reference when generating code

**Pragmatic Simplifications Applied:**
1. **Docker Compose for Single-Command Development:** Despite having two services, `docker-compose up --build` provides a one-command local development environment (satisfies pragmatist's speed requirement)
2. **Coolify for Deployment:** Self-hosted PaaS treats Docker Compose as a single unit; user doesn't manage services individually (satisfies self-hosted constraint with minimal complexity)
3. **SQLite Over PostgreSQL:** Keeps database setup trivial for MVP scale (satisfies pragmatist's "boring technology" principle)
4. **File-Based Configuration:** YAML files for content types, categories, tags (no admin UI needed for MVP configuration)

### Hybrid Implementation Strategy:

**Backend (FastAPI):**
- Thin service layer: no over-abstraction or premature optimization
- Explicit error handling with structured error responses
- Comprehensive docstrings (Google style) for every function
- Type hints throughout (aids AI understanding and IDE support)

**Frontend (Next.js 16):**
- Leverage React Server Components where possible (reduces client-side complexity)
- shadcn/ui components (copy-to-project approach = full control, easier for AI to modify)
- Tailwind CSS 4 utility classes (declarative, AI-friendly styling)

**Development Workflow:**
- Local: `docker-compose up` (frontend + backend + shared volumes)
- AI-assisted development: Claude/Cursor can read service layer code and generate matching route handlers, tests, or frontend API calls
- Testing: Separate test suites for backend (pytest) and frontend (Jest/Vitest)

**Deployment:**
- Coolify connects to Git repository
- Push to main branch → automatic deployment of both services
- Nginx reverse proxy configured by Coolify (SSL via Let's Encrypt)

---

## 4. Key Architectural Decisions & Trade-offs

### Decision 1: Markdown Files as Source of Truth + SQLite Index

**Chosen Approach:** Dual storage (markdown files + SQLite metadata index)

**Rationale:**
- Markdown files satisfy `[Constraint:Portability]` (future-proof, version control-friendly)
- SQLite index provides fast search/filtering without scanning all files
- Index is regenerated on app start or manual sync (simple synchronization strategy)

**Trade-off Accepted:**
- Complexity of maintaining synchronization between files and database
- **Mitigation:** Clear service function (`sync_index_from_files()`) handles regeneration; comprehensive logging tracks sync operations

---

### Decision 2: Docxtemplater (Node.js) for DOCX Export

**Chosen Approach:** Use Docxtemplater library (requires Node.js runtime in backend container)

**Rationale:**
- Template-based generation with Handlebars-style syntax (non-technical user can edit templates)
- Industry-standard for branded document generation
- Supports custom templates → user can add client-specific branding

**Trade-off Accepted:**
- Requires Node.js installation in Python backend container (adds ~50MB to Docker image)
- **Mitigation:** Multi-stage Docker build keeps final image size reasonable; Docxtemplater is more mature than Python alternatives (python-docx-template)

**Alternative Considered:** pandoc with pypandoc (rejected due to limited template customization compared to Docxtemplater)

---

### Decision 3: Multi-Client Organization via Custom Fields (MVP)

**Chosen Approach:** Use `custom_fields.client` in YAML frontmatter for client association

**Rationale:**
- Avoids premature complexity of multi-tenancy architecture
- Filtering by `custom_fields.client` is straightforward in SQL queries
- Allows flexible organizational schemes (some users may not need client separation)

**Trade-off Accepted:**
- Not as robust as dedicated multi-tenancy with database-level isolation
- **Post-MVP Path:** Can migrate to tenant-specific databases or table prefixes if needed

---

### Decision 4: Session-Based Authentication with JWT (MVP)

**Chosen Approach:** JWT tokens stored in HTTP-only cookies

**Rationale:**
- Stateless authentication (backend doesn't store session state)
- HTTP-only cookies prevent XSS attacks (JavaScript cannot access token)
- Standard pattern with strong library support (python-jose)

**Trade-off Accepted:**
- Slightly more complex than basic session cookies
- **Mitigation:** Well-documented pattern; AI assistants have extensive training data on JWT implementation

---

## 5. Security Analysis (by @dev_security_hawk)

### Critical Security Measures Enforced:

1. **Markdown Import Validation:**
   - File type whitelist: only `.md` files accepted
   - File size limit: max 10MB per file (prevents DoS via large uploads)
   - YAML frontmatter parsing with safe_load (prevents code injection)
   - Markdown body sanitization: strip script tags, limit HTML subset

2. **File Path Security:**
   - Never expose filesystem paths to frontend (use UUIDs as content IDs)
   - Backend constructs file paths from content_type + ID (prevents path traversal)
   - Validate content_type against whitelist before constructing paths

3. **Authentication & Authorization:**
   - All API endpoints require authentication (except /login, /register)
   - Role-based access control enforced at service layer (not just route decorators)
   - Admin-only endpoints: user management, configuration changes
   - Editor role: create/edit own content + view all
   - Viewer role: read-only access, can export but not modify

4. **Export Security:**
   - Template rendering with Jinja2 auto-escaping enabled
   - User-provided metadata sanitized before insertion into templates
   - Generated files stored in temporary directory with auto-cleanup (prevents disk exhaustion)

5. **Database Security:**
   - Prepared statements only (Pydantic models → SQLite via parameterized queries)
   - No raw SQL from user input
   - Password hashing with bcrypt (12+ rounds, salted)

---

## 6. AI-Assisted Development Optimizations

### Design Choices Optimized for Claude/Cursor:

1. **Comprehensive Docstrings:**
   - Every function includes Google-style docstring with Args, Returns, Raises sections
   - AI can parse docstrings to understand function purpose and generate correct calls

2. **Explicit Type Hints:**
   - Python: all function signatures use type hints (str, dict, List[ContentItem], etc.)
   - TypeScript: strict mode enabled; all props and return types explicitly typed
   - AI models use type information to generate correct code and catch errors

3. **Service-Oriented Architecture:**
   - Business logic lives in `services/` modules, not route handlers
   - AI can easily locate relevant service function: "find content creation logic" → `markdown_service.py::create_content_item()`
   - Each service function does ONE thing (single responsibility)

4. **Example-Driven Code Patterns:**
   - Section 14 of CLAUDE.md includes example patterns for markdown parsing and API routes
   - AI can copy these patterns when generating new similar code

5. **Clear Error Handling:**
   - All exceptions include context (file path, user ID, operation name)
   - Error responses follow consistent structure: `{"error": "code", "message": "readable", "details": {...}}`
   - AI can generate matching error handling in new code by referencing existing patterns

---

## 7. Phased Implementation Strategy

### Phase 1: Foundation (Week 1-2)
**Goal:** Basic project structure, development environment, core data models

- Set up Docker Compose with FastAPI + Next.js + shared volumes
- Define Pydantic models for Content, User, Config
- Implement markdown_service: read, write, parse frontmatter
- Create SQLite schema and init_db script
- Build basic Next.js pages (home, content list, content detail)

### Phase 2: Core CRUD (Week 3-4)
**Goal:** Full content management workflow via UI

- Backend: content CRUD API endpoints (create, read, update, delete)
- Frontend: content list view with sortable table
- Frontend: content detail page with edit form
- Frontend: new content creation form
- Markdown import: file upload UI + backend import service
- SQLite index synchronization

### Phase 3: Search & Filtering (Week 4-5)
**Goal:** Advanced content discovery

- Backend: search_service with FTS5 full-text search
- Backend: filter API with date ranges, content type, status, tags
- Frontend: search bar with live results
- Frontend: filter panel with multi-select dropdowns
- Frontend: saved filter presets (localStorage)

### Phase 4: Authentication & Multi-User (Week 5-6)
**Goal:** Secure multi-user access with roles

- Backend: auth_service with JWT token generation
- Backend: user CRUD endpoints (admin only)
- Frontend: login/logout pages
- Frontend: user management UI (admin only)
- Role-based access control middleware

### Phase 5: Export Functionality (Week 6-7)
**Goal:** Professional report generation

- Backend: export_service with Docxtemplater for DOCX
- Backend: export_service with WeasyPrint for PDF
- Frontend: export button with format selection
- Frontend: export options modal (select fields, choose template)
- Branded export templates (default + custom)

### Phase 6: Multi-Client Organization (Week 7-8)
**Goal:** Separate content views per client

- Add `client` field to content schema
- Backend: filter content by client (enforce in queries)
- Frontend: client selector dropdown
- Frontend: client-specific dashboard view
- Migration script for existing content (add client field)

### Phase 7: Future Content Planning (Week 8)
**Goal:** Separate planning view for content pipeline

- Backend: status workflow states (To Do, In Progress, UAT, Reviewed, Approved)
- Frontend: future-planning page with kanban-style view
- Frontend: drag-and-drop status transitions
- Backend: status transition validation

### Phase 8: Testing & Documentation (Week 9)
**Goal:** Production readiness

- Backend: pytest test suite (75%+ coverage)
- Frontend: Jest test suite for components
- SETUP.md: deployment instructions for Coolify
- USAGE.md: user guide with screenshots
- DEVELOPMENT.md: AI-assisted maintenance guide

### Phase 9: Deployment & Validation (Week 10)
**Goal:** Live production environment

- Deploy to user's server via Coolify
- SSL certificate via Let's Encrypt
- Backup procedure setup and documentation
- Load testing with sample content library
- User acceptance testing

---

## 8. Testing Strategy

### Backend Testing (pytest):
- **Unit Tests:** Service layer functions in isolation (mock file I/O, database)
- **Integration Tests:** API endpoints with test database and temporary file directory
- **Coverage Target:** 75%+ for service layer, 60%+ overall
- **Test Data:** Fixture markdown files in `tests/fixtures/`

### Frontend Testing (Jest/Vitest):
- **Component Tests:** Render tests for UI components (ContentCard, FilterPanel)
- **Integration Tests:** User flows (create content, apply filters, export)
- **Coverage Target:** 60%+ for components
- **Mocking:** Mock API calls with MSW (Mock Service Worker)

### Security Testing:
- **Manual Penetration Testing:** Test file upload restrictions, path traversal attempts, SQL injection
- **Automated Scanning:** Run OWASP ZAP or similar tool against API endpoints
- **Authentication Tests:** Verify JWT expiry, role enforcement, logout behavior

---

## 9. Deployment Architecture (Coolify)

### Infrastructure Components:

1. **Docker Compose Services:**
   - `frontend`: Next.js app (port 3000 internally)
   - `backend`: FastAPI app (port 8000 internally)
   - `shared_volume`: content_library/ and data/ directories

2. **Coolify Configuration:**
   - Git repository: user pushes to `main` branch → auto-deploy
   - Environment variables: set via Coolify UI (SECRET_KEY, DATABASE_URL)
   - Nginx reverse proxy: configured by Coolify
     - `/api/*` → backend:8000
     - `/*` → frontend:3000
   - SSL: Let's Encrypt certificate auto-renewal

3. **Backup Strategy:**
   - Daily cron job: `tar -czf backup-$(date +%Y%m%d).tar.gz content_library/ data/`
   - Backups stored in separate volume (not in Docker container)
   - Retention: 30 days of daily backups

---

## 10. Migration Plan for Existing Content

### User has existing .md files from external content creation system:

**Step 1: Prepare Import Directory**
- User places existing .md files in `imports/` directory on server
- Files can be in any structure; import script will flatten and organize by content_type

**Step 2: Run Import Script**
```bash
python -m app.services.markdown_service --import /path/to/imports/
```

**Import Process:**
1. Scan directory recursively for .md files
2. Parse each file's YAML frontmatter
3. Validate required fields (title, content_type); prompt for missing data
4. Generate UUID for content ID if not present
5. Copy file to content_library/{content_type}/{ID}.md (standardize naming)
6. Update SQLite index with metadata
7. Generate import report: success count, error list

**Step 3: Verify Import**
- User logs into web UI
- Checks content list to confirm all items imported
- Spot-checks content detail pages for accuracy

**Error Handling:**
- Files with invalid YAML: logged to `import_errors.log`, skipped (no crash)
- Duplicate titles: append UUID to title, log warning
- Missing required fields: prompt user interactively or use defaults (e.g., content_type="blog")

---

## 11. Post-MVP Roadmap Alignment

This architecture supports future enhancements without major refactoring:

1. **Analytics Dashboard (Phase 2):**
   - Add analytics_service to backend
   - Add chart components to frontend (recharts library)
   - Query SQLite for aggregated metrics (content by type, publish frequency)

2. **Publishing Integrations (Phase 3):**
   - Add integrations/ directory to backend
   - Implement WordPress API client, social media clients
   - Add "Publish" button to content detail page

3. **Collaboration Features (Phase 4):**
   - Extend content schema with comments field (JSON array)
   - Add notifications_service for email alerts
   - WebSocket connection for real-time updates (optional)

4. **Advanced Reporting (Phase 5):**
   - Extend export_service with report builder logic
   - Add template editor UI for admin users
   - Scheduled exports via cron jobs (backend task scheduler)

---

## 12. Definition of Done for MVP

### Feature Completeness Checklist:

- [ ] Can import .md files from folder (batch import via CLI or web upload)
- [ ] Can create, edit, delete content items via web UI
- [ ] Can filter content by client, status, content type, tags, date range
- [ ] Can search content by text query (title, description, tags, body)
- [ ] Can export filtered content set to DOCX with branded template
- [ ] Can export filtered content set to PDF
- [ ] Multi-user authentication with admin/editor/viewer roles
- [ ] Client-specific content views (filter by client field)
- [ ] Status workflow: To Do → In Progress → UAT → Reviewed → Approved
- [ ] Future Content Planning view (separate page for planning pipeline)
- [ ] Professional, mobile-responsive UI design (shadcn/ui components)

### Technical Quality Checklist:

- [ ] Backend test coverage ≥75% (service layer)
- [ ] Frontend test coverage ≥60% (components)
- [ ] No security vulnerabilities (OWASP Top 10 checks pass)
- [ ] All service functions have comprehensive docstrings
- [ ] API documented via FastAPI automatic OpenAPI spec
- [ ] SETUP.md deployment guide complete and tested
- [ ] DEVELOPMENT.md AI-assisted maintenance guide complete

### Deployment Readiness Checklist:

- [ ] Application deploys successfully via Coolify
- [ ] SSL certificate configured (Let's Encrypt)
- [ ] Backup procedure documented and tested
- [ ] Application stable for 7+ days continuous operation
- [ ] No memory leaks or resource exhaustion under normal load

---

## 13. Risk Assessment & Mitigation

### Risk 1: Markdown + SQLite Synchronization Bugs
**Likelihood:** Medium
**Impact:** High (data inconsistency)
**Mitigation:**
- Comprehensive unit tests for sync logic
- Manual sync command available to rebuild index from files
- Logging of all sync operations for debugging

### Risk 2: Docxtemplater Integration Complexity
**Likelihood:** Medium
**Impact:** Medium (delayed export feature)
**Mitigation:**
- Prototype DOCX export early (Phase 5, Week 6)
- Fallback option: simple plaintext export if Docxtemplater issues arise
- Document template syntax in USAGE.md with examples

### Risk 3: Non-Technical User Deployment Challenges
**Likelihood:** Low (Coolify simplifies deployment)
**Impact:** High (user cannot deploy application)
**Mitigation:**
- Step-by-step SETUP.md with screenshots
- Video walkthrough of Coolify deployment process
- Offer one-time deployment assistance call if needed

### Risk 4: AI-Assisted Development Learning Curve
**Likelihood:** Low (user already uses Claude/Cursor)
**Impact:** Medium (slower development pace)
**Mitigation:**
- DEVELOPMENT.md includes specific prompts for common tasks
- Example patterns in CLAUDE.md (Section 14) guide AI code generation
- Encourage user to ask AI to explain code before modifying

---

## 14. Success Metrics for Architecture Decision

**The chosen architecture will be considered successful if:**

1. **AI-Assisted Development Velocity:**
   - Non-technical builder can add new content types via AI assistance in <1 hour
   - Adding new API endpoints takes <30 minutes with AI code generation
   - AI-generated code passes linting and type checking on first attempt >80% of the time

2. **Deployment Simplicity:**
   - Initial deployment to Coolify takes <2 hours (including DNS setup)
   - Future deployments automated via Git push (zero manual steps)

3. **Security Posture:**
   - Zero critical vulnerabilities in production (OWASP ZAP scan passes)
   - No unauthorized access incidents in first 6 months

4. **Maintainability:**
   - User can modify service layer code with AI assistance without breaking tests
   - Adding new service functions requires minimal context (docstrings provide sufficient guidance)

---

## 15. Conclusion

The synthesized architecture balances three competing concerns:

1. **Pragmatic Simplicity:** Docker Compose + Coolify provide single-unit deployment despite layered services
2. **AI-Assisted Maintainability:** Clear service boundaries and comprehensive docstrings optimize for Claude/Cursor code generation
3. **Security & Robustness:** Dedicated backend with authentication middleware and input validation protects multi-client data

This decision prioritizes long-term success over short-term speed, recognizing that the `[Constraint:Simplicity]` tag refers to **maintenance simplicity**, not **architectural simplicity**. A well-documented layered architecture is simpler for AI tools to maintain than a tangled monolith.

**Next Step:** Proceed to `task_deps.md` for granular implementation tasks.

---

**Document Prepared By:** Chief Software Architect
**Cognitive Squad:** @dev_pragmatist, @dev_custodian, @dev_security_hawk
**Strategic Tags Applied:** [Philosophy:Pragmatism], [Constraint:Simplicity], [Constraint:Portability], [Constraint:Self-Hosted], [Constraint:Documentation]
