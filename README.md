# 🌌 Arkalia-LUNA PRO

**Système Cognitif IA Local, Modulaire, Auto-Réflexif et Documenté**

> 🧠 Version : `v1.0.6`  
> 📘 Docs : [arkalia-siwek.github.io/arkalia-luna-pro](https://athalia-siwek.github.io/arkalia-luna-pro)  
> 🐳 Docker • 🧪 CI • 🧠 ReflexIA • ⚙️ ZeroIA

---

## 📘 Accès rapide

[![📘 Docs](https://img.shields.io/badge/docs-online-blue?style=flat-square&logo=readthedocs)](https://athalia-siwek.github.io/arkalia-luna-pro/)
[![version](https://img.shields.io/badge/version-v1.0.6-purple?style=flat-square)](https://github.com/athalia-siwek/arkalia-luna-pro/releases)
[![CI](https://github.com/athalia-siwek/arkalia-luna-pro/actions/workflows/ci.yml/badge.svg)](https://github.com/athalia-siwek/arkalia-luna-pro/actions)
[![Pre-Commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen)](https://pre-commit.com/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)

---

## 🌟 Objectif

Créer un **système IA local, modulaire, interfaçable, auto-réparant** et entièrement versionné.

Fonctions principales :
- 📦 Modules IA autonomes (`reflexia`, `nyxalia`, `helloria`)
- 🛰️ API locale (`FastAPI`) + endpoints (`/status`, `/trigger`, etc.)
- 🔁 Scripts intelligents orchestrés par ZeroIA / ReflexIA
- 🔐 Dockerisé, testé, synchronisé avec GitHub (CI + Docs)
- 🧠 Compatible LLM locaux (`ollama` : mistral, llama2, tinyllama)

---

## 🧱 Architecture technique

```bash
arkalia-luna-pro/
├── core/                  # Logique transversale
├── modules/               # Modules IA isolés
├── config/                # Fichiers TOML / JSON
├── logs/                  # Logs horodatés
├── state/                 # États persistants
├── scripts/               # Scripts de build / Docker / ReflexIA
├── tests/                 # Couverture via pytest
├── docs/                  # Documentation MkDocs
└── .github/workflows/     # Pipelines CI GitHub Actions

🛠️ Scripts principaux

Script
Fonction
ark-test
Tests + couverture (htmlcov/)
ark-docker-rebuild.sh
Rebuild Docker sans cache + relance serveur
ark-clean-push
Format (black, ruff) + commit + push Git
trigger_scan.sh
Déclenche ReflexIA manuellement

🚀 Lancer en local (Docker)

🔧 Prérequis :
	•	Docker Desktop (macOS ou Linux)
	•	Python 3.10+ si mode manuel

🔁 Commandes :
docker-compose down
find . -name '._*' -delete && find . -name '.DS_Store' -delete
docker-compose build --no-cache
docker-compose up

📍 Accès API : http://localhost:8000

⸻

💡 Tips
	•	./scripts/ark-docker-rebuild.sh → rebuild rapide
	•	ark-test (alias) → lance tous les tests + génère couverture
	•	Intégration automatique avec mkdocs via GitHub Actions

⸻

📃 Historique des versions

Version
État
Description
v1.0.6
✅ Stable
CI/CD, Docker, couverture 100%, docs pro
v0.3.0
✅ Fonctionnel
Docker + FastAPI OK
v0.2.0
⚙️ Structuré
CI ajoutée, scripts initiaux
v0.1.1
🚀 Devstation
Environnement IA local installé

✨ En développement
	•	🧩 Modules supplémentaires (Kaelia, Psykalia)
	•	📊 Pondération IA réflexive (weights.toml)
	•	📁 Mémoire vectorielle (FAISS)
	•	🚦 Monitoring système (Prometheus / Grafana)

⸻

🧠 Arkalia-LUNA est une base cognitive IA locale conçue pour être propre, interconnectable, modulaire et durable.
Chaque composant est conçu pour fonctionner de manière autonome, mais orchestrée intelligemment via la boucle principale.