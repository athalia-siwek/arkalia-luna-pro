# 📁 tests/integration — Tests d'intégration

Ce dossier regroupe les **tests d'intégration** :
- Vérifient l'interaction entre plusieurs modules, API, ou services
- Peuvent nécessiter des dépendances externes (DB, API, Docker)

## Conventions
- Fichiers : `test_*.py`
- Markers : `@pytest.mark.integration`
- Utiliser des données de test isolées

## Bonnes pratiques
- Nettoyer l'environnement après chaque test
- Documenter les dépendances nécessaires
- Utiliser les fixtures partagées
