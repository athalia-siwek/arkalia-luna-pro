# 🔧 ZeroIA Troubleshooting — Guide v3.x

![Version](https://img.shields.io/badge/version-v3.0--phase2-blue)
![Support](https://img.shields.io/badge/support-24%2F7-green)
![Intelligence](https://img.shields.io/badge/sandozia-diagnostic-blue)

Guide complet de **dépannage ZeroIA v3.x** avec **Sandozia Intelligence Croisée** et diagnostic automatique enterprise.

---

## 🚨 Diagnostic Rapide v3.x

### **Commandes Essentielles**
```bash
# Santé cognitive complète
ark-zeroia-health

# Diagnostic approfondi avec Sandozia
ark-zeroia-full

# Debug et redémarrage intelligent
ark-debug-zeroia

# Status temps réel
ark-zeroia-status
```

---

## 🔍 Erreurs de Démarrage v3.x

### **1. Échec Initialisation Sandozia**
**Symptômes :**
```
ERROR: Sandozia intelligence croisée inaccessible
ERROR: Cross-module validation failed
```

**Solutions :**
```bash
# Vérification Sandozia Core
ark-sandozia-status

# Restart coordonné avec Sandozia
ark-restart-all

# Rebuild Sandozia si nécessaire
ark-rebuild-sandozia
```

### **2. Configuration TOML Corrompue**
**Symptômes :**
```
ERROR: Unable to parse zeroia_state.toml
ERROR: Invalid configuration format
```

**Solutions :**
```bash
# Validation configuration
python -c "import toml; toml.load('state/zeroia_state.toml')"

# Rollback configuration
ark-zeroia-rollback

# Regeneration clean
cp state/zeroia_state_backup.toml state/zeroia_state.toml
```

### **3. Seuils Adaptatifs Défaillants**
**Symptômes :**
```
WARNING: Adaptive thresholds not responding
ERROR: ML model corruption detected
```

**Solutions :**
```bash
# Reset seuils adaptatifs
python modules/zeroia/adaptive_thresholds.py --reset

# Recalibration avec Sandozia
ark-zeroia-calibrate

# Restore from backup
ark-zeroia-restore --adaptive-thresholds
```

---

## ⚡ Problèmes Performance v3.x

### **1. Latence Élevée Détection**
**Diagnostic :**
```bash
# Métriques performance temps réel
ark-zeroia-metrics --performance

# Profiling détaillé
python -m cProfile modules/zeroia/reason_loop.py
```

**Optimisations :**
```bash
# Cache optimization
redis-cli FLUSHDB  # Reset cache Redis

# Réduction fréquence monitoring
# Edit: config/zeroia_config.toml
# monitoring_interval = 10  # Default: 5

# Parallélisation détection
# enable_parallel_detection = true
```

### **2. Utilisation Mémoire Excessive**
**Diagnostic :**
```bash
# Memory profiling
memory_profiler python modules/zeroia/confidence_score.py

# Analyse leaks mémoire
valgrind --tool=memcheck python modules/zeroia/reason_loop.py
```

**Solutions :**
```bash
# Nettoyage cache automatique
python scripts/zeroia_memory_cleanup.py

# Réduction historique métriques
# Edit: retention_days = 7  # Default: 30

# Garbage collection forcé
python -c "import gc; gc.collect()"
```

---

## 🧠 Problèmes Intelligence Croisée

### **1. Désynchronisation Sandozia**
**Symptômes :**
```
WARNING: Cross-correlation below threshold (0.85)
ERROR: Sandozia consensus timeout
```

**Solutions :**
```bash
# Resync avec Sandozia
ark-sandozia-sync --force

# Validation consensus
ark-sandozia-validator --zeroia-focus

# Rebuild relation cross-module
ark-rebuild-cross-validation
```

### **2. Consensus Décisionnel Bloqué**
**Symptômes :**
```
ERROR: Decision consensus timeout (30s)
WARNING: Reflexia approval pending
```

**Solutions :**
```bash
# Bypass consensus temporaire
export ZEROIA_BYPASS_CONSENSUS=true

# Debug consensus workflow
python modules/zeroia/logic/reflexia_check_trigger.py --debug

# Reset consensus state
rm state/zeroia_decision_log.toml
```

---

## 📊 Logs et Monitoring v3.x

### **Analyse Logs Avancée**
```bash
# Logs erreurs dernières 24h
tail -f logs/zeroia.log | grep ERROR | head -100

# Patterns suspects Sandozia
grep "cross_validation_failed" logs/zeroia.log

# Métriques détection anomalies
cat logs/model_integrity.log | jq '.anomaly_score'
```

### **Dashboard Monitoring**
- **Grafana ZeroIA** : http://localhost:3000/d/zeroia
- **Prometheus Metrics** : http://localhost:9090/targets
- **Sandozia Dashboard** : http://localhost:3000/d/sandozia

### **Alertes Configurées**
```yaml
Alerts:
  - "ZeroIA Detection Rate < 95%"
  - "Sandozia Correlation < 0.95"
  - "Response Time > 200ms"
  - "Memory Usage > 85%"
```

---

## 🚨 FAQ Troubleshooting v3.x

### **Q: ZeroIA ne détecte plus d'anomalies ?**
```bash
# Test détection manuel
python -c "from modules.zeroia.reason_loop import test_detection; test_detection()"

# Vérification seuils
cat state/zeroia_state.toml | grep threshold

# Recalibration forcée
ark-zeroia-calibrate --force
```

### **Q: Sandozia rapporte incohérences ZeroIA ?**
```bash
# Validation état ZeroIA
ark-sandozia-validator --zeroia-deep-check

# Synchronisation forcée
ark-zeroia-sync-sandozia

# Reset relation cross-module
ark-reset-cross-validation --zeroia
```

### **Q: Erreurs "Decision loop stuck" ?**
```bash
# Kill boucle bloquée
pkill -f "reason_loop.py"

# Nettoyage état décisionnel
rm state/zeroia_decision_log.toml

# Restart propre
ark-zeroia-restart --clean
```

### **Q: Performance dégradée après update ?**
```bash
# Comparaison avant/après
ark-zeroia-benchmark --compare

# Rollback version précédente
git checkout HEAD~1 modules/zeroia/

# Migration configuration
python scripts/migrate_zeroia_config.py --to-v3
```

---

## 🔧 Scripts Utilitaires v3.x

### **Diagnostic Automatique**
```bash
#!/bin/bash
# ark-zeroia-diagnose.sh

echo "🔍 Diagnostic ZeroIA v3.x complet..."

# 1. Santé services
ark-zeroia-health

# 2. Validation Sandozia
ark-sandozia-validator --zeroia-focus

# 3. Performance metrics
ark-zeroia-metrics --full

# 4. Configuration check
python -m modules.zeroia.config.validator

echo "✅ Diagnostic terminé"
```

### **Recovery Automatique**
```bash
#!/bin/bash
# ark-zeroia-auto-recovery.sh

if ! ark-zeroia-health --silent; then
    echo "🚨 ZeroIA défaillant - Recovery automatique..."

    # 1. Sauvegarde état
    cp state/zeroia_state.toml state/zeroia_backup_$(date +%s).toml

    # 2. Restart coordonné
    ark-debug-zeroia

    # 3. Validation recovery
    ark-zeroia-health --post-recovery
fi
```

---

## 📞 Support Enterprise

### **Escalation Matrix**
| Sévérité | Temps Réponse | Contact |
|----------|---------------|---------|
| **P1 - Critique** | < 15min | enterprise@arkalia-luna.com |
| **P2 - Majeur** | < 2h | support@arkalia-luna.com |
| **P3 - Mineur** | < 24h | GitHub Issues |

### **Collecte Logs pour Support**
```bash
# Package logs pour support
tar -czf zeroia_support_$(date +%s).tar.gz \
    logs/zeroia.log \
    logs/model_integrity.log \
    state/zeroia_state.toml \
    config/zeroia_config.toml
```

---

**© 2025 Arkalia-LUNA Team** — ZeroIA Troubleshooting v3.x
🔧 *Powered by Sandozia Intelligence Croisée*
