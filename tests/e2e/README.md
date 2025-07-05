# Tests End-to-End (E2E)

Ce dossier contient les tests bout-en-bout simulant des scénarios réels d’utilisation.

- **But** : Valider le fonctionnement global de la plateforme (API, UI, flux utilisateur).
- **Organisation** : Un fichier par scénario E2E.
- **Exécution** : `pytest tests/e2e/`

## Règles
- Utiliser des données de test isolées
- Nettoyer l'état après chaque test
- Marquer les tests E2E avec `@pytest.mark.e2e`

## Exemple d'exécution
```bash
pytest tests/e2e/
```
