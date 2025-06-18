# 📃 CHANGELOG — Arkalia-LUNA

Historique complet des versions et évolutions majeures du système IA local **Arkalia-LUNA**.

---

## [v1.0.6] — 2025-06-18

🔖 **Version STABLE PRO — Base officielle du noyau IA modulaire local**

### ✅ Ajouts
- Modules IA actifs : `Reflexia`, `Nyxalia`, `Helloria`
- API FastAPI opérationnelle (`/`, `/status`, `/module/trigger`)
- Intégration complète de Docker (`Dockerfile`, `docker-compose`)
- Scripts IA pro : `ark-test`, `ark-docker-rebuild.sh`, `ark-clean-push`, `trigger_scan.sh`
- Intégration Ollama : modèles locaux (`mistral`, `llama2`, `tinyllama`)
- Documentation publique auto-générée avec `MkDocs`

### 🧪 Tests & CI
- Couverture `pytest` à 100 %
- CI GitHub Actions : `black`, `ruff`, `pytest`, `gh-pages`

### 🛠 Structure stabilisée
- Séparation claire entre `arkalia-luna-core` (kernel) et `arkalia-luna-pro` (devstation)
- `.zshrc` pro avec alias (`ark-test`, `ark-backup`, etc.)
- `README.md` restructuré + badges actifs

---

## [v0.3.0-docker-ok] — 2025-06-17

- Dockerfile fonctionnel avec FastAPI
- `docker-compose` opérationnel
- Déploiement en local avec `uvicorn`
- Premiers scripts : `ark-docker-rebuild.sh`, `ark-test`

---

## [v0.2.0] — 2025-06-16

- Ajout des dossiers pro : `docs/`, `scripts/`, `tests/`, `.github/workflows/`
- Intégration des outils : `pytest`, `black`, `ruff`, `pre-commit`
- Début de CI/CD GitHub

---

## [v0.1.1] — 2025-06-15

- Nettoyage complet des anciens fichiers
- Initialisation de la Devstation IA (`arkalia-luna-pro`)
- Configuration du venv, `pyproject.toml`, `bumpver`, hooks Git

---

## [v0.1.0] — INIT

- Réinitialisation d'Arkalia-LUNA depuis `arkalia-system` hérité
- Création du noyau `arkalia-luna-core` (figé, propre, sans dette technique)

## 🚀 Nouveautés v1.0.7

- 🧭 Nouvelle navigation MkDocs avec palette claire/sombre
- 📘 `CHANGELOG.md` intégré à la documentation publique
- 🗺 Diagramme visuel `img/diagram_kernel.png`
- 📂 Page `roadmap.md` ajoutée, avec jalons de développement
- ✅ Déploiement GitHub Pages corrigé (`--force`)
- 🧪 Tests & CI toujours actifs (`black`, `ruff`, `pytest`, `pre-commit`)
- 📦 Site de documentation synchronisé avec GitHub Pages

🔗 [Documentation publique Arkalia-LUNA](https://athalia-siwek.github.io/arkalia-luna-pro/)