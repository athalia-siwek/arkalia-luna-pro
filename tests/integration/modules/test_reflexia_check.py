# 📁 tests/integration/test_reflexia_check.py

import pytest
from fastapi.testclient import TestClient

from helloria.core import app  # ou là où tu exposes FastAPI


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_reflexia_check(client) -> None:
    # 🔎 Appel du endpoint Reflexia health (endpoint existant)
    response = client.get("/reflexia/health")

    # ✅ Statut HTTP attendu
    assert response.status_code == 200, f"Erreur HTTP : {response.status_code} - {response.text}"

    # ✅ Structure de la réponse attendue
    data = response.json()
    assert "status" in data, "Clé 'status' manquante dans la réponse"
    assert "module" in data, "Clé 'module' manquante dans la réponse"
    assert data["module"] == "reflexia", "Module incorrect dans la réponse"
