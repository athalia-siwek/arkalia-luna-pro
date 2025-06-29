# 🔒 Tests de Sécurité — Arkalia-LUNA

## Objectif
Valider la robustesse du système face aux attaques, injections, corruptions et accès non autorisés.

## Structure
- `assistantia/` : sécurité AssistantIA
- `zeroia/` : sécurité ZeroIA
- `general/` : sécurité générale (cross-modules)

## Exécution rapide
```bash
pytest tests/security/assistantia/
pytest tests/security/zeroia/
pytest tests/security/general/
```

## Marqueurs
- `@pytest.mark.security` : tests de sécurité
- `@pytest.mark.slow` : tests longs

## Bonnes pratiques
- Couvrir tous les points d'entrée critiques
- Ajouter un test pour chaque faille ou bug découvert
- Utiliser des mocks pour simuler les attaques
- Documenter chaque scénario d'attaque

## Exemple de test
```python
import pytest

@pytest.mark.security
def test_poisoning_attack():
    # ... scénario d'attaque ...
    assert True  # à remplacer par la vraie vérification
```

## Conseil
Lance les tests de sécurité régulièrement et après chaque modification sensible. 