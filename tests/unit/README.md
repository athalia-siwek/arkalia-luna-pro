# 📁 tests/unit — Tests unitaires

Ce dossier contient les **tests unitaires** d’Arkalia-LUNA Pro.

- Cible : modules isolés, logique métier, fonctions pures
- Objectif : garantir la robustesse de chaque composant indépendamment

## Conventions
- Fichiers : `test_*.py`
- Markers : `@pytest.mark.unit`
- Pas de dépendance réseau ou base de données
- Utiliser les fixtures de `tests/fixtures/` si besoin

## Bonnes pratiques
- Un test = un comportement attendu
- Garder les tests rapides et indépendants
- Documenter les cas limites
