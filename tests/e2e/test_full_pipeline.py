import pytest
import requests

API_URL = "http://localhost:8000/decision"


@pytest.mark.e2e
def test_full_pipeline():
    """
    Test E2E complet :
    - Envoie une requête à l'API /decision
    - Vérifie la réponse
    - Vérifie la persistance (état ZeroIA, snapshot, etc.)
    """
    input_data = {
        "context": "test pipeline e2e"
        # Ajouter les champs nécessaires selon le schéma de l'API
    }
    r = requests.post(API_URL, json=input_data)
    assert r.status_code == 200
    data = r.json()
    assert "decision" in data
    assert "confidence" in data
    # TODO : Vérifier la persistance (fichier, DB, etc.)
    # Exemple :
    # with open("state/zeroia_state.toml") as f:
    #     assert "last_decision" in f.read()
