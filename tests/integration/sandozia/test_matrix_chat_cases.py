import os
import sys
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

# Ajout dynamique du chemin du projet pour garantir l'import correct
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

<<<<<<<< HEAD:tests/matrix/test_matrix_chat_cases.py
from core.ark_logger import ark_logger
from modules.assistantia.core import app
========
# Import après modification du path
from modules.assistantia.core import app  # noqa: E402
>>>>>>>> dev-migration:tests/integration/sandozia/test_matrix_chat_cases.py

client = TestClient(app)


def test_debug_routes():
    """Test de debug pour afficher les routes disponibles."""
    ark_logger.info("\n--- ROUTES DISPONIBLES ---", extra={"module": "matrix"})
    for route in app.routes:
        ark_logger.info(f"{route.path} | methods: {route.methods}", extra={"module": "matrix"})
    ark_logger.info("--- FIN ROUTES ---\n", extra={"module": "matrix"})
    # On ne fait pas d'assert pour ne pas bloquer


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
    """Teste l'endpoint /api/v1/chat avec divers messages."""
    with (
        patch(
            "modules.assistantia.core.real_query_ollama",
            return_value="Réponse simulée pour le test",
        ),
        patch("modules.assistantia.core._check_ollama_health", return_value=True),
    ):
        response = client.post("/api/v1/chat", json={"message": msg})
        assert response.status_code == 200, (
            f"Statut inattendu: {response.status_code} {response.text}"
        )
        assert "response" in response.json(), "Réponse manquante"
