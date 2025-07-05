# Tests de Performance

Ce dossier contient les tests de performance et benchmarks.

- **But** : Mesurer la latence, le débit, la robustesse sous charge.
- **Organisation** : Un fichier par type de test (API, modules, global).
- **Exécution** : `pytest tests/performance/`

## Conventions
- Fichiers : `test_*.py`
- Markers : `@pytest.mark.performance`
