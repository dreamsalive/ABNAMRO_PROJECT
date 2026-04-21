# Recipe Manager API
A simple FastAPI-based Recipe Management System built using a layered architecture with SQLAlchemy, Pydantic, and SQLite. The project supports full CRUD operations along with flexible filtering, and is designed with separation of concerns and testability in mind.



# Architecture Overview
The application follows a layered architecture:

Client
↓
FastAPI API Layer
↓
Service Layer
↓
SQLAlchemy ORM Layer
↓
SQLite Database




# Project Structure

app/
├── api/ # FastAPI route definitions
├── services/ # Business logic layer
├── models/ # SQLAlchemy ORM models
├── schemas/ # Pydantic request/response models
├── db/ # Database configuration
├── core/ # Application settings
└── main.py # Application entry point



# Core Components

## API Layer `app/api/recipes.py`
  
- Defines REST endpoints:
  - `POST /recipes`
  - `GET /recipes`
  - `PUT /recipes/{id}`
  - `DELETE /recipes/{id}`
- Delegates all logic to the service layer
- Handles HTTP request/response lifecycle



## Service Layer `app/services/recipe_service.py`

- Contains all business logic
- Supports:
  - Create recipe
  - Get recipes with filters
  - Update recipe (partial updates supported)
  - Delete recipe
- Handles ingredient serialization (JSON storage)



## Data Model `app/models/recipe.py`

- SQLAlchemy ORM model mapped to `recipes` table
- Fields:
  - id, name, vegetarian, servings
  - ingredients (stored as JSON string)
  - instructions


## Schema Layer `app/schemas/recipe.py`

- Request validation and response models
- Supports:
  - `RecipeCreate`
  - `RecipeUpdate` (partial updates via optional fields)
  - `RecipeResponse`


## Database Layer `app/db/database.py`

- Configures SQLAlchemy engine
- Provides session management via `get_db`
- Uses SQLite database


## Configuration `app/core/config.py`

- Uses Pydantic Settings
- Loads environment variables
- Defines database connection string



## Entry Point `app/main.py`
- Initializes FastAPI app
- Registers routers
- Creates database tables at startup



# API Flow

### Example: Create Recipe
Client → API Layer → Service Layer → ORM → Database

### Example: Get Recipes
Client → API Layer → Service Layer (filters applied) → Database



# Testing Strategy

## Unit Tests
- Focus on `RecipeService`
- Uses mocks for database session

## API Tests
- Tests FastAPI endpoints
- Mocks service layer

## Integration Tests
- Uses real SQLite database
- Tests full request → DB lifecycle



# Design Principles

- Separation of concerns (API / Service / DB / Schema)
- Single Responsibility Principle
- Dependency Injection (DB session via `get_db`)
- Testability via mocking boundaries


# Tech Stack

- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Pytest

