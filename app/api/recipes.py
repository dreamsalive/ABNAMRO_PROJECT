"""
Recipe API Router

This module defines all REST endpoints for managing recipes.

It provides:
- Create recipe
- Get recipes with filters
- Update recipe
- Delete recipe

Architecture:
- FastAPI router layer (HTTP layer)
- Delegates business logic to RecipeService
- Uses SQLAlchemy Session via dependency injection
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.recipe import RecipeCreate, RecipeUpdate
from app.services.recipe_service import RecipeService

router = APIRouter()
service = RecipeService()


# =========================================================
# CREATE RECIPE
# =========================================================
@router.post("/recipes")
def create_recipe(payload: RecipeCreate, db: Session = Depends(get_db)):
    """
    Create a new recipe.

    Args:
        payload (RecipeCreate): Recipe input data including:
            - name (str)
            - vegetarian (bool)
            - servings (int)
            - ingredients (list[str])
            - instructions (str)

        db (Session): Database session injected via dependency.

    Returns:
        Recipe: Created recipe object.

    Notes:
        - Ingredients are stored as JSON string in DB.
    """
    return service.create(db, payload)


# =========================================================
# GET RECIPES (WITH FILTERS)
# =========================================================
@router.get("/recipes")
def get_recipes(
    vegetarian: bool = None,
    servings: int = None,
    ingredient: str = None,
    exclude: str = None,
    search: str = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve recipes with optional filters.

    Filters supported:
        - vegetarian: filter vegetarian/non-vegetarian recipes
        - servings: filter by number of servings
        - ingredient: include recipes containing ingredient
        - exclude: exclude recipes containing ingredient
        - search: search text in instructions

    Args:
        vegetarian (bool, optional)
        servings (int, optional)
        ingredient (str, optional)
        exclude (str, optional)
        search (str, optional)
        db (Session): Database session

    Returns:
        List[Recipe]: List of matching recipes
    """
    
    filters = {
        k: v for k, v in {
            "vegetarian": vegetarian,
            "servings": servings,
            "ingredient": ingredient,
            "exclude": exclude,
            "search": search
        }.items() if v is not None
    }

    return service.get_all(db, filters)


# =========================================================
# UPDATE RECIPE
# =========================================================
@router.patch("/recipes/{recipe_id}")
def update_recipe(recipe_id: int, payload: RecipeUpdate, db: Session = Depends(get_db)):
    """
    Update an existing recipe.

    Args:
        recipe_id (int): ID of recipe to update
        payload (RecipeCreate): Full recipe payload (replace-style update)
        db (Session): Database session

    Returns:
        Recipe: Updated recipe object

    Raises:
        HTTPException (404): If recipe not found
    """
    
    updated = service.update(db, recipe_id, payload)

    if not updated:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return updated


# =========================================================
# DELETE RECIPE
# =========================================================
@router.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """
    Delete a recipe by ID.

    Args:
        recipe_id (int): ID of recipe to delete
        db (Session): Database session

    Returns:
        dict: Success message

    Raises:
        HTTPException (404): If recipe not found
    """

    success = service.delete(db, recipe_id)

    if not success:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return {"message": "Deleted successfully"}