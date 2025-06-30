from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from modules.assistantia.core import app, get_query_ollama


@pytest.fixture(scope="module")
def test_client():
    """Client de test FastAPI pour tous les tests du module."""
    return TestClient(app)


def test_root_get(test_client):
    """Teste l'endpoint racine (GET /) — tolère 404 si non défini."""
    response = test_client.get("/")
    assert response.status_code in [200, 404]


def test_chat_post(test_client):
    """Teste l'endpoint POST /chat avec un message simple"""

    def mock_query_ollama(prompt: str) -> str:
        return "Tu as dit : Bonjour"

    with patch("modules.assistantia.core.get_query_ollama", return_value=mock_query_ollama):
        response = test_client.post("/chat", json={"message": "Bonjour"})
        assert response.status_code == 200

        response_data = response.json()
        assert "réponse" in response_data
        # La réponse devrait contenir le message mocké
        response_text = response_data["réponse"]
        assert "Tu as dit : Bonjour" in response_text


def test_chat_post_empty_message(test_client: TestClient):
    """Teste l'endpoint /chat avec un message vide → 400 attendu."""
    response = test_client.post("/chat", json={"message": ""})
    assert response.status_code == 400
    assert "message vide" in response.json()["detail"].lower()


def test_chat_post_no_message_field(test_client: TestClient):
    """Teste l'endpoint /chat sans champ message → 422 attendu."""
    response = test_client.post("/chat", json={})
    assert response.status_code == 422  # Erreur de validation automatique FastAPI


def test_chat_post_long_message(test_client):
    """Teste l'endpoint POST /chat avec un message long"""
    long_msg = "A" * 1000

    def mock_query_ollama(prompt: str) -> str:
        return "Message reçu"

    with patch("modules.assistantia.core.get_query_ollama", return_value=mock_query_ollama):
        response = test_client.post("/chat", json={"message": long_msg})
        assert response.status_code == 200

        response_data = response.json()
        assert "réponse" in response_data
        assert "Message reçu" in response_data["réponse"]
