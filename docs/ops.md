# 🧠 Arkalia IA Ops — Infrastructure Cognitive

Bienvenue dans le **système de surveillance cognitive** d'Arkalia.

---

## 🔐 Santé cognitive : ZeroIA

- `ark-zeroia-health` → Vérifie le fichier TOML (`zeroia_state.toml`)
- `ark-zeroia-rollback` → Restaure un état précédent si erreur détectée
- `ark-monitor` → Affiche l'état JSON + TOML de ZeroIA

---

## 🧪 Pre-commit

- Hook `zeroia-healthcheck` exécuté à chaque commit
- Évite les pushs avec un état corrompu ou invalide

---

## 📊 Dashboard à venir

> Export Grafana / Prometheus bientôt connecté à ReflexIA

---

## 🧠 Prochaine phase IA Ops

- Ajout de `reflexia_monitor.py`
- Export des snapshots vers Grafana
- Génération automatique de rapports Markdown
