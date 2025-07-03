# 📁 tests/fixtures — Fixtures & Helpers partagés

Ce dossier centralise toutes les **fixtures** et **helpers** réutilisables dans les tests.

- Ajoute ici toute fixture commune (connexion DB, données, mocks, etc.)
- Exemple d'import : `from tests.fixtures.fixtures import my_fixture`
- Toute modification doit être documentée ici ou dans le doc principal des tests.

## Bonnes pratiques
- Garder les fixtures génériques et découplées
- Documenter chaque nouvelle fixture
- Ne pas mettre de données sensibles

## Règles d'utilisation

- Place ici toutes les fixtures réutilisables (données, mocks, setup commun, helpers).
- Les fichiers doivent être importés via `from tests.fixtures...` dans les tests.
- Adapter `conftest.py` pour pointer ici si besoin de fixtures globales.
- Ne pas mettre de tests ici, uniquement des outils/supports pour les tests.

## Exemples de contenu
- `fixtures.py` : fixtures Pytest partagées (répertoires, configs, nettoyage...)
- `test_helpers.py` : fonctions utilitaires pour préparer l'environnement de test

---

**But :** éviter la duplication, garantir la cohérence et accélérer l'écriture de nouveaux tests.
