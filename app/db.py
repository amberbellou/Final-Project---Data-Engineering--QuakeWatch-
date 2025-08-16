# app/db.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Read DB URL from environment or default to local Postgres
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/quakewatch"
)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
    echo=False  # Set to True for SQL logging during development
)

# Create sessionmaker factory
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)

# Base class for ORM models
Base = declarative_base()

# Optional: Session dependency (for FastAPI or scripts)
def get_db():
    """Dependency to get a new DB session (for FastAPI or scripts)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
