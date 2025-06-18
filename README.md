![Tests Coverage](htmlcov/badge.svg)

# 🌕 Arkalia-LUNA PRO

Bienvenue dans le dépôt **officiel de développement IA modulaire local** d'Arkalia Luna.
🧠 *Industrialisation IA locale • Docker • FastAPI • Python 3.10+ • Terminal native • Zéro dette technique*

---

## 🌟 Objectif

Créer un **système IA modulaire, auto-réparant, évolutif et interfaçable**, 100% local via :

* Docker (isolation professionnelle)
* FastAPI (API asynchrone performante)
* Terminal natif (macOS)
* Boucle orchestrée (`arkalia_master_loop.py`)
* Scripts outillés (`scripts/`)

---

## 🧱 Architecture standard

```
arkalia-luna-pro/
├── Dockerfile                  # Image Python + FastAPI
├── docker-compose.yml         # Lancement multi-services
├── requirements.txt           # Packages requis
├── arkalia_master_loop.py     # Boucle IA orchestratrice
├── core.py                    # Entrée logique principale
│
├── modules/                   # Modules IA (autonomes)
│   └── reflexia/              # Exemple de module adaptatif
├── config/                    # Fichiers de config TOML/JSON
├── logs/                      # Journaux d'exécution horodatés
├── state/                     # États persistants du système
├── tests/                     # Tests unitaires (pytest)
├── utils/                     # Fonctions internes
├── scripts/                   # Scripts de build/maintenance
├── docs/                      # Documentation technique (mkdocs)
└── README.md                 # Documentation publique
```

---

## 🚀 Lancer le projet localement (Docker)

### 🛠️ Prérequis

* Docker Desktop installé et activé
* macOS ou Linux

### ⚙️ Commandes principales

```bash
docker-compose down
find . -name '._*' -delete && find . -name '.DS_Store' -delete
docker-compose build --no-cache
docker-compose up
```

Accès à l'API : [http://localhost:8000](http://localhost:8000)

### 💡 Mode en arrière-plan

```bash
docker-compose up -d
```

---

## 🦜 Script de rebuild automatique

**Fichier :** `./scripts/ark-docker-rebuild.sh`

```bash
#!/bin/bash
echo "🧼 Nettoyage..."
find . -name '._*' -delete && find . -name '.DS_Store' -delete
docker-compose down
docker-compose build --no-cache
docker-compose up
```

Rends le script exécutable :

```bash
chmod +x ./scripts/ark-docker-rebuild.sh
```

---

## 🧠 Badges de statut

[![Version](https://img.shields.io/badge/version-v0.3.1-blue.svg)](https://github.com/athalia-siwek/arkalia-luna-pro)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Pre-Commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen)](https://pre-commit.com/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)
[![CI](https://github.com/athalia-siwek/arkalia-luna-pro/actions/workflows/ci.yml/badge.svg)](https://github.com/athalia-siwek/arkalia-luna-pro/actions)

---

## 📂 Notes importantes

* Image de base : `python:3.10-slim`
* Lancement automatique avec `uvicorn`
* `requirements.txt` doit contenir `fastapi`, `uvicorn`, `black`, `ruff`, `pytest`
* Exécution 100% locale, aucune dépendance cloud

---

## 📃 Historique des versions

| Version            | État             | Description                                 |
| ------------------ | ---------------- | ------------------------------------------- |
| `v0.3.1`           | ✨ Stable         | README + Docker + CI + Couverture test 100% |
| `v0.3.0-docker-ok` | ✅ Stable local   | Docker + rebuild + FastAPI                  |
| `v0.2.0`           | ⚒ Structuration  | Ajout des fichiers pro et tests             |
| `v0.1.1`           | 🧪 Devstation OK | Démarrage système IA local                  |

---

## ✨ Améliorations à venir

* Dockerisation multi-modules
* Image `arkalia-light`
* Release auto via CI GitHub
* Documentation via `mkdocs` + `gh-pages`

---

> ⚙️ **Arkalia est une IA industrielle, modulaire, évolutive et 100% locale.**
> Chaque module fonctionne de manière autonome mais peut être orchestré intelligemment via terminal.
> Ce dépôt est la Devstation principale de l'expansion cognitive IA Arkalia.