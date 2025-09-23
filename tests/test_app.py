# tests/test_app.py
import json


def test_flash_endpoint(client):
    resp = client.post(
        "/flash",
        json={
            "z": [0.5, 0.5],
            "T": 78.0,
            "P": 760.0,
            "components": ["water", "ethanol"],
        },
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert "x" in data and "y" in data
    assert isinstance(data["x"], list)
    assert isinstance(data["y"], list)


def test_flash_endpoint_component_not_found(client):
    resp = client.post(
        "/flash",
        json={"z": [1.0], "T": 100.0, "P": 760.0, "components": ["unobtainium"]},
    )
    assert resp.status_code == 404
    data = resp.get_json()
    assert "error" in data
    assert "not found" in data["error"].lower()


def test_flash_endpoint_invalid_input(client):
    resp = client.post(
        "/flash",
        json={"z": "not-a-list", "T": "hot", "P": 760.0, "components": ["water"]},
    )
    assert resp.status_code == 400
    data = resp.get_json()
    assert "error" in data
