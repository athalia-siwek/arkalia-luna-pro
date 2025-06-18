# 🧬 Structure du noyau Arkalia

Le noyau IA est divisé en 2 zones :

## 1️⃣ `/arkalia-luna-core/` (Kernel pur)

- Config système
- Versionnage
- Aucun code métier
- Exécutable : `arkalia_devstation_bootstrap.sh`

## 2️⃣ `/arkalia-luna-pro/` (Devstation IA)

- Modules IA
- Serveur API (FastAPI)
- Docker, tests, CI
- Version actuelle : `v1.0.6`

## Structure type :
arkalia-luna-pro/
├── modules/
├── core/
├── config/
├── logs/
├── state/
├── scripts/
├── docs/
├── tests/
├── .github/workflows/