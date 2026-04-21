"""
Recipe ORM Model

This module defines the Recipe database model using SQLAlchemy ORM.

It represents the core entity of the application and is used to:
- Store recipe data in the database
- Map Python objects to database rows
- Support CRUD operations via SQLAlchemy sessions

Design Note:
- Ingredients are stored as a JSON string in a TEXT column
  (can be improved later using JSON type in PostgreSQL)
"""

from sqlalchemy import Column, Integer, String, Boolean, Text
from app.db.database import Base

# =========================================================
# RECIPE TABLE MODEL
# =========================================================
class Recipe(Base):
    """
    Recipe database model.

    Represents a single recipe entry in the system.

    Table:
        recipes

    Fields:
        id (int):
            Primary key, unique identifier for each recipe.

        name (str):
            Name of the recipe.
            Cannot be null.

        vegetarian (bool):
            Indicates whether the recipe is vegetarian.
            Default: False

        servings (int):
            Number of people the recipe serves.
            Cannot be null.

        ingredients (str):
            List of ingredients stored as JSON string.
            Example: '["tomato", "cheese"]'

        instructions (str):
            Cooking instructions in plain text.
    """
    
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    vegetarian = Column(Boolean, default=False)
    servings = Column(Integer, nullable=False)
    ingredients = Column(Text, nullable=False)  # JSON string
    instructions = Column(Text, nullable=False)