# 🧠 ReflexIA — Agent Adaptatif

Reflexia est un module de supervision cognitive autonome.

## 🔁 Fonctionnement

- Analyse les modules Arkalia toutes les `x` secondes
- Pondère leur état (CPU, erreurs, logs)
- Prend une décision (`continue`, `pause`, `reboot`, `alert`)
- Enregistre chaque cycle dans un journal réflexif

## 📁 Dossiers

- `modules/reflexia/logic/` : décision, snapshot, métriques
- `modules/reflexia/config/weights.toml` : pondération personnalisée
- `modules/reflexia/state/reflexia_state.toml` : mémoire du module

## 🐳 Lancement via Docker

```bash
docker-compose up reflexia
