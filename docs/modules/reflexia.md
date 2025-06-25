# 🧠 ReflexIA — Agent Adaptatif

![Version](https://img.shields.io/badge/version-v2.4.0-blue)
![CI](https://github.com/athalia-siwek/arkalia-luna-pro/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-Proprietary-red)
![Coverage](https://img.shields.io/badge/coverage-93%25-brightgreen)

Reflexia est un module de supervision cognitive autonome.

---

## 🔄 Fonctionnement

- Analyse les modules Arkalia toutes les `x` secondes
- Pondère leur état (CPU, erreurs, logs)
- Prend une décision (`continue`, `pause`, `reboot`, `alert`)
- Enregistre chaque cycle dans un journal réflexif

---

## 📂 Dossiers

- `modules/reflexia/logic/` : décision, snapshot, métriques
- `modules/reflexia/config/weights.toml` : pondération personnalisée
- `modules/reflexia/state/reflexia_state.toml` : mémoire du module

---

## 🐳 Lancement via Docker

```bash
docker-compose up reflexia
```

---

© 2025 **Athalia** – Tous droits réservés.
🤖 Powered by Arkalia ReflexIA `v1.x`
