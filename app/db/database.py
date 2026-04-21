"""
Database Configuration Module

This module is responsible for:
- Creating the SQLAlchemy database engine
- Managing database sessions
- Providing dependency injection for FastAPI routes
- Defining the ORM base class for all models

It acts as the central database access layer of the application.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# =========================================================
# DATABASE ENGINE
# =========================================================
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # sqlite only
)

"""
Database engine instance.

Responsibilities:
- Establish connection pool to the database
- Execute SQL queries via ORM
- Manage DB connections lifecycle

Note:
- `check_same_thread=False` is required only for SQLite
  when used with FastAPI (async server + multiple threads)
"""
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# =========================================================
# ORM BASE CLASS
# =========================================================
Base = declarative_base()

"""
Base class for all ORM models.

All database models should inherit from this class:
    class Recipe(Base):
        __tablename__ = "recipes"
"""

# =========================================================
# FASTAPI DB DEPENDENCY
# =========================================================
def get_db():
    """
    Database dependency for FastAPI routes.

    This function:
    - Creates a new database session per request
    - Yields it to the route handler
    - Ensures session is always closed after request ends

    Usage in FastAPI:
        db: Session = Depends(get_db)

    Yields:
        Session: SQLAlchemy database session
    """
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()