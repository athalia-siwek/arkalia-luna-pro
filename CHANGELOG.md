# 📋 CHANGELOG.md — Historique des versions Arkalia-LUNA

Ce fichier retrace les changements apportés à chaque version publique d'Arkalia-LUNA.

## [helloria-v1.0.0] — 2025-06-19

### ✅ Ajouts
- Endpoint `GET /` pour ping racine (`core.py`)
- Endpoint `GET /status` pour état opérationnel (`core.py`)
- Gestion d'état via `HelloriaStateManager` (`state.py`)
- Ajout de `main.py` pour exécution directe via Uvicorn
- Test unitaire minimal (`test_helloria.py`)

### ♻️ Refactoring
- Nettoyage et normalisation via `black` et `ruff`

### 📄 Documentation
- `README.md` : objectif, routes, exemple de requête, lien vers MkDocs

🔁 **Couverture test :** 100 % sur `test_helloria.py`  
🔗 **Documentation :** [https://athalia-siwek.github.io/arkalia-luna-pro/modules](https://athalia-siwek.github.io/arkalia-luna-pro/modules)

---

## [0.1.2] - 2025-06-18
### Ajouté
- ENHANCEMENTS.md avec roadmap d'amélioration IA
- CONTRIBUTING.md avec règles de contribution
- Badges pro dans README

## [0.1.1] - 2025-06-17
### Initialisation
- Dépôt GitHub mis en ligne
- README.md structuré
- Pre-commit activé (`black`, `ruff`)

## [v1.3.1] — 2025-06-20

### ✅ Tests
- 20 tests validés avec succès
- Intégration AssistantIA, ReflexIA, Nyxalia, Helloria OK

### 📊 Couverture
- Couverture > 85 %

### 🚀 CI/CD
- CI/CD et Docker validés

## [v1.3.2] - 2025-06-19

### 🔧 Améliorations Dev
- Ajout des badges `Black` + `Ruff` dans le README
- Correction `.pre-commit-config.yaml` (exclusions propres)
- CI/CD validée avec tous les tests unitaires
- Linting propre (black, ruff) passé à 100%

### ✅ État du système
- Couverture globale : **86 %**
- Tests : **8/8 passés**
- CI GitHub : **verte**
- Docker : **ok**

## [v1.2.2] — 2025-06-20

### 🚀 Nouveautés
- Création du module `assistantia` avec endpoint `/chat` dynamique
- Intégration locale d'Ollama (`mistral`), via `query_ollama()`
- Ajout du fichier `ollama_connector.py` dans `utils/` (testé à 91%)
- Comportement IA sécurisé : prompt vide, modèles invalides → contrôlés

### ✅ Tests
- 35 tests unitaires passés (`pytest`)
- 92 % de couverture globale (`htmlcov/index.html`)
- Ajout de cas limites (`422`, ValueError, timeouts)

### 🛠️ CI / Docker
- CI GitHub Actions validée (lint, tests, doc)
- Docker stable (`ark-docker`, `assistantia` intégré)

### 📘 Documentation
- Site MkDocs à jour (sitemap, modules, automation)
- Bloc `/chat` ajouté dans `docs/api.md` avec erreurs gérées
- Signature visuelle maintenue (`extra.css`, `.arkalia-box`)

### 🏁 État
- Version stable IA contextuelle validée
- Prête pour évolution vers Arkalia LUNA Nexus

---

## 🏷️ Version `v1.3.4-final` — 20 juin 2025

### ✅ Stabilisation totale du système IA

- 🎯 Objectif atteint : IA locale modulaire, dockerisée, testée, publiée.
- 🧠 Modules actifs :
  - `reflexia/` (analyse cognitive adaptative)
  - `nyxalia/` (interface mobile/API)
  - `helloria/` (FastAPI & serveurs IA)
  - `assistantia/` (Ollama connector IA locale)

### 🧪 Tests & couverture

- ✔️ `35` tests passés (`pytest`)
- 📈 Couverture : `90 %`
- 📂 Rapport : `htmlcov/index.html`

### 📘 Documentation publique

- 🌍 Publication MkDocs : [https://arkalia-luna-system.github.io/arkalia-luna-pro/](https://arkalia-luna-system.github.io/arkalia-luna-pro/)
- 🗺️ Sitemap dynamique généré : [`/sitemap.xml`](https://arkalia-luna-system.github.io/arkalia-luna-pro/sitemap.xml)
- 📦 Dossiers nettoyés : suppression des doublons `docs/docs/*`, renommages, correction `nav` dans `mkdocs.yml`

### ⚙️ Système & Devstation

- 🐳 Docker opérationnel (`docker-compose`)
- 🧪 `ark-test`, `ark-docs`, `ark-docker`, `ark-backup` activés
- 🎛️ CI GitHub : lint (`black`, `ruff`) + tests + pages
- 🪪 Fichier `.pre-commit-config.yaml` actif

### 🧰 Scripts & bonus

- ✅ Script `sitemap_generator.py` exécuté automatiquement après `mkdocs build` via plugin `simple-hooks`
- ✅ Test unitaire `test_sitemap.py` intégré (`scripts/`)
- ✅ Page `ci-cd.md` enrichie (bonus UX, collapsibles, état réel CI)
- ✅ Pages stylisées (Mermaid, blocs contextuels, tableaux dynamiques)

---

📦 **Version gelée, stable et publiable**.

➡️ Prochaine version `v1.3.5` : préparation phase Nexus (ZéroIA + Psykalia + surcouche cognitive Arkalia).

---
