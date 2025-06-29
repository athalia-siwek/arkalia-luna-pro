import os
import time

import pytest
from fastapi.testclient import TestClient

from modules.assistantia.core import app, get_query_ollama

client = TestClient(app)


@pytest.mark.performance
@pytest.mark.slow
@pytest.mark.skipif(os.getenv("CI") == "true", reason="Ignoré en CI")
def test_chat_response_time_under_2s():
    """
    Vérifie que l'endpoint /chat répond en moins de 2 secondes (avec mock Ollama).
    Ce test est ignoré en CI et marqué comme test de performance lent.
    """

    def mock_query_ollama(msg: str, model: str = "mistral") -> str:
        """Mock rapide pour éviter les appels Ollama réels"""
        return f"Mock response: {msg}"

    # 🔧 Mock de la dépendance Ollama pour performance
    app.dependency_overrides[get_query_ollama] = lambda: mock_query_ollama

    try:
        # 🎯 Mesure réelle (sans cold start Ollama)
        start = time.time()
        response = client.post("/chat", json={"message": "Hello"})
        elapsed = time.time() - start

        # ✅ Vérification du code retour
        assert response.status_code == 200

        # ⏱️ Contrôle de la latence (< 2s avec mock)
        threshold = float(os.getenv("CHAT_LATENCY_THRESHOLD", "2.0"))
        assert (
            elapsed < threshold
        ), f"❌ Réponse trop lente : {elapsed:.2f}s (limite : {threshold}s)"
    finally:
        # 🧼 Nettoyage des overrides
        app.dependency_overrides.clear()


@pytest.mark.performance
def test_chat_response_time_with_real_ollama():
    """
    Test optionnel avec Ollama réel (plus lent, pour validation complète).
    """
    if not os.getenv("TEST_WITH_OLLAMA"):
        pytest.skip("TEST_WITH_OLLAMA non défini - skip test Ollama réel")

    # 🔁 Appel de préchauffe (modèle Ollama)
    _ = client.post("/chat", json={"message": "Préparation"})

    time.sleep(1)  # temps pour charger le modèle

    # 🎯 Mesure réelle
    start = time.time()
    response = client.post("/chat", json={"message": "Hello"})
    elapsed = time.time() - start

    # ✅ Vérification du code retour
    assert response.status_code == 200

    # ⏱️ Contrôle de la latence (< 10s avec Ollama réel)
    threshold = float(os.getenv("CHAT_LATENCY_THRESHOLD_REAL", "10.0"))
    assert elapsed < threshold, f"❌ Réponse trop lente : {elapsed:.2f}s (limite : {threshold}s)"
