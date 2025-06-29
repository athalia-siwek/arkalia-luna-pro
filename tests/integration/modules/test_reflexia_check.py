# 📁 tests/integration/test_reflexia_check.py

import pytest
from fastapi.testclient import TestClient

from helloria.core import app  # ou là où tu exposes FastAPI


@pytest.fixture
def client() -> None:
    return TestClient(app)


def test_reflexia_check(client) -> None:
    # 🔎 Appel du endpoint Reflexia
    response = client.get("/reflexia/check")

    # ✅ Statut HTTP attendu
    assert response.status_code == 200, f"Erreur HTTP : {response.status_code} - {response.text}"

    # ✅ Structure de la réponse attendue
    data = response.json()
    assert "status" in data, "Clé 'status' manquante dans la réponse"
    assert "metrics" in data, "Clé 'metrics' manquante dans la réponse"
    assert isinstance(data["metrics"], dict), "'metrics' doit être un dictionnaire"
    assert "cpu" in data["metrics"], "Clé 'cpu' manquante dans les métriques"
    assert "ram" in data["metrics"], "Clé 'ram' manquante dans les métriques"
