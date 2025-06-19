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