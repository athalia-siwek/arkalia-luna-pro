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


def test_chat_post(test_client: TestClient):
    """Teste l'endpoint /chat avec une dépendance mockée."""

    def mock_query_ollama(msg: str, model: str = "mistral") -> str:
        return msg  # brut, sans "Tu as dit"

    app.dependency_overrides[get_query_ollama] = lambda: mock_query_ollama

    try:
        response = test_client.post("/chat", json={"message": "Bonjour"})
        assert response.status_code == 200
        response_data = response.json()
        assert "réponse" in response_data
        assert "Tu as dit : Bonjour" in response_data["réponse"]
        # Accepte aussi le contexte système enrichi
        if "Contexte système" in response_data["réponse"]:
            assert "ZeroIA" in response_data["réponse"]
    finally:
        app.dependency_overrides.clear()


def test_chat_post_empty_message(test_client: TestClient):
    """Teste l'endpoint /chat avec un message vide → 400 attendu."""
    response = test_client.post("/chat", json={"message": ""})
    assert response.status_code == 400
    assert "message vide" in response.json()["detail"].lower()


def test_chat_post_no_message_field(test_client: TestClient):
    """Teste l'endpoint /chat sans champ message → 422 attendu."""
    response = test_client.post("/chat", json={})
    assert response.status_code == 422  # Erreur de validation automatique FastAPI


def test_chat_post_long_message(test_client: TestClient):
    """Teste l'endpoint /chat avec un message très long (stress test)."""
    long_msg = "𐍈" * 1000

    def mock_query_ollama(msg: str, model: str = "mistral") -> str:
        return msg

    app.dependency_overrides[get_query_ollama] = lambda: mock_query_ollama

    try:
        response = test_client.post("/chat", json={"message": long_msg})
        assert response.status_code == 200
        assert "tu as dit" in response.json()["réponse"].lower()
    finally:
        app.dependency_overrides.clear()
