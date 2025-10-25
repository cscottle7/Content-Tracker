# Content Tracking System

A comprehensive content management platform designed for professionals managing multiple content types across various channels. Track blog posts, videos, podcasts, social media content, and more—all in one intuitive interface with markdown-based storage.

## Features

- **Multi-format Content Tracking**: Support diverse content types with flexible metadata schemas
- **Markdown-Based Storage**: Each content item stored as portable .md files with YAML frontmatter
- **Powerful Search & Filtering**: Full-text search plus advanced filtering capabilities
- **Professional Export**: Generate DOCX and PDF reports with customizable templates
- **Self-Hosted**: Deploy on your own infrastructure with complete data control
- **Team Collaboration**: Multi-user support with role-based access control
- **AI-Maintainable**: Clean, well-documented codebase optimized for AI-assisted development

## Quick Start

### Prerequisites

- Docker and Docker Compose
- 1GB+ free disk space

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd content-tracking
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```

3. **Generate secret key**
   ```bash
   openssl rand -hex 32
   ```
   Add the generated key to `.env` as `SECRET_KEY`

4. **Start the application**
   ```bash
   docker-compose up --build
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Documentation

- **[Setup Guide](docs/SETUP.md)**: Detailed installation and deployment instructions
- **[Development Guide](docs/DEVELOPMENT.md)**: Developer documentation and API reference
- **[Project Brief](CLAUDE.md)**: Complete project specification and architecture

## Tech Stack

**Backend:**
- Python 3.11+ with FastAPI
- SQLite for metadata indexing
- Markdown file storage with YAML frontmatter

**Frontend:**
- Next.js 14 with TypeScript
- Tailwind CSS for styling
- shadcn/ui component library

**Deployment:**
- Docker and Docker Compose
- Nginx reverse proxy (production)
- Coolify-compatible for easy self-hosting

## Project Status

**Phase 1: Foundation** ✅ (Current)
- Project structure established
- Backend core with FastAPI
- Frontend core with Next.js
- Database initialization
- Testing infrastructure
- Docker configuration

**Phase 2: Core Features** (Next)
- Content CRUD operations
- Markdown file operations
- Search and filtering
- Basic UI components

**Phase 3: Export & Polish**
- DOCX/PDF export
- Complete UI/UX
- Performance optimization

## Contributing

This project is optimized for AI-assisted development. When contributing:

1. Review `CLAUDE.md` for project conventions
2. Follow established code patterns
3. Include tests with new features
4. Add comprehensive docstrings
5. Update documentation as needed

## License

[License information to be added]

## Support

For issues and questions:
- Check the [Development Guide](docs/DEVELOPMENT.md)
- Review existing GitHub issues
- Create a new issue with detailed information

---

**Built with AI-Native Development principles for maximum maintainability and extensibility.**
