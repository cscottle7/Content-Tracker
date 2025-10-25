# Content Tracking System - Setup Guide

## Prerequisites

- Docker and Docker Compose installed on your system
- Git for version control (optional but recommended)
- 1GB+ free disk space

## Quick Start (Docker)

1. **Clone or download the project**
   ```bash
   cd /path/to/content-tracking
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```

3. **Edit .env file and set SECRET_KEY**
   ```bash
   # Generate a secure secret key
   openssl rand -hex 32

   # Add to .env file
   SECRET_KEY=your-generated-key-here
   ```

4. **Start the application**
   ```bash
   docker-compose up --build
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Manual Setup (Without Docker)

### Backend Setup

1. **Install Python 3.11+**

2. **Create virtual environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file**
   ```bash
   cp .env.example .env
   # Edit .env and set required variables
   ```

5. **Initialize databases**
   ```bash
   python -m app.db.init_db
   ```

6. **Run development server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Install Node.js 20+**

2. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

3. **Create .env.local file**
   ```bash
   cp .env.local.example .env.local
   # Edit .env.local if backend is not on localhost:8000
   ```

4. **Run development server**
   ```bash
   npm run dev
   ```

## Production Deployment

### Using Coolify (Recommended)

1. Connect your Git repository to Coolify
2. Coolify will detect docker-compose.yml automatically
3. Set environment variables in Coolify dashboard
4. Deploy with one click

### Manual Production Deployment

1. **Set production environment variables**
   ```bash
   DEBUG=false
   SECRET_KEY=<secure-random-key>
   ALLOWED_ORIGINS=https://yourdomain.com
   ```

2. **Build and run with docker-compose**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Configure Nginx reverse proxy**
   - See nginx configuration example in docs/nginx.conf.example
   - Set up SSL with Let's Encrypt

## Troubleshooting

### Backend won't start
- Check that ports 8000 is available
- Verify .env file exists and SECRET_KEY is set
- Check logs: `docker-compose logs backend`

### Frontend won't start
- Check that port 3000 is available
- Verify Node.js version is 20+
- Check logs: `docker-compose logs frontend`

### Database errors
- Ensure data/ directory has write permissions
- Try reinitializing: `rm -rf data/*.db && python -m app.db.init_db`

## Next Steps

- Read USAGE.md for user documentation
- Read DEVELOPMENT.md for developer guide
- Create your first content item via the web UI
