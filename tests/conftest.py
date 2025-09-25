import pytest
from flash.app import app
from db.models import Base, Component
from db.database import SessionLocal, engine


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Create a clean in-memory SQLite database for tests,
    seed it with some known components.
    """
    # Rebind engine to in-memory database
    test_engine = engine.execution_options(sqlite_raw_colnames=True)
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    # Seed with ethanol + water
    db = SessionLocal()
    db.add_all(
        [
            Component(name="ethanol", A=8.20417, B=1642.89, C=230.300),
            Component(name="water", A=8.07131, B=1730.63, C=233.426),
        ]
    )
    db.commit()
    db.close()
    yield
    # Cleanup at end of session
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    """
    Provides a Flask test client that uses the test database.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
