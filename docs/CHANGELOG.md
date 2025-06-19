# 📃 CHANGELOG — Arkalia-LUNA

> Historique des versions du système IA local **Arkalia-LUNA**  
> Maintenu par [Athalia 🌙](https://github.com/arkalia-luna-system)

---

## [v1.0.7] — 2025-06-19

✨ **Améliorations majeures de la documentation et navigation**

### ✅ Ajouts
- Nouvelle palette visuelle MkDocs : clair / sombre (theme toggle)
- Page `roadmap.md` intégrée à la navigation
- Page `CHANGELOG.md` intégrée à la documentation publique
- Diagramme d’architecture (`img/diagram_kernel.png`)
- Révision complète des fichiers `mkdocs.yml` & `index.md`

### ⚙️ Automatisation
- Déploiement GitHub Pages corrigé (`--force`)
- Génération automatique à chaque push `main`

### 🧪 Qualité & CI
- CI toujours active (`black`, `ruff`, `pytest`, `pre-commit`)
- Aucun warning détecté

📘 [Voir la documentation publique](https://arkalia-luna-system.github.io/arkalia-luna-pro/)

---

## [v1.0.6] — 2025-06-18

🔖 **Version STABLE PRO — Base officielle du noyau IA local modulaire**

### ✅ Fonctionnalités principales
- Modules IA actifs : `reflexia`, `nyxalia`, `helloria`
- API FastAPI avec endpoints (`/`, `/status`, `/module/trigger`)
- Intégration complète de Docker (`Dockerfile`, `docker-compose.yml`)
- Scripts IA : `ark-test`, `ark-docker-rebuild.sh`, `ark-clean-push`, `trigger_scan.sh`
- Intégration LLM local (Ollama) avec `mistral`, `llama2`, `tinyllama`
- Documentation auto-générée avec MkDocs (hébergée via GitHub Pages)

### 🧪 Tests & CI
- Couverture de test `pytest` : **100%**
- CI GitHub Actions complète : `black`, `ruff`, `pytest`, `gh-pages`
- Alias `.zshrc` actifs pour automatiser les tests et le push

### 🛠 Structure stabilisée
- Séparation propre : `arkalia-luna-core` (kernel) / `arkalia-luna-pro` (devstation)
- Nettoyage des artefacts (`__pycache__`, `.DS_Store`, etc.)
- `README.md` restructuré avec badges dynamiques

---

## [v0.3.0-docker-ok] — 2025-06-17

### ✅ Ajouts
- Dockerfile + docker-compose fonctionnels
- Uvicorn lancé en local via Docker
- Scripts créés : `ark-docker-rebuild.sh`, `ark-test`

---

## [v0.2.0] — 2025-06-16

### ✅ Mise en place de l’ossature pro
- Dossiers créés : `docs/`, `scripts/`, `tests/`, `.github/`
- Intégration : `pytest`, `black`, `ruff`, `pre-commit`, `bumpver`
- Début CI GitHub Actions

---

## [v0.1.1] — 2025-06-15

### ✅ Initialisation Devstation
- Nettoyage complet des anciens scripts & backups
- Mise en place du venv IA (`arkalia-luna-venv`)
- `pyproject.toml`, `bumpver`, `pre-commit` configurés

---

## [v0.1.0] — INIT (base reboot)

### ✅ Réinitialisation totale d’Arkalia
- Création du noyau `arkalia-luna-core` (structure stable, clean, sans dette technique)
- Nouveau dépôt propre `arkalia-luna-pro`
- Début du développement modulaire par session

---