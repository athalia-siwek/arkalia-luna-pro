# 🧠 ReflexIA Enhanced — Agent Adaptatif Intelligent

![Version](https://img.shields.io/badge/version-v3.0--phase1-blue)
![CI](https://github.com/athalia-siwek/arkalia-luna-pro/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-Proprietary-red)
![Coverage](https://img.shields.io/badge/coverage-36%25-brightgreen)

Reflexia Enhanced est un module de supervision cognitive autonome avec **vraies métriques système**.

---

## 🚀 **NOUVEAU** : Reflexia Enhanced v2.8.0

### ✨ Fonctionnalités Révolutionnaires

#### 📊 Vraies Métriques Système
- **CPU/RAM/Disk réels** via `psutil` (plus de métriques statiques !)
- **Monitoring Docker** : État containers Arkalia en temps réel
- **Analyse logs** : Détection erreurs récentes automatique
- **Performance** : Collection <2s par cycle (optimisé)

#### 🧠 Intelligence Avancée
- **Détection anomalies** : CPU >80%, RAM >85%, Disk >90%
- **Recommandations automatiques** : Actions correctives suggérées
- **Status adaptatif** : `ok`, `degraded`, `critical` selon métriques
- **Logs structurés** : Timestamps, métriques, recommandations

#### 🐳 Container Integration
- **Surveillance Arkalia** : ZeroIA, Sandozia, AssistantIA status
- **Healthcheck intelligent** : Détection containers défaillants
- **Corrélation état** : Métriques système ↔ containers ↔ modules

---

## 🔄 Fonctionnement Enhanced

### Cycle Reflexia v2.8.0
```
[15:59:19] Reflexia Cycle #1
💻 CPU: 15.8% | RAM: 76.6% | Status: degraded
🐳 Containers: 4 actifs (zeroia: healthy, sandozia: healthy...)
🎯 Recommandations:
   • ⚠️ RAM élevée: Optimiser l'usage mémoire
   • ✅ Système nominal - Continuer surveillance
⏱️ Cycle time: 2.07s
```

### Analyse Intelligente
- **Système** : CPU, RAM, disque avec seuils dynamiques
- **Containers** : État Docker Arkalia + recommandations
- **Modules** : ZeroIA, Sandozia, logs d'erreur
- **Performance** : Temps de collection et optimisations

---

## 📂 Architecture Enhanced

### Structure Modules
```
modules/reflexia/
├── core.py                    # Interface Enhanced v2.8.0
├── logic/
│   ├── metrics_enhanced.py    # 🆕 Vraies métriques système
│   ├── main_loop_enhanced.py  # 🆕 Boucle intelligente
│   ├── decision.py            # Logique décision (compatible)
│   └── snapshot.py            # Sauvegarde état
├── config/weights.toml        # Pondération personnalisée
└── state/reflexia_state.toml  # Mémoire persistante
```

### Métriques Collectées
```json
{
  "system": {
    "cpu_percent": 15.8,
    "memory_percent": 76.6,
    "disk_usage": 7.7
  },
  "containers": {
    "zeroia": "healthy",
    "sandozia": "healthy",
    "reflexia": "running",
    "assistantia": "running"
  },
  "performance": {
    "collection_time_ms": 2070.5,
    "metrics_version": "enhanced_v2.8.0"
  }
}
```

---

## 🚀 Utilisation

### Lancement Container (Auto Enhanced)
```bash
docker-compose up reflexia
```

### Test Enhanced Local
```bash
# Demo 3 cycles avec vraies métriques
ark-reflexia-enhanced

# Ou directement
python scripts/demo_reflexia_enhanced.py
```

### Monitoring Temps Réel
```bash
# Logs Enhanced en live
ark-reflexia-logs

# Ou directement
docker logs reflexia --tail=15 -f
```

---

## 🎯 Recommandations Automatiques

### Exemples Générés
- **CPU Critique** : `🔥 CPU critique: Vérifier les processus lourds`
- **RAM Élevée** : `⚠️ RAM élevée: Optimiser l'usage mémoire`
- **Containers** : `🔥 Containers défaillants: Vérifier docker-compose`
- **Nominal** : `✅ Système nominal - Continuer surveillance`

### Actions Correctives
- **Auto-détection** dégradations performance
- **Alertes proactives** avant pannes critiques
- **Intégration ZeroIA** pour décisions autonomes
- **Corrélation Sandozia** pour intelligence croisée

---

## 📊 Performance Enhanced

### Métriques Observées
- **Collection** : 2.07-2.09s par cycle (vs 5s avant)
- **Précision** : Métriques système ±0.1% précision
- **Containers** : Detection <100ms status Docker
- **Intelligence** : Recommandations contextuelles automatiques

### Comparaison v2.4.0 → v2.8.0
| Fonctionnalité | v2.4.0 | v2.8.0 Enhanced |
|---|---|---|
| Métriques | Static fake | Vraies (psutil) |
| Performance | 5s/cycle | 2s/cycle |
| Containers | Non | Docker integration |
| Recommandations | Non | IA automatiques |
| Logs | Répétitifs | Structurés + timestamps |

---

## 🔧 Configuration

### Dependencies
```toml
# requirements.txt
psutil>=5.9.0     # Métriques système réelles
diskcache>=5.6.3  # Cache performances
```

### Docker Healthcheck
```dockerfile
# Container optimisé Enhanced
HEALTHCHECK --interval=30s --timeout=5s \
  CMD python modules/reflexia/core.py
```

---

## 🐛 Troubleshooting Enhanced

### Diagnostics Avancés
```bash
# Test métriques système
python modules/reflexia/logic/metrics_enhanced.py

# Vérif containers Docker
docker ps --filter name="zeroia|sandozia|reflexia|assistantia"

# Analyse logs erreurs
tail -f logs/reflexia.log
```

### Problèmes Fréquents
- **Métriques manquantes** : Installer `pip install psutil`
- **Containers non détectés** : Vérifier Docker daemon
- **Performance lente** : Vérifier espace disque disponible

---

## 📈 Roadmap

### Version 2.7.0 (Prochaine)
- **Machine Learning** : Détection patterns anormaux
- **Alerting** : Notifications Slack/email automatiques
- **Predictive** : Prédiction pannes avant occurrence
- **API REST** : Endpoints métriques externes

---

© 2025 **Athalia** – Tous droits réservés.
🤖 Powered by Arkalia **ReflexIA Enhanced v2.8.0**

# Documentation du Module ReflexIA

## Introduction
Le module ReflexIA est conçu pour fournir des capacités avancées de surveillance et de réponse automatique aux événements système. Il joue un rôle crucial dans la détection précoce des anomalies et la prévention des pannes.

## Fonctionnalités
- **Surveillance en Temps Réel** : ReflexIA surveille en continu les métriques système pour détecter les anomalies.
- **Réponse Automatique** : Lorsqu'une anomalie est détectée, ReflexIA peut déclencher des actions correctives automatiquement.
- **Rapports Détaillés** : Génère des rapports détaillés sur les événements et les actions prises.

## Configuration
Pour configurer ReflexIA, modifiez le fichier `reflexia_config.toml` et ajustez les paramètres selon vos besoins.

## Dépannage
En cas de problème avec ReflexIA, consultez les logs dans `logs/reflexia.log` pour des informations détaillées.
