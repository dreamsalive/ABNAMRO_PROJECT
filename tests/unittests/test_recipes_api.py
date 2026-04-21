from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app

client = TestClient(app)


# =========================================================
# CREATE
# =========================================================
def test_create_recipe():
    payload = {
        "name": "Pizza",
        "vegetarian": True,
        "servings": 2,
        "ingredients": ["cheese"],
        "instructions": "Bake"
    }

    with patch("app.api.recipes.service.create") as mock_create:
        mock_create.return_value = {"id": 1, **payload}

        res = client.post("/recipes", json=payload)

        assert res.status_code == 200
        assert res.json()["id"] == 1
        mock_create.assert_called_once()


# =========================================================
# GET ALL (FILTERED)
# =========================================================
def test_get_recipes_filtered():
    mock_data = [{"id": 1, "name": "Veg Dish"}]

    with patch("app.api.recipes.service.get_all") as mock_get_all:
        mock_get_all.return_value = mock_data

        res = client.get("/recipes?vegetarian=true&ingredient=potato")

        assert res.status_code == 200
        assert res.json() == mock_data

        args, _ = mock_get_all.call_args
        assert isinstance(args[1], dict)
        assert "vegetarian" in args[1]


# =========================================================
# UPDATE SUCCESS
# =========================================================
def test_update_recipe_success():
    payload = {
        "name": "Updated Pizza",
        "vegetarian": True,
        "servings": 3,
        "ingredients": ["cheese"],
        "instructions": "Bake"
    }

    with patch("app.api.recipes.service.update") as mock_update:
        mock_update.return_value = {"id": 1, **payload}

        res = client.patch("/recipes/1", json=payload)

        assert res.status_code == 200
        assert res.json()["id"] == 1
        mock_update.assert_called_once()


# =========================================================
# UPDATE NOT FOUND
# =========================================================
def test_update_recipe_not_found():
    payload = {
        "name": "Pizza",
        "vegetarian": True,
        "servings": 2,
        "ingredients": ["cheese"],
        "instructions": "Bake"
    }

    with patch("app.api.recipes.service.update") as mock_update:
        mock_update.return_value = None

        res = client.patch("/recipes/1", json=payload)

        assert res.status_code == 404
        assert res.json()["detail"] == "Recipe not found"


# =========================================================
# DELETE SUCCESS
# =========================================================
def test_delete_recipe_success():
    with patch("app.api.recipes.service.delete") as mock_delete:
        mock_delete.return_value = True

        res = client.delete("/recipes/1")

        assert res.status_code == 200
        assert res.json()["message"] == "Deleted successfully"
        mock_delete.assert_called_once()


# =========================================================
# DELETE NOT FOUND
# =========================================================
def test_delete_recipe_not_found():
    with patch("app.api.recipes.service.delete") as mock_delete:
        mock_delete.return_value = False

        res = client.delete("/recipes/1")

        assert res.status_code == 404
        assert res.json()["detail"] == "Recipe not found"