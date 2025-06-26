from fastapi.testclient import TestClient

from modules.assistantia.core import app

client = TestClient(app)


def test_chat_sql_injection_like():
    """Teste une entrée ressemblant à une injection SQL."""
    payload = {"message": "'DROP TABLE users;"}
    response = client.post("/chat", json=payload)
    assert response.status_code == 200, "Statut inattendu"
    assert "réponse" in response.json(), "Réponse manquante"
