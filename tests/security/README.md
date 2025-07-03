# 📁 tests/security — Tests de sécurité

Ce dossier contient les **tests de sécurité** :
- Vérification des permissions, injections, gestion des secrets
- Tests d'attaque, fuzzing, validation des protections

## Conventions
- Fichiers : `test_*.py`
- Markers : `@pytest.mark.security`
- Ne jamais exposer de secrets réels dans les tests

## Bonnes pratiques
- Utiliser des données fictives ou mockées
- Documenter chaque cas de test
- Nettoyer les traces sensibles après chaque test

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
