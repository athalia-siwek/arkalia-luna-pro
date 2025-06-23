
import pytest
from fastapi.testclient import TestClient

from modules.assistantia.core import app, get_query_ollama, process_input


@pytest.fixture
def test_client() -> TestClient:
    """Client de test pour l'app FastAPI."""
    return TestClient(app)


def test_chat_route_exists():
    """✅ Vérifie que l'application FastAPI est bien instanciée."""
    assert app is not None


def test_process_input_empty():
    """✅ Teste le traitement d'une entrée vide."""
    assert process_input("") == "Tu as dit : "


def test_process_input_normal():
    """✅ Teste le traitement d'une entrée normale avec respect de la casse."""
    assert process_input("Bonjour") == "Tu as dit : Bonjour"


def test_chat_post(test_client: TestClient):
    """✅ Teste l'endpoint /chat avec une dépendance mockée."""

    def mock_query_ollama(msg: str, model: str = "mistral") -> str:
        return msg  # pas de doublon, le formatting se fait dans process_input

    try:
        # 🧪 Surcharge de la dépendance
        app.dependency_overrides[get_query_ollama] = lambda: mock_query_ollama

        response = test_client.post("/chat", json={"message": "Bonjour"})
        assert response.status_code == 200

        json_data = response.json()
        assert "réponse" in json_data
        assert json_data["réponse"] == "Tu as dit : Bonjour"

    finally:
        # 🧼 Nettoyage dans tous les cas
        app.dependency_overrides.clear()