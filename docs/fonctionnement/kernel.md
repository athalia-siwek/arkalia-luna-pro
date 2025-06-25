# 🧬 Structure du Noyau — Arkalia-LUNA

> Le noyau Arkalia est fondé sur une **architecture IA industrielle modulaire**, garantissant une séparation stricte entre exécution, logique métier et développement.

---

## ⚙️ 1️⃣ `/arkalia-luna-core/` — Noyau IA Pur

> Partie figée, **stable** et **non évolutive**. Elle constitue le **socle de sécurité du système**.

| Élément                        | Description                                                   |
|-------------------------------|---------------------------------------------------------------|
| 📁 Contenu                    | Fichiers de configuration système uniquement (`.toml`, `.sh`) |
| 🚫 Aucune logique métier      | Pas de modules IA ni de code d’application                   |
| 🔒 Interdiction de dette tech | Cette zone doit rester immuable                              |
| 🚀 Script de boot             | `arkalia_devstation_bootstrap.sh`                            |
| 🧱 Rôle principal              | Isoler la Devstation, sécuriser l’environnement système      |

---

## 🧠 2️⃣ `/arkalia-luna-pro/` — Devstation IA Modulaire

> Espace de **développement local**, dockerisé, versionné, avec CI/CD automatique.

| Composant         | Description                                             |
|------------------|---------------------------------------------------------|
| 🧩 Modules IA     | `reflexia`, `nyxalia`, `helloria`, `assistantia`, etc. |
| 🧪 Tests          | `pytest`, `pytest-cov` (couverture 85% mini recommandée)|
| 🐳 Docker         | Lancement local via `docker-compose`                   |
| 🚦 CI/CD          | GitHub Actions (`lint`, `tests`, `deploy`)             |
| 🌍 API            | FastAPI (`/`, `/status`, `/chat`, etc.)                |
| 🏷 Version active | `v1.2.1` (dernier tag stable)                          |

---

## 📁 Structure Type — `arkalia-luna-pro/`

```
arkalia-luna-pro/
├── modules/               # Modules IA autonomes (1 fonction = 1 dossier)
├── core/                  # Logique transversale partagée
├── config/                # Fichiers de configuration TOML/JSON
├── logs/                  # Logs du système (temps réel, historisés)
├── state/                 # États persistants des modules
├── scripts/               # Scripts d’automatisation (build, test, docker)
├── tests/                 # Tests unitaires, intégration et couverture
├── docs/                  # Documentation MkDocs (publique)
├── .github/workflows/     # CI GitHub Actions
```

---

## 🧩 Philosophie de Conception

| Principe                     | Application concrète                          |
|-----------------------------|-----------------------------------------------|
| 🔒 Stabilité                 | Kernel figé, sans dette technique              |
| 🧠 Modularité                | Chaque module IA est autonome et testable     |
| 🧪 Qualité                   | CI active : `black`, `ruff`, `pytest`, `cov`  |
| 📚 Documentation continue   | Auto-générée avec MkDocs, versionnée          |
| 🛰 Déploiement local maîtrisé | Docker + scripts `ark-docker`, `ark-test`, etc.|

---

🧠 Le système Arkalia est conçu comme un **noyau cognitif auto-réflexif**, industriel, extensible et maîtrisé localement — sans dépendance cloud.
