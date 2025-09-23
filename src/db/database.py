"""
Database configuration and session management.
Handles creating the SQLite database and initializing tables.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# SQLite URL — file-based database stored in the project root.
# For testing, we'll override with an in-memory SQLite instance.
DATABASE_URL = "sqlite:///./flash.db"

# Create engine (connection to the database)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
    Initializes the database by creating all tables.
    Should be called at application startup.
    """
    Base.metadata.create_all(bind=engine)
