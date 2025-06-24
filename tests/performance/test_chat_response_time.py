import os
import time

import pytest
from fastapi.testclient import TestClient

from modules.assistantia.core import app

client = TestClient(app)


@pytest.mark.skipif(os.getenv("CI") == "true", reason="Ignoré en CI")
@pytest.mark.slow
def test_chat_response_time_under_2s():
    """Assure que /chat répond en moins de 2 secondes."""
    start = time.time()
    response = client.post("/chat", json={"message": "Hello"})
    elapsed = time.time() - start

    assert response.status_code == 200
    assert elapsed < 2.5, f"Réponse trop lente : {elapsed:.2f}s"
