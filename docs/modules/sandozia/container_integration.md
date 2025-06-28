# 🧠 Sandozia Container Integration v2.6.1

## 📖 Vue d'Ensemble

Sandozia Intelligence Croisée est maintenant complètement dockerisé et intégré dans l'infrastructure container d'Arkalia-LUNA. Ce document détaille l'implémentation, l'utilisation et les métriques du container Sandozia.

## 🐳 Architecture Container

### Dockerfile.sandozia
- **Base Image** : `python:3.10-slim`
- **Sécurité** : Utilisateur non-root `sandozia`
- **Environment** : `SANDOZIA_ENV=production`
- **Healthcheck** : Validation SandoziaCore toutes les 45s
- **Dependencies** : Isolation complète avec requirements.txt

### Configuration Docker Compose
```yaml
sandozia:
  container_name: sandozia
  build:
    dockerfile: Dockerfile.sandozia
  command: python scripts/demo_sandozia.py --daemon
  environment:
    - SANDOZIA_ENV=production
    - SANDOZIA_MONITORING_ENABLED=true
  depends_on:
    - zeroia
    - reflexia
  healthcheck:
    test: ["CMD", "python", "-c", "from modules.sandozia.core.sandozia_core import SandoziaCore; print('OK')"]
    interval: 45s
    timeout: 10s
    retries: 3
    start_period: 20s
```

## 🔄 Mode Daemon

### Fonctionnement
Le container Sandozia tourne en **mode daemon** avec une boucle infinie qui :

1. **Validation Croisée** : Analyse cohérence entre modules (ZeroIA, Reflexia)
2. **Analyse Comportementale** : Détection patterns et anomalies
3. **Métriques Intégrées** : Collecte données de performance
4. **Intelligence Snapshot** : Capture état global du système

### Cycle de Fonctionnement
```
Cycle N (15s) :
├── 🔍 CrossModuleValidator.run_full_validation()
├── 🧠 BehaviorAnalyzer.analyze_behavior()
├── 📊 SandoziaMetrics.collect_all_metrics()
├── 🎯 SandoziaCore.collect_intelligence_snapshot()
└── 💤 Pause 15s avant cycle N+1
```

## 📊 Métriques & Performance

### Score Global Intelligence
- **Performance mesurée** : 0.831/1.0 (Excellent)
- **Seuil minimum** : 0.700
- **Seuil optimal** : 0.800+

### Modules Connectés
- **ZeroIA** : ✅ Connexion active
- **Reflexia** : ✅ Connexion active
- **Ratio** : 2/2 (100% connectivity)

### Snapshots Intelligence
- **Fréquence** : 3 snapshots par cycle daemon
- **Stockage** : Cache disque avec éviction LRU
- **Patterns** : Détection automatique anomalies comportementales

## 🛠️ Utilisation & Commandes

### Aliases ZSH Disponibles
```bash
# Logs temps réel Sandozia
ark-sandozia-logs

# Statut container Sandozia
ark-sandozia-status

# Vue d'ensemble tous modules IA
ark-all-status
```

### Gestion Container
```bash
# Démarrer Sandozia
docker-compose up sandozia -d

# Redémarrer avec rebuild
docker-compose stop sandozia
docker-compose build sandozia
docker-compose up sandozia -d

# Logs détaillés
docker logs sandozia --tail 50 -f

# Healthcheck manuel
docker exec sandozia python -c "from modules.sandozia.core.sandozia_core import SandoziaCore; print('OK')"
```

## 🔍 Monitoring & Diagnostics

### Healthcheck Status
- **Interval** : 45 secondes
- **Timeout** : 10 secondes
- **Retries** : 3 tentatives
- **Start Period** : 20 secondes

### Logs Patterns
```
🔄 === CYCLE SANDOZIA DAEMON N ===
⏰ HH:MM:SS
📊 Score global Sandozia: 0.831
✅ Modules connectés: 2/2
🎯 Status après N cycles: [détails performance]
💤 Pause 15s avant prochain cycle...
```

### Détection Anomalies
Sandozia détecte automatiquement :
- **Incohérences** entre modules
- **Dégradations performance** comportementales
- **Patterns suspects** répétitifs
- **Contradictions** dans les décisions

## 🏗️ Intégration Architecture

### Dependencies Container
```
assistantia (base)
    ↓
reflexia (observateur)
    ↓
zeroia (orchestrator enhanced)
    ↓
sandozia (intelligence croisée)
```

### Réseau Docker
- **Network** : arkalia-luna-pro_default
- **Isolation** : cap_drop=[ALL], no-new-privileges
- **Communication** : Inter-container via noms de services

## 🎯 Recommandations

### Optimisation Performance
1. **Memory** : Monitorer utilisation cache snapshots
2. **CPU** : Cycles daemon optimisés pour production
3. **Network** : Latence inter-containers minimisée

### Sécurité
1. **Utilisateur** : sandozia non-root obligatoire
2. **Capabilities** : ALL dropped pour sécurité maximale
3. **Secrets** : Environment variables pour configuration

### Monitoring
1. **Healthcheck** : Surveillance continue état container
2. **Logs** : Rotation automatique prévue
3. **Métriques** : Score global > 0.800 recommandé

## 🚀 Évolutions Futures

### Phase 1.2 (Prochaine)
- **Error Recovery** : Rollback automatique intelligent
- **Graceful Degradation** : Mode dégradé préservant fonctions critiques

### Phase 3 (Moyen terme)
- **API REST** : Endpoints Sandozia via FastAPI
- **Tests d'intégration** : Suite complète API + Container

---

**📅 Dernière mise à jour** : 28 Juin 2025
**🏷️ Version** : Arkalia-LUNA v2.6.1 Enterprise
**👤 Auteur** : Athalia
**🎯 Status** : ✅ Production Ready
