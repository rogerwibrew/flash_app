import pytest
import json
from app import app


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_flash_endpoint(client):
    payload = {
        "z": [0.5, 0.5],
        "T": 78.0,
        "P": 760.0,
        "components": [
            {"A": 8.07131, "B": 1730.63, "C": 233.426},
            {"A": 8.20417, "B": 1642.89, "C": 230.300},
        ],
    }
    response = client.post("/flash", json=payload)
    assert response.status_code == 200
    data = response.get_json()

    assert "x" in data
    assert "y" in data
    assert "beta" in data
    assert pytest.approx(sum(data["x"]), rel=1e-6) == 1.0
    assert pytest.approx(sum(data["y"]), rel=1e-6) == 1.0
    assert 0.0 <= data["beta"] <= 1.0
