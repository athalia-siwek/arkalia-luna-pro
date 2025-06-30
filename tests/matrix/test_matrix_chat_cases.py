from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from modules.assistantia.core import app

client = TestClient(app)


@pytest.mark.parametrize(
    "msg",
    [
        "Bonjour",
        "Que fais-tu ?",
        "Explique-moi les étoiles",
        "𐍈" * 50,
    ],
)
def test_chat_various_messages(msg):
    """Teste l'endpoint /chat avec divers messages."""
    with patch(
        "modules.assistantia.core.real_query_ollama", return_value="Réponse simulée pour le test"
    ):
        response = client.post("/chat", json={"message": msg})
        assert response.status_code == 200, "Statut inattendu"
        assert "réponse" in response.json(), "Réponse manquante"
