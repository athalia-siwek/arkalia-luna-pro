# 🧪 Architecture des Tests

## Objectifs
- Vérifier le bon fonctionnement de chaque module IA
- Garantir stabilité, compatibilité et couverture

## Répartition
- `unit/` : logique interne
- `integration/` : endpoints + coordination
- `core/` : lancement, orchestration
- `scripts/` : outils internes (sitemap, automation…)

## Outils & alias
- `ark-test`, `ark-test-modules`, `pytest-cov`, `pytest -k`

## Bonnes pratiques
- Isoler chaque test
- Couvrir erreurs connues
- Éviter dépendance entre tests