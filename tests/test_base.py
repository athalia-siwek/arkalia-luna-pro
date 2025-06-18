# tests/test_base.py

from fastapi.testclient import TestClient

from helloria.core import app  # Assure-toi que helloria/core.py expose bien `app`

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    data = response.json()
    assert response.status_code == 200
    assert "message" in data
    assert "Arkalia" in data["message"]
