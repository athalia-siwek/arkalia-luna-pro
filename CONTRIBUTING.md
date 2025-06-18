# 🤝 CONTRIBUTING.md — Contribuer à Arkalia-LUNA

Bienvenue dans le dépôt `arkalia-luna-pro`. Ce guide décrit les bonnes pratiques à respecter pour contribuer efficacement et de manière professionnelle.

---

## 📁 Structure du projet

- Chaque module IA = un dossier dans `modules/<nom_du_module>/`
- Aucun code métier dans `arkalia_master_loop.py` → uniquement orchestration
- Fichiers séparés pour :
  - `core.py` → logique métier principale du module
  - `config/`, `logs/`, `state/` → données internes du module
  - `tests/` → tests unitaires avec `pytest`

---

## ⚙️ Setup local (devstation)

```bash
# 1. Cloner le dépôt
git clone https://github.com/athalia-siwek/arkalia-luna-pro.git
cd arkalia-luna-pro

# 2. Activer l’environnement Python
source /Volumes/T7/arkalia-luna-venv/bin/activate

# 3. Initialiser les hooks de pré-commit
pre-commit install

# 4. Vérifier la qualité du code
black .
ruff check .
pytest
```

---

## ✅ Conventions à respecter

- Formatage avec `black`
- Lint avec `ruff`
- Respect strict de la structure modulaire
- Aucun fichier `.DS_Store`, `__pycache__/`, ou fichier temporaire dans le dépôt
- Commits clairs avec emoji + résumé court (ex: `🧠 ajout ZeroIA loop adaptative`)

---

## 📦 Versionnage

Le système utilise `bumpver` pour incrémenter proprement les versions.

```bash
bumpver update
```

---

## 🧪 Tests

Les tests doivent être isolés dans `tests/` par module.

```bash
pytest tests/
```

---

## 📅 Mise à jour

Fichier généré le : `2025-06-18`  
Merci de contribuer à un projet IA propre et durable ✨

© Athalia — Arkalia System
