# 🌕 Arkalia-LUNA PRO

Bienvenue dans le dépôt **officiel de développement modulaire IA local** d'Arkalia Luna.

---

## 🎯 Objectif

Développer un **système IA modulaire, évolutif, auto-réparant, zéro dette technique**, orchestré en local via Docker, FastAPI et Terminal sous macOS.

Chaque module est :
- Autonome
- Testable indépendamment
- Interfaçable dans une boucle centrale (`arkalia_master_loop.py`)

---

## 🧱 Architecture standard

```
arkalia-luna-pro/
├── Dockerfile                 # Configuration Docker
├── docker-compose.yml        # Lancement multi-service
├── requirements.txt          # Dépendances Python
├── arkalia_master_loop.py    # Boucle orchestratrice des modules
├── core.py                   # Entrée logique principale
├── modules/                  # Modules IA
│   └── reflexia/             # Exemple : module adaptatif
├── config/                   # Configs TOML / JSON
├── logs/                     # Logs horodatés
├── state/                    # États persistants
├── tests/                    # Tests unitaires
├── utils/                    # Fonctions internes
└── README.md                 # Documentation publique
```

---

## 🚀 Lancer le projet localement (Docker)

### 📦 Prérequis

- Docker installé : [https://www.docker.com/](https://www.docker.com/)
- Docker Desktop activé (macOS)

---

### 🛠️ Commandes de build & exécution

```bash
docker-compose down
find . -name '._*' -delete && find . -name '.DS_Store' -delete
docker-compose build --no-cache
docker-compose up
```

📍 Accès local : [http://localhost:8000](http://localhost:8000)

---

### 🧪 Lancer en arrière-plan (mode daemon)

```bash
docker-compose up -d
```

---

## 📌 Notes importantes

- Le Dockerfile utilise l’image : `python:3.10-slim`
- Le serveur FastAPI démarre automatiquement avec `uvicorn`
- `requirements.txt` doit contenir toutes les dépendances (ex : `fastapi`, `uvicorn`, etc.)

---

## 🧠 Badges de statut

[![Version](https://img.shields.io/badge/version-0.3.0--docker--ok-blue.svg)](https://github.com/athalia-siwek/arkalia-luna-pro)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)  
[![Pre-Commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen)](https://pre-commit.com/)  
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

---

## ✨ Améliorations en cours

➡ Consulte [`ENHANCEMENTS.md`](./ENHANCEMENTS.md)  
➡ Documentation technique dans [`docs/index.md`](./docs/index.md)

---

## 🗃️ Historique des Versions

| Version             | État                | Description                                      |
|---------------------|---------------------|--------------------------------------------------|
| `v0.3.0-docker-ok`  | ✅ Stable & local    | Dockerfile + Compose opérationnels avec FastAPI |
| `v0.2.0`            | 🛠 Structuration Git | Ajout des fichiers pro (`README`, `tests`, etc.)|
| `v0.1.1`            | 🧪 Devstation OK     | Lancement stable de la devstation IA            |

---

> **Système IA modulaire local** — FastAPI • Python • Terminal • 🛡️ Zéro dette technique