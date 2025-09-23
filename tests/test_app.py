# tests/test_app.py
import json


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

    response = client.post(
        "/flash", data=json.dumps(payload), content_type="application/json"
    )

    assert response.status_code == 200
    data = response.get_json()
    assert "beta" in data
    assert "x" in data
    assert "y" in data
