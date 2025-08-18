# app/db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --- Read & normalize DB URL ---
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/quakewatch",
)

# Some providers hand out postgres://; SQLAlchemy needs postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# --- Engine / Session / Base ---
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # avoids stale connections
    future=True,          # SQLAlchemy 2.0 style
    echo=False,           # flip to True locally to debug SQL
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
Base = declarative_base()

# --- FastAPI dependency (name matches imports in api.py) ---
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
