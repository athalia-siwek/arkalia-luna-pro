---

# ✅ `/docs/automation.md` — **Scripts & Automatisation**

```markdown
# 🤖 Scripts & Automatisation — Arkalia-LUNA

Le cœur d’Arkalia repose sur un ensemble de **scripts bash professionnels** et de **boucles intelligentes** permettant l'orchestration autonome du système IA.

---

## 🔁 Boucle Maîtresse : `arkalia_master_loop.py`

Cette boucle unique orchestre l’ensemble du système en :

- Chargeant les modules déclarés dans `config/`
- Réinjectant les états enregistrés depuis `state/`
- Analysant les logs pour décisions correctives
- Déléguant aux IA internes (Reflexia, ZeroIA) les actions adaptatives

---

## ⚙️ Scripts Principaux

| Script                         | Fonction                                                                 |
|-------------------------------|--------------------------------------------------------------------------|
| `ark-bootstrap`               | Initialise l’environnement IA local (`venv`, pre-commit, configs)        |
| `ark-test`                    | Lance tous les tests `pytest` + génère la couverture                    |
| `ark-docker-rebuild.sh`       | Rebuild du container Docker propre et relance FastAPI                   |
| `trigger_scan.sh`             | Déclenche une analyse réflexive manuelle via ReflexIA                   |
| `ark-clean-push`              | Lint (`ruff`), format (`black`) puis `git commit + push` automatisé     |

---

💡 *Ces scripts sont conçus pour être **déclenchés par l’IA elle-même** (ZeroIA, ReflexIA) selon les contextes systèmes détectés.*

---

## 🧠 Orchestration IA Dynamique

Reflexia ou ZeroIA peuvent :

- suspendre des modules
- forcer des tests
- relancer un container
- corriger automatiquement un état corrompu

---

🧭 Arkalia n'est pas seulement automatisée — elle est **auto-orchestrée**.