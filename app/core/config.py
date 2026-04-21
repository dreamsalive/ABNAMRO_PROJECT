"""
Application Configuration Module

This module manages all application-level configuration settings.

It uses Pydantic BaseSettings to:
- Load environment variables
- Provide default values for local development
- Ensure type-safe configuration handling

Configuration is automatically loaded from:
- Environment variables
- .env file (if present)
"""

from pydantic_settings import BaseSettings

# =========================================================
# APPLICATION SETTINGS
# =========================================================
class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Attributes:
        DATABASE_URL (str):
            Database connection string.
            Default: SQLite local file database (recipes.db)

    Environment loading priority:
        1. OS environment variables
        2. .env file
        3. Default values defined here
    """

    DATABASE_URL: str = "sqlite:///./recipes.db"

    class Config:
        """
        Pydantic configuration class.

        Attributes:
            env_file (str):
                Path to the environment file used for local development.
        """

        env_file = ".env"

# Global settings instance used across the application
settings = Settings()