# 📁 tests/performance — Tests de performance

Ce dossier contient les **tests de performance** et benchmarks :
- Mesure du temps de réponse, du débit, de la consommation mémoire
- Stress tests, benchmarks, tests de scalabilité

## Conventions
- Fichiers : `test_*.py`
- Markers : `@pytest.mark.performance`
- Rapports générés dans `tests/reports/`

## Bonnes pratiques
- Isoler les tests de performance des autres types de tests
- Documenter les métriques mesurées
- Nettoyer les ressources après chaque test
