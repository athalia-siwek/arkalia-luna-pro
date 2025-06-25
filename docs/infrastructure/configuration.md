# ⚙️ Configuration — Arkalia-LUNA

> Guide complet pour configurer correctement le système IA **Arkalia-LUNA**, en garantissant stabilité, performance et sécurité.

---

## 🔑 Paramètres Essentiels

- **Fichier principal** : `config/system/config.yaml`
  Contient :
  - chemins d’accès (logs, state, modules…)
  - clés API locales (si activées)
  - poids IA initiaux (`weights.toml`)

- **Variables d’environnement** :
  - `ARKALIA_ENV=dev` ou `prod`
  - `OLLAMA_HOST=http://localhost:11434`
  - `ARKALIA_SECRET_KEY=...` *(à définir)*

Définir dans `.env`, `.zshrc` ou `docker-compose.yml` selon le mode utilisé.

---

## ⚙️ Configuration Avancée

### 🔧 Modules personnalisés

Chaque module IA dispose de son propre fichier :

modules/<nom_module>/config/config.toml

- Tu peux y adapter le comportement (seuils, poids, déclencheurs, etc.)

### 🚀 Optimisations recommandées

- **Docker** : Limite CPU/mémoire pour chaque container
- **FastAPI** : Config `workers`, `keep-alive` dans `uvicorn`
- **Logs** : Rotation automatique via `logging.conf` si besoin

---

## 🧾 Bonnes pratiques

| Sécurité | Recommandation |
|---------|-----------------|
| 🔒 | Ne jamais committer les clés dans Git |
| 🛡️ | Sauvegarde automatique régulière (`ark-backup`) |
| 🔍 | Vérifier les accès avec `ZeroIA` ou `Reflexia` |
| 🧩 | Isoler les `venv`, les fichiers `.env` et `/state/` |

---

## ✅ Checklist post-installation

- [x] `config.yaml` bien rempli
- [x] variables d’environnement définies
- [x] modules IA accessibles
- [x] Docker + FastAPI fonctionnels
- [x] scripts `arkalia-*.sh` opérationnels

---

💡 Une **configuration propre**, c’est la garantie d’un système IA **autonome, sécurisé et sans dette technique**.
