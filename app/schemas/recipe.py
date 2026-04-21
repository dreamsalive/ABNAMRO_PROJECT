"""
Recipe Pydantic Schemas

This module defines the data validation and serialization layer
for the Recipe API.

It is responsible for:
- Validating incoming API requests
- Defining response structures
- Supporting partial updates (PATCH-like behavior)
- Enforcing type safety at API boundary

These schemas act as the contract between client and backend.
"""

from pydantic import BaseModel
from typing import List
from typing import List, Optional

# =========================================================
# CREATE SCHEMA
# =========================================================
class RecipeCreate(BaseModel):
    """
    Schema used for creating a new recipe.

    This schema is required for POST /recipes.

    All fields are mandatory.
    """

    name: str
    vegetarian: bool
    servings: int
    ingredients: List[str]
    instructions: str

# =========================================================
# RESPONSE SCHEMA
# =========================================================
class RecipeResponse(RecipeCreate):
    """
    Schema used for returning recipe data to clients.

    Extends RecipeCreate by adding database-generated fields.
    """

    id: int

# =========================================================
# UPDATE SCHEMA (PARTIAL UPDATE)
# =========================================================
class RecipeUpdate(BaseModel):
    """
    Schema used for updating an existing recipe.

    This supports partial updates (PATCH-style behavior),
    meaning any subset of fields can be provided.

    Example:
        {
            "servings": 4
        }

    Only provided fields will be updated.
    """
    
    name: Optional[str] = None
    vegetarian: Optional[bool] = None
    servings: Optional[int] = None
    ingredients: Optional[List[str]] = None
    instructions: Optional[str] = None