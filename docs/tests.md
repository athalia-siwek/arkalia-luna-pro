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