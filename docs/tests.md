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

Pour plus d'informations sur les modèles testés, consultez [Ollama](ollama.md).

## Module assistantia — Couverture 100 %

- 🔁 Tests unitaires avec FastAPI `TestClient`
- 🧪 Vérification :
  - `/chat` (mocké et réel)
  - gestion erreurs 422 / 400
  - réponse longue (stress test)
- 📦 Dépendance mockée : `get_query_ollama`

### 🤖 Module ReflexIA

| Fichier de test | Cible | Couverture |
|------------------|--------|------------|
| `test_reflexia.py` | Fonction globale `launch_reflexia_check` | ✅ |
| `test_reflexia_core.py` | Fonctions internes de `core.py` | ✅ |
| `test_reflexia_decision.py` | `monitor_status` (analyse cognitive) | ✅ |
| `test_reflexia_metrics.py` | `read_metrics()` (CPU/RAM simulées) | ✅ |
| `test_reflexia_snapshot.py` | `save_snapshot()` JSON réflexif | ✅ |

Tous les tests passent avec succès ✅ (CI : 58/58), et le module ReflexIA atteint 100 % de couverture.

## Résultats de la session de test v2.1.2 — 23 juin 2025

### État des tests
- **Tests Pytest** : ✅ 68/68 passés en 41.95s
- **Couverture globale** : 🔍 94% HTML, 89% moyenne code
- **Reflexia core.py** : ✅ 93% couvert (2 succursales logiques testées)
- **assistantia modules** : ✅ 91–93% pour core et utils, stable
- **Fichiers ignorés** : 📁 8 fichiers entièrement couverts (pas listés)
- **CI/CD locale** : 🟢 Tests, lint, pre-commit, tout passe sans erreur

### Couverture détaillée (top modules)
- **modules/reflexia/core.py** : ✅ 93%
- **modules/assistantia/utils/ollama_connector.py** : ✅ 91%
- **modules/assistantia/core.py** : ✅ 93%
- **modules/helloria/core.py** : ✅ 83%
- **arkalia/hooks.py** : ✅ 83%

### Prochaines pistes (optionnel pour la perfection totale)
- 🔬 Monter core.py et helloria/core.py à 100% → quelques branches conditionnelles manquantes (if/else)
- 🔁 Tester reflexia_loop() en mode timeout (boucle longue)
- 📁 Archiver cette version : v2.1.2-tests-ok-full
- 📝 Documenter cette étape dans CHANGELOG.md + badge coverage (si pas encore fait)

![Couverture](https://img.shields.io/badge/couverture-94%25-brightgreen)🔧 Patch test
