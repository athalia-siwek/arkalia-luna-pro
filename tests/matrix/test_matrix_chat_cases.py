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
    response = client.post("/chat", json={"message": msg})
    assert response.status_code == 200
    assert "réponse" in response.json()
