# 📁 tests/e2e — Tests End-to-End (E2E)

Ce dossier contient les **tests bout-en-bout** (E2E) :
- Scénarios complets API + DB + mémoire
- Validation du parcours utilisateur ou de l'intégration système

## Règles
- Utiliser des données de test isolées
- Nettoyer l'état après chaque test
- Marquer les tests E2E avec `@pytest.mark.e2e`

## Exemple d'exécution
```bash
pytest tests/e2e/
```
