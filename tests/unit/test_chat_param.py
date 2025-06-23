from fastapi.testclient import TestClient

from modules.assistantia.core import app

client = TestClient(app)


def test_chat_with_lang_and_mode():
    """Vérifie que les paramètres `lang` et `mode` sont acceptés."""
    payload = {"message": "Salut", "lang": "fr", "mode": "friendly"}
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    assert "réponse" in response.json()
