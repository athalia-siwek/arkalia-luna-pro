import time

from fastapi.testclient import TestClient

from modules.assistantia.core import app

client = TestClient(app)


def test_chat_response_time_under_2s():
    """Assure que /chat répond en moins de 2 secondes."""
    start = time.time()
    response = client.post("/chat", json={"message": "Hello"})
    elapsed = time.time() - start

    assert response.status_code == 200
    assert elapsed < 2.0, f"Réponse trop lente : {elapsed:.2f}s"
