"""FastAPI application entry point for Content Tracking System.

This module initializes the FastAPI application, configures CORS,
registers all routers, and sets up application lifecycle events.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.init_db import init_database


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Application lifespan manager.

    Handles startup and shutdown events for the application.
    Initializes database and other resources on startup.
    """
    # Startup: Initialize database
    await init_database()
    print(f"✓ Database initialized at {settings.DATABASE_URL}")
    print(f"✓ Content library path: {settings.CONTENT_LIBRARY_PATH}")

    yield

    # Shutdown: Clean up resources
    print("Application shutting down...")


# Initialize FastAPI application
app = FastAPI(
    title="Content Tracking System API",
    description="REST API for managing content library with markdown-based storage",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint returning API status."""
    return {
        "message": "Content Tracking System API",
        "version": "0.1.0",
        "status": "operational",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "database": "connected",
        "content_library": str(settings.CONTENT_LIBRARY_PATH),
    }


# TODO: Register routers when implemented
# from app.routers import content, search, export, planning, auth
# app.include_router(content.router, prefix="/api/content", tags=["content"])
# app.include_router(search.router, prefix="/api/search", tags=["search"])
# app.include_router(export.router, prefix="/api/export", tags=["export"])
# app.include_router(planning.router, prefix="/api/planning", tags=["planning"])
# app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
