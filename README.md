# 🌌 Arkalia-LUNA PRO

![Arkalia Logo](https://example.com/logo.png)

**Système Cognitif IA Local • Modulaire • Auto-Réflexif • Documenté**

🧠 Version : **v2.0.2**
📘 Docs : **[arkalia-luna-system.github.io/arkalia-luna-pro](https://arkalia-luna-system.github.io/arkalia-luna-pro)**
🧪 CI • 🐳 Docker • 🧠 ReflexIA • ⚙️ ZeroIA
🔒 Maintenu par Arkalia-LUNA System

⸻

## 📘 Accès Rapide

[![Docs](https://img.shields.io/badge/docs-online-blue?style=flat-square&logo=readthedocs)](https://arkalia-luna-system.github.io/arkalia-luna-pro/)
[![Version](https://img.shields.io/badge/version-v1.3.4-purple?style=flat-square)](https://github.com/arkalia-luna-system/arkalia-luna-pro/releases)
[![CI](https://github.com/arkalia-luna-system/arkalia-luna-pro/actions/workflows/ci.yml/badge.svg)](https://github.com/arkalia-luna-system/arkalia-luna-pro/actions)
[![Pre-Commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen)](https://pre-commit.com/)
[![Tests](https://img.shields.io/badge/tests-100%25-brightgreen?style=flat-square&logo=pytest)](https://github.com/arkalia-luna-system/arkalia-luna-pro/actions)
[![Docker](https://img.shields.io/badge/docker-ready-blue?style=flat-square)](https://www.docker.com/)
[![Sitemap](https://img.shields.io/badge/sitemap-valid-brightgreen?style=flat-square&logo=sitemaps)](https://arkalia-luna-system.github.io/arkalia-luna-pro/sitemap.xml)
[![Ruff](https://img.shields.io/badge/Ruff-validated-brightgreen?style=flat-square)](https://github.com/charliermarsh/ruff-pre-commit)
[![Black](https://img.shields.io/badge/Black-validated-brightgreen?style=flat-square)](https://github.com/psf/black)
[![Coverage](https://img.shields.io/badge/Coverage-92%25-blue?style=flat-square)](https://arkalia-luna-system.github.io/arkalia-luna-pro/coverage)

🌟 Objectif

Construire un système IA local, modulaire, interfaçable et auto-réparant, avec :
	•	📦 Modules IA isolés (reflexia, nyxalia, helloria, assistantia)
	•	🛰️ API FastAPI locale : /status, /trigger, /chat
	•	🔁 Scripts orchestrés par ReflexIA / ZeroIA
	•	🐳 Environnement Dockerisé, testé, CI/CD intégré
	•	🧠 Compatibilité LLM locaux (ollama) : mistral, llama2, tinyllama

⸻

🧱 Architecture

arkalia-luna-pro/
├── core/                  # 💡 Logique transversale (utilisée par tous les modules)
├── modules/               # 🧠 Modules IA autonomes (AssistantIA, ReflexIA, Nyxalia…)
├── config/                # ⚙️ Configurations centralisées (TOML / JSON)
├── logs/                  # 🪵 Logs structurés horodatés
├── state/                 # 💾 États persistants (Reflexia, AssistantIA…)
├── scripts/               # 🛠️ Scripts Docker, ReflexIA, build, CI
├── tests/                 # ✅ Tests unitaires et intégration (Pytest + couverture)
├── docs/                  # 📘 Documentation (MkDocs)
└── .github/workflows/     # 🔁 Workflows CI (GitHub Actions)


🛠️ Scripts essentiels

Script
Fonction
ark-test
Lance tous les tests + génère htmlcov
ark-docker-rebuild.sh
Rebuild complet Docker
ark-clean-push
Formatage auto (black, ruff) + commit
trigger_scan.sh
Déclenche ReflexIA manuellement


🚀 Lancement rapide

🐳 Docker (recommandé)

docker compose down
find . -name '._*' -delete && find . -name '.DS_Store' -delete
docker compose build --no-cache
docker compose up

📍 Accès : http://localhost:8000

💡 Astuces :
	•	ark-test → lance tests + couverture
	•	./scripts/ark-docker-rebuild.sh → rebuild rapide
	•	CI + docs auto via GitHub Actions

⸻

📃 Historique des versions

Version
État
Description technique
v1.3.4
✅ Spéciale
100 % couverture
v1.3.2
✅ Stable
Docs refondues, utilisation.md, navigation optimisée
v1.3.1
✅ Validé
Couverture > 85 %, Docker, CI OK
v1.0.9
✅ Propre
Design final, architecture stable
v1.0.6
✅ Solide
Docker + couverture 100 %, CI
v0.3.0
🛠️ Base
FastAPI + Docker fonctionnel
v0.1.1
🚀 Départ
Devstation + env IA locale


🧠 AssistantIA

Module IA de dialogue contextuel, branché sur Ollama (Mistral, TinyLLaMA)

	•	Port local : 8001
	•	Dev local : uvicorn modules.assistantia.core:app --port 8001
	•	Docker : docker-compose up assistantia

    Méthode
URL
Description
GET
/
Accueil API AssistantIA
POST
/chat
Dialogue avec la LLM


📘 [Voir la documentation complète](docs/assistantia.md)

⸻

🐳 Services Docker actifs

Service
Port
Lancement
arkalia-api
8000
docker-compose up arkalia-api
assistantia
8001
docker-compose up assistantia


🧠 Vision & avenir

Modules à venir :
	•	kaelia/ → gestion cognitive de tâches complexes
	•	psykalia/ → analyse émotionnelle et psycholinguistique
	•	Mémoire vectorielle (FAISS)
	•	Monitoring système (Prometheus, Grafana)

⸻

🌓 Un projet signé Arkalia-LUNA — système IA local, durable, interconnectable.

- [API](https://arkalia-luna-system.github.io/arkalia-luna-pro/api)
- [Modules](https://arkalia-luna-system.github.io/arkalia-luna-pro/modules)
- [CI/CD](https://arkalia-luna-system.github.io/arkalia-luna-pro/ci-cd)
- [Tests](https://arkalia-luna-system.github.io/arkalia-luna-pro/tests)


