# Tests de Sécurité

Ce dossier contient les tests de sécurité (injection, XSS, fuzzing, etc).

- **But** : Détecter les vulnérabilités et valider les protections.
- **Organisation** : Un fichier par type de test de sécurité.
- **Exécution** : `pytest tests/security/`

## Conventions
- Fichiers : `test_*.py`
- Markers : `@pytest.mark.security`
