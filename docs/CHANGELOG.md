# 📃 CHANGELOG — Arkalia-LUNA

> Suivi des versions du système IA local **Arkalia-LUNA**  
> Maintenu par [Athalia 🌙](https://github.com/arkalia-luna-system)

---

## [v1.0.7] — 2025-06-19

✨ **Améliorations majeures de la documentation**

### ✅ Ajouts
- Activation du **mode clair/sombre** (theme toggle MkDocs)
- Nouvelle page `roadmap.md` dans la navigation
- `CHANGELOG.md` intégré à la documentation publique
- Diagramme d’architecture ajouté (`img/diagram_kernel.png`)
- Révision complète des fichiers `mkdocs.yml` et `index.md`

### ⚙️ Automatisation
- Déploiement GitHub Pages corrigé (`--force`)
- Déclenchement automatique à chaque push sur `main`

### 🧪 Qualité & CI
- CI GitHub Actions opérationnelle : `black`, `ruff`, `pytest`, `pre-commit`
- Aucun avertissement détecté

📘 [Documentation publique](https://arkalia-luna-system.github.io/arkalia-luna-pro/)

---

## [v1.0.6] — 2025-06-18

🔖 **Version STABLE PRO — Noyau IA local modulaire**

### ✅ Fonctionnalités principales
- Modules IA actifs : `reflexia`, `nyxalia`, `helloria`
- API FastAPI avec endpoints : `/`, `/status`, `/module/trigger`
- Intégration Docker complète : `Dockerfile`, `docker-compose.yml`
- Scripts IA : `ark-test`, `ark-docker-rebuild.sh`, `ark-clean-push`, `trigger_scan.sh`
- Support des modèles LLM locaux (`mistral`, `llama2`, `tinyllama`)
- Documentation auto-générée avec MkDocs (hébergement GitHub Pages)

### 🧪 Tests & CI
- Couverture de tests `pytest` : **100%**
- CI GitHub Actions complète : lint + tests + docs
- Aliases `.zshrc` actifs pour automatiser le workflow

### 🛠 Structure
- Séparation claire : `arkalia-luna-core` (kernel) vs `arkalia-luna-pro` (devstation)
- Nettoyage des artefacts (`__pycache__`, `.DS_Store`, etc.)
- `README.md` restructuré avec badges dynamiques

---

## [v0.3.0-docker-ok] — 2025-06-17

### ✅ Intégration Docker
- `Dockerfile` + `docker-compose.yml` fonctionnels
- Serveur Uvicorn lancé via Docker
- Scripts : `ark-docker-rebuild.sh`, `ark-test`

---

## [v0.2.0] — 2025-06-16

### ✅ Ossature Pro
- Dossiers créés : `docs/`, `scripts/`, `tests/`, `.github/`
- Intégration des outils : `pytest`, `black`, `ruff`, `pre-commit`, `bumpver`
- Début de la CI GitHub Actions

---

## [v0.1.1] — 2025-06-15

### ✅ Devstation initiale
- Nettoyage complet des anciens scripts et backups
- Initialisation de l’environnement `arkalia-luna-venv`
- Configuration : `pyproject.toml`, `bumpver`, `pre-commit`

---

## [v0.1.0] — INITIALISATION

### ✅ Reboot complet d’Arkalia
- Création du noyau `arkalia-luna-core` (clean, stable, sans dette technique)
- Nouveau dépôt `arkalia-luna-pro`
- Début du développement modulaire en sessions

## [v1.3.4-final] — 2025-06-20

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

## v2.1.0 — 21/06/2025

- ✅ Tests `assistantia` 100 %
- ✅ Nouvelle gestion des erreurs 400/422
- ✅ Amélioration couverture `ollama_connector`

### Ajouté
- 🔧 Module ReflexIA entièrement finalisé
- 💯 5 fichiers de test unitaire ReflexIA
- ✅ 100 % de couverture de test (reflexia)
- 📚 Documentation mise à jour : api.md, tests.md, modules.md

---