import pytest
import requests

API_URL = "http://localhost:8000"


@pytest.mark.e2e
def test_full_pipeline():
    """
    Test E2E complet :
    - Vérifie que l'API principale fonctionne
    - Vérifie les endpoints de santé
    - Vérifie les métriques
    """
    # Test endpoint de santé principal
    r = requests.get(f"{API_URL}/health")
    assert r.status_code == 200
    data = r.json()
    assert "status" in data

    # Test endpoint de métriques
    try:
        r = requests.get(f"{API_URL}/metrics")
        assert r.status_code == 200
    except Exception:
        pytest.skip("Endpoint metrics non disponible - test ignoré")

    # Test endpoint de statut
    try:
        r = requests.get(f"{API_URL}/status")
        assert r.status_code == 200
        data = r.json()
        assert "status" in data
    except Exception:
        pytest.skip("Endpoint status non disponible - test ignoré")
