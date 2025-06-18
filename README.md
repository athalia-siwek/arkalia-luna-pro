# 🌕 Arkalia-LUNA PRO

Bienvenue dans le dépôt **officiel de développement IA modulaire local** d'Arkalia Luna.  
> 🧠 Industrialisation IA locale • Docker • FastAPI • Python 3.10+ • Terminal native • Zéro dette technique

---

## 🎯 Objectif

Créer un **système IA modulaire, auto-réparant, évolutif et interfaçable**, fonctionnant à 100% en local via :

- Docker
- FastAPI (API asynchrone)
- Boucle terminal orchestrée (`arkalia_master_loop.py`)
- Scripts pro & structure modulaire professionnelle (`modules/<nom_module>/`)

---

## 🧱 Architecture standard

```
arkalia-luna-pro/
├── Dockerfile                 # Configuration d'image Python 3.10 + FastAPI
├── docker-compose.yml        # Lancement isolé (mode développeur)
├── requirements.txt          # Dépendances Python
├── arkalia_master_loop.py    # Boucle IA principale orchestrée
├── core.py                   # Entrée logique système
│
├── modules/                  # Modules IA autonomes
│   └── reflexia/             # Exemple : module adaptatif réflexif
│
├── config/                   # Fichiers TOML/JSON de configuration
├── logs/                     # Journaux d'exécution module par module
├── state/                    # États persistants internes
├── tests/                    # Tests unitaires
├── utils/                    # Fonctions internes réutilisables
├── scripts/                  # Scripts outils (rebuild, export, backup, etc.)
└── README.md                 # Documentation publique
```

---

## 🚀 Lancer en local avec Docker

### 🧰 Prérequis

- [Docker](https://www.docker.com/) installé
- Docker Desktop activé (si macOS)

### ⚙️ Commandes de lancement

```bash
docker-compose down
find . -name '._*' -delete && find . -name '.DS_Store' -delete
docker-compose build --no-cache
docker-compose up
```

📍 Accès local après lancement : [http://localhost:8000](http://localhost:8000)

---

### 🧪 Mode production local (en arrière-plan)

```bash
docker-compose up -d
```

---

## 🧼 Script automatique de rebuild

Ajouté dans `./scripts/ark-docker-rebuild.sh` :

```bash
#!/bin/bash
echo "🧼 Nettoyage..."
find . -name '._*' -delete && find . -name '.DS_Store' -delete
docker-compose down
docker-compose build --no-cache
docker-compose up
```

> Rends-le exécutable :
```bash
chmod +x ./scripts/ark-docker-rebuild.sh
```

---

## 🧠 Badges de statut

[![Version](https://img.shields.io/badge/version-v0.3.0--docker--ok-blue.svg)](https://github.com/athalia-siwek/arkalia-luna-pro)  
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)  
[![Pre-Commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen)](https://pre-commit.com/)  
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)  
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)

---

## 📌 Notes importantes

- Image Docker : `python:3.10-slim`
- Lancement auto avec `uvicorn`
- Le fichier `requirements.txt` doit contenir :  
  `fastapi`, `uvicorn`, `black`, `ruff`, `pytest`, etc.
- Fonctionne hors cloud, sans dépendance externe

---

## 🗃️ Historique des Versions

| Version             | État                | Description                                      |
|---------------------|---------------------|--------------------------------------------------|
| `v0.3.0-docker-ok`  | ✅ Stable & local    | Dockerfile + Compose opérationnels avec FastAPI |
| `v0.2.0`            | 🛠 Structuration Git | Ajout des fichiers pro (`README`, `tests`, etc.)|
| `v0.1.1`            | 🧪 Devstation OK     | Lancement stable de la devstation IA            |

📍 **Checkpoint** : `v0.3.0-docker-ok`  
📂 **Contexte** : Docker fonctionnel, FastAPI auto-déployé, script rebuild intégré  
🔒 **Statut** : **STABLE LOCAL DEV OK**

---

## ✨ Améliorations en cours

➡ Voir [`ENHANCEMENTS.md`](./ENHANCEMENTS.md)  
➡ Documentation technique : [`docs/index.md`](./docs/index.md)

---

## 💡 À venir (prévu pour v0.4.0)

- Dockerisation multi-modules (multi-services)
- Ajout d’une image Docker `arkalia-light`
- Setup CI GitHub Actions pour test auto
- Option `docker-compose.override.yml` pour profil production

---

> ⚙️ Arkalia est une IA **industrielle, modulaire, évolutive, terminal-native**. Chaque module agit indépendamment mais peut être orchestré dans une boucle intelligente locale.  
> Ce dépôt est la Devstation principale pour l’expansion des modules IA cognitifs.