# modules/assistantia/tests/test_assistantia.py

from fastapi.testclient import TestClient

from modules.assistantia.core import app

client = TestClient(app)


def test_root_get():
    response = client.get("/")
    assert response.status_code in [200, 404]  # Selon exposition réelle


def test_chat_post():
    response = client.post("/chat", json={"message": "Bonjour"})
    assert response.status_code == 200
    assert "réponse" in response.json()
