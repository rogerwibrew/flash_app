"""
SQLAlchemy models for storing thermodynamic data (Antoine constants).
Each model corresponds to a table in the database.
"""

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

# Base class for our ORM models
Base = declarative_base()


class Component(Base):
    """
    Represents a chemical component with its Antoine equation constants.
    Antoine equation: log10(P_sat) = A - B / (T + C)
    """

    __tablename__ = "components"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # e.g. "ethanol"
    A = Column(Float, nullable=False)
    B = Column(Float, nullable=False)
    C = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Component(name={self.name}, A={self.A}, B={self.B}, C={self.C})>"
