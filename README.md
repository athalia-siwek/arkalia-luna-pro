# 🌕 Arkalia-LUNA Pro — Devstation IA

**Dévstation professionnelle pour modules IA Arkalia Luna**  
→ FastAPI, CI, bumpver, modules propres, structure modulaire.

---

## 📁 Arborescence

```
arkalia-luna-pro/
├── application/           # Future app centralisée FastAPI
├── configuration/         # Configs globales système
├── modules/               # Modules IA : helloria/, nyxalia/, ...
├── scripts/               # Scripts CLI, bootstrap, tests
├── venv/                  # Virtualenv local (non versionné)
├── README.md              # Ce fichier !
├── pyproject.toml         # Config Python + tools (black, ruff, pytest)
├── version.toml           # bumpver versionning
└── .pre-commit-config.yaml # Hooks automatiques (black, ruff)
```

---

## 🚀 Démarrage rapide

```bash
# 1. Activer l’environnement
source ./venv/bin/activate

# 2. Installer les dépendances
pip install -r exigences.txt

# 3. Lancer l’API FastAPI
uvicorn application.main:app --reload

# 4. Lancer les tests
pytest
```

---

## 🧪 Modules IA intégrés

| Module     | Description courte                  | Version  |
|------------|-------------------------------------|----------|
| `helloria` | Module API IA base de test          | `v0.1.0` |
| `nyxalia`  | Module interface IA (à venir)       | `v0.1.0` |

---

## 🛠️ Outils intégrés

| Outil         | Rôle                            |
|---------------|---------------------------------|
| `black`       | Formatage automatique du code   |
| `ruff`        | Lint & fix style Python         |
| `pytest`      | Tests automatisés               |
| `bumpver`     | Gestion versions et tags Git    |
| `pre-commit`  | Lint/format auto avant commit   |
| `Makefile`    | Scriptable CLI (à compléter)    |

---

## 🔖 Versions et Tags

Version actuelle : `v0.1.0`  
Voir tous les tags : `git tag --list`

---

## 👩‍💻 Auteur

**Athalia Siwek** — *Système IA autonome Arkalia.*  
🌀 [GitHub](https://github.com/athalia-siwek)
