import pytest
from fastapi.testclient import TestClient

from modules.assistantia.core import app


@pytest.fixture(scope="module")
def test_client():
    """Client de test FastAPI pour tous les tests du module."""
    return TestClient(app)


def test_chat_post_empty_message(test_client: TestClient):
    """Teste l'endpoint /chat avec un message vide → erreur 400 attendue."""
    response = test_client.post("/chat", json={"message": ""})
    assert response.status_code == 400
    assert "Message vide" in response.json()["detail"] 