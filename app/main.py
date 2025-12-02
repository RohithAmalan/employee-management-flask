# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routes import employees as employees_router
from . import models  # needed so SQLAlchemy sees the models

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee Management API",
    description="REST API for managing employee details (CRUD)",
    version="1.0.0",
)

# CORS (for frontend later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(employees_router.router)


@app.get("/")
def root():
    return {"message": "Employee Management API is running"}
