"""
Main Application Entry Point

This module initializes the FastAPI application and wires all components together.

Responsibilities:
- Creates FastAPI application instance
- Initializes database schema (tables)
- Registers API routers
- Acts as the entry point for the backend service

Architecture Role:
- Composition root of the application
- Wires together API, database, and service layers
"""

from fastapi import FastAPI
from app.api.recipes import router
from app.db.database import Base, engine

# =========================================================
# DATABASE INITIALIZATION
# =========================================================
Base.metadata.create_all(bind=engine)
"""
Creates all database tables defined in SQLAlchemy models.

Note:
- This is suitable for development/demo purposes.
- In production, migrations (e.g., Alembic) should be used instead.
"""

# =========================================================
# FASTAPI APPLICATION INSTANCE
# =========================================================
app = FastAPI(title="Recipe Manager")
"""
FastAPI application instance.

This is the main ASGI application that:
- Handles incoming HTTP requests
- Routes requests to API endpoints
- Generates OpenAPI documentation (/docs)
"""

# =========================================================
# ROUTER REGISTRATION
# =========================================================
app.include_router(router)
"""
Registers the Recipe API router.

All endpoints defined in:
    app/api/recipes.py

are now available under this application.
"""