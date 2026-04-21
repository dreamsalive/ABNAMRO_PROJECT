"""
Recipe Service Layer

This module contains the business logic for managing recipes.

Responsibilities:
- Handles all CRUD operations for recipes
- Applies filtering logic for queries
- Transforms data between Pydantic schemas and ORM models
- Encapsulates database interaction logic (via SQLAlchemy Session)

Architecture Role:
- Acts as the service layer between API (FastAPI) and DB (SQLAlchemy)
- Keeps API layer thin and free of business logic
"""

import json
from sqlalchemy.orm import Session
from app.models.recipe import Recipe
from app.schemas.recipe import RecipeCreate, RecipeUpdate


# =========================================================
# SERVICE CLASS
# =========================================================
class RecipeService:
    """
    Service class that contains all recipe-related business logic.

    Each method operates on a SQLAlchemy session and ensures
    proper creation, retrieval, updating, and deletion of recipes.
    """

    # -----------------------------------------------------
    # CREATE
    # -----------------------------------------------------
    def create(self, db: Session, data: RecipeCreate):
        """
        Create a new recipe in the database.

        Args:
            db (Session): SQLAlchemy database session
            data (RecipeCreate): Validated recipe input data

        Returns:
            Recipe: The created Recipe ORM object

        Notes:
            - Ingredients are stored as JSON string in DB
            - Transaction is committed immediately
        """
        
        recipe = Recipe(
            name=data.name,
            vegetarian=data.vegetarian,
            servings=data.servings,
            ingredients=json.dumps(data.ingredients),
            instructions=data.instructions
        )

        db.add(recipe)
        db.commit()
        db.refresh(recipe)
        return recipe
    
    # -----------------------------------------------------
    # READ (FILTERED QUERY)
    # -----------------------------------------------------
    def get_all(self, db: Session, filters: dict):
        """
        Retrieve all recipes with optional filtering.

        Supported filters:
            - vegetarian (bool)
            - servings (int)
            - ingredient (str): include recipes containing ingredient
            - exclude (str): exclude recipes containing ingredient
            - search (str): search keyword in instructions

        Args:
            db (Session): Database session
            filters (dict): Dictionary of filter conditions

        Returns:
            List[Recipe]: List of matching recipes
        """

        query = db.query(Recipe)

        if "vegetarian" in filters:
            query = query.filter(Recipe.vegetarian == filters["vegetarian"])

        if "servings" in filters:
            query = query.filter(Recipe.servings == filters["servings"])

        if "ingredient" in filters:
            query = query.filter(Recipe.ingredients.contains(filters["ingredient"]))

        if "exclude" in filters:
            query = query.filter(~Recipe.ingredients.contains(filters["exclude"]))

        if "search" in filters:
            query = query.filter(Recipe.instructions.contains(filters["search"]))

        return query.all()

    # -----------------------------------------------------
    # DELETE
    # -----------------------------------------------------
    def delete(self, db: Session, recipe_id: int):
        """
        Delete a recipe by its ID.

        Args:
            db (Session): Database session
            recipe_id (int): ID of the recipe to delete

        Returns:
            bool:
                True  → if deletion was successful
                False → if recipe was not found
        """

        recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

        if not recipe:
            return False

        db.delete(recipe)
        db.commit()
        return True
    
    # -------------------------
    # UPDATE
    # -------------------------
    def update(self, db: Session, recipe_id: int, data: RecipeUpdate):
      """
        Update an existing recipe (supports partial updates).

        This method behaves like PATCH:
        only provided fields are updated.

        Args:
            db (Session): Database session
            recipe_id (int): ID of recipe to update
            data (RecipeUpdate): Partial update payload

        Returns:
            Recipe | None:
                Updated Recipe object if found
                None if recipe does not exist
      """
      
      recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

      if not recipe:
        return None

      update_data = data.model_dump(exclude_unset=True)

      if "name" in update_data:
        recipe.name = update_data["name"]

      if "vegetarian" in update_data:
        recipe.vegetarian = update_data["vegetarian"]

      if "servings" in update_data:
        recipe.servings = update_data["servings"]

      if "ingredients" in update_data:
        recipe.ingredients = json.dumps(update_data["ingredients"])

      if "instructions" in update_data:
        recipe.instructions = update_data["instructions"]

      db.commit()
      db.refresh(recipe)

      return recipe

