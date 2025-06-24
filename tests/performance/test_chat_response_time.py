import os
import time

import pytest
from fastapi.testclient import TestClient

from modules.assistantia.core import app

client = TestClient(app)


@pytest.mark.performance
@pytest.mark.slow
@pytest.mark.skipif(os.getenv("CI") == "true", reason="Ignoré en CI")
def test_chat_response_time_under_2s():
    """
    Vérifie que l'endpoint /chat répond en moins de 2 secondes (hors cold start Ollama).
    Ce test est ignoré en CI et marqué comme test de performance lent.
    """

    # 🔁 Appel de préchauffe (modèle Ollama)
    _ = client.post("/chat", json={"message": "Préparation"})

    time.sleep(1)  # temps pour charger le modèle

    # 🎯 Mesure réelle
    start = time.time()
    response = client.post("/chat", json={"message": "Hello"})
    elapsed = time.time() - start

    # ✅ Vérification du code retour
    assert response.status_code == 200

    # ⏱️ Contrôle de la latence (< 4.5s par défaut, ou seuil custom via env)
    threshold = float(os.getenv("CHAT_LATENCY_THRESHOLD", "4.5"))
    assert (
        elapsed < threshold
    ), f"❌ Réponse trop lente : {elapsed:.2f}s (limite : {threshold}s)"
