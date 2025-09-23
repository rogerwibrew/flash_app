# tests/test_flash_api.py
import json


def test_flash_missing_components(client):
    payload = {"z": [0.5, 0.5], "T": 78.0, "P": 760.0}
    response = client.post(
        "/flash", data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 400


def test_flash_invalid_z_length(client):
    payload = {
        "z": [0.5, 0.3, 0.2],  # wrong length
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
    assert response.status_code == 400


def test_flash_invalid_types(client):
    payload = {
        "z": ["a", "b"],  # wrong types
        "T": "not a number",
        "P": 760.0,
        "components": [
            {"A": "foo", "B": 1730.63, "C": 233.426},
            {"A": 8.20417, "B": "bar", "C": 230.300},
        ],
    }
    response = client.post(
        "/flash", data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 400
