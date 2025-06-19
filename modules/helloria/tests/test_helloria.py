from fastapi.testclient import TestClient

from modules.helloria.core import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_echo():
    response = client.post("/echo", json={"message": "Salut"})
    assert response.status_code == 200
    assert response.json()["echo"] == "Salut"


def test_ping():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
