# modules/assistantia/tests/test_assistantia.py

from fastapi.testclient import TestClient

from modules.assistantia.core import app

client = TestClient(app)


def test_root_get():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "AssistantIA module actif" in response.json()["message"]


def test_chat_post():
    response = client.post("/chat", json={"message": "Bonjour"})
    assert response.status_code == 200
    assert "response" in response.json()
    assert "Bonjour" in response.json()["response"]
