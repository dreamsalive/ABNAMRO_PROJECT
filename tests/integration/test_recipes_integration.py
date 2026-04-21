import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db.database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# =========================================================
# TEST DATABASE (IN-MEMORY SQLITE)
# =========================================================
SQLALCHEMY_DATABASE_URL = "sqlite:///:recipes:"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


# =========================================================
# DB SETUP / TEARDOWN PER TEST
# =========================================================
@pytest.fixture(scope="function", autouse=True)
def setup_db():
    """
    Create fresh schema for every test.
    Ensures complete isolation between tests.
    """
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


# =========================================================
# DEPENDENCY OVERRIDE
# =========================================================
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# =========================================================
# CREATE + READ FLOW
# =========================================================
def test_create_and_get_recipe():
    payload = {
        "name": "Pizza",
        "vegetarian": True,
        "servings": 2,
        "ingredients": ["cheese", "tomato"],
        "instructions": "Bake in oven"
    }

    res = client.post("/recipes", json=payload)
    assert res.status_code == 200
    recipe_id = res.json()["id"]

    res = client.get("/recipes")
    assert res.status_code == 200
    assert len(res.json()) == 1


# =========================================================
# FILTER TEST
# =========================================================
def test_filter_recipe():
    client.post("/recipes", json={
        "name": "Pizza",
        "vegetarian": True,
        "servings": 2,
        "ingredients": ["cheese"],
        "instructions": "Bake"
    })

    res = client.get("/recipes?vegetarian=true")
    assert res.status_code == 200
    assert len(res.json()) == 1


# =========================================================
# UPDATE FLOW
# =========================================================
def test_update_recipe():
    res = client.post("/recipes", json={
        "name": "Soup",
        "vegetarian": True,
        "servings": 2,
        "ingredients": ["water"],
        "instructions": "Boil"
    })

    recipe_id = res.json()["id"]

    update_payload = {
        "name": "Updated Soup",
        "vegetarian": False,
        "servings": 4,
        "ingredients": ["water", "salt"],
        "instructions": "Boil more"
    }

    res = client.patch(f"/recipes/{recipe_id}", json=update_payload)

    assert res.status_code == 200
    assert res.json()["name"] == "Updated Soup"
    assert res.json()["servings"] == 4


# =========================================================
# UPDATE NOT FOUND
# =========================================================
def test_update_not_found():
    res = client.patch("/recipes/999", json={
        "name": "X",
        "vegetarian": True,
        "servings": 1,
        "ingredients": [],
        "instructions": "X"
    })

    assert res.status_code == 404


# =========================================================
# DELETE FLOW
# =========================================================
def test_delete_recipe():
    res = client.post("/recipes", json={
        "name": "Salad",
        "vegetarian": True,
        "servings": 1,
        "ingredients": ["lettuce"],
        "instructions": "Mix"
    })

    recipe_id = res.json()["id"]

    res = client.delete(f"/recipes/{recipe_id}")
    assert res.status_code == 200

    # verify actually deleted
    res = client.get("/recipes")
    assert res.status_code == 200
    assert len(res.json()) == 0