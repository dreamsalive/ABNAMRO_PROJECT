How to Run the Recipe Manager Application
==========================================

Clone the Repository
==========================================
git clone https://github.com/dreamsalive/ABNAMRO_PROJECT.git
cd ABNAMRO_PROJECT

Create Virtual Environment
=========================================
python3 -m venv venv

To Activate
=============================

Linux / Mac
=============================
source venv/bin/activate

Windows
==============================
venv\Scripts\activate

Install Dependencies
==============================
pip install -r requirements.txt

Run the Application

To Start the FastAPI server
===============================

uvicorn app.main:app --reload


Swagger UI
=========================
http://127.0.0.1:8000/docs

Database Info
===========================
Uses SQLite

File created automatically:
============================
recipes.db


Run unit tests and integration tests
====================================
pytest tests


Folder structure
=====================================
app/
 ├── api/          → FastAPI routes
 ├── core/         → config
 ├── db/           → database setup
 ├── models/       → SQLAlchemy models
 ├── schemas/      → Pydantic models
 ├── services/     → business logic
 └── main.py       → app entry point

tests/
 ├── unittests/    → service & API tests (mocked)
 └── integration/  → full system tests (real DB)

 

