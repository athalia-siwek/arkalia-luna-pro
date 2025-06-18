# 🧠 Arkalia-Luna Pro

**Devstation IA professionnelle pour Arkalia Luna**  
Modules IA — FastAPI, CI, bumpver, tests, pré-commit, et versioning automatisé.

---

## 🚀 Structure du projet

```
arkalia-luna-pro/
├── application/                 # Code applicatif central (FastAPI, endpoints, démarrage)
├── configuration/              # Fichiers de configuration système ou runtime
├── modules/                    # Modules IA actifs (ex: helloria, nyxalia...)
│   └── <nom_module>/
│       ├── __init__.py
│       ├── core.py
│       ├── config/
│       ├── logs/
│       ├── state/
│       ├── tests/
│       └── utils/
├── scripts/                    # Scripts de provisioning / outils de gestion
├── venv/                       # Environnement Python local (non versionné)
├── .pre-commit-config.yaml    # Lint automatique avec black + ruff
├── pyproject.toml             # Config Python + bumpver
├── version.toml               # Fichier de version unique (géré par bumpver)
└── README.md                  # Présentation pro du dépôt
```

---

## 🧩 Modules IA disponibles

- [`helloria`](modules/helloria/) — Interface de lancement cognitif IA
- [`nyxalia`](modules/nyxalia/) — [à compléter]

---

## 🛠️ Commandes principales

```bash
# Lancer l’API en mode développement
uvicorn application.main:app --reload

# Exécuter tous les tests
pytest

# Lint + auto-format du projet
black . && ruff check . --fix

# Mettre à jour la version (patch, minor, major)
ark-bump-patch
ark-bump-minor
ark-bump-major

# Lancer le bootstrap dans une nouvelle fenêtre Terminal
ark-bootstrap
```

---

## 🧪 Configuration des outils

- ✅ `black` — formatage de code
- ✅ `ruff` — linting performant
- ✅ `pytest` — tests unitaires
- ✅ `bumpver` — gestion version automatique
- ✅ `pre-commit` — hooks de vérification avant chaque commit

---

## 🧰 Dossiers sensibles exclus

Les dossiers suivants sont ignorés par git :

- `venv/` (environnement virtuel)
- `__pycache__/` et fichiers `.DS_Store`, `._*`
- Tout contenu temporaire ou généré automatiquement

---

## 🪪 Auteure

**Athalia 🌙**  
Développement IA propre, modulaire et ultra-pro.  
Architecture : Arkalia System.

