import pytest
from unittest.mock import MagicMock

from app.services.recipe_service import RecipeService
from app.models.recipe import Recipe
from app.schemas.recipe import RecipeCreate, RecipeUpdate


service = RecipeService()


# =========================================================
# CREATE TEST
# =========================================================
def test_create_recipe():
    db = MagicMock()

    payload = RecipeCreate(
        name="Pizza",
        vegetarian=True,
        servings=2,
        ingredients=["cheese"],
        instructions="Bake"
    )

    result = service.create(db, payload)

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()
    assert result.name == "Pizza"
    assert result.vegetarian is True


# =========================================================
# GET ALL TEST (FILTERING)
# =========================================================
def test_get_all_filters():
    db = MagicMock()
    query = MagicMock()

    db.query.return_value = query
    query.filter.return_value = query
    query.all.return_value = []

    filters = {
        "vegetarian": True,
        "servings": 2,
        "ingredient": "potato",
        "exclude": "salmon",
        "search": "oven"
    }

    result = service.get_all(db, filters)

    db.query.assert_called_once_with(Recipe)
    query.filter.assert_called()
    query.all.assert_called_once()
    assert result == []


# =========================================================
# DELETE - SUCCESS
# =========================================================
def test_delete_recipe_success():
    db = MagicMock()

    recipe = MagicMock()
    query = db.query.return_value
    query.filter.return_value.first.return_value = recipe

    result = service.delete(db, 1)

    db.delete.assert_called_once_with(recipe)
    db.commit.assert_called_once()
    assert result is True


# =========================================================
# DELETE - NOT FOUND
# =========================================================
def test_delete_recipe_not_found():
    db = MagicMock()

    query = db.query.return_value
    query.filter.return_value.first.return_value = None

    result = service.delete(db, 1)

    assert result is False
    db.delete.assert_not_called()


# =========================================================
# UPDATE - SUCCESS (PARTIAL UPDATE)
# =========================================================
def test_update_recipe_success():
    db = MagicMock()

    recipe = MagicMock()
    query = db.query.return_value
    query.filter.return_value.first.return_value = recipe

    payload = RecipeUpdate(servings=5)

    result = service.update(db, 1, payload)

    assert result is not None
    assert recipe.servings == 5
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(recipe)


# =========================================================
# UPDATE - NOT FOUND
# =========================================================
def test_update_recipe_not_found():
    db = MagicMock()

    query = db.query.return_value
    query.filter.return_value.first.return_value = None

    payload = RecipeUpdate(servings=5)

    result = service.update(db, 1, payload)

    assert result is None
    db.commit.assert_not_called()