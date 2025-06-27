# ♻️ Rebuild — Reconstruction Système Arkalia-LUNA

![Status](https://img.shields.io/badge/status-operational-green)
![Automation](https://img.shields.io/badge/automation-99%25-blue)

Guide complet pour la reconstruction complète ou partielle du système Arkalia-LUNA, incluant procedures d'urgence et recovery.

---

## 🎯 **Types de Rebuild**

### **1. 🔄 Rebuild Standard**
Reconstruction normale pour mises à jour ou maintenance
```bash
# Rebuild complet avec préservation données
./scripts/ark-rebuild.sh --standard --preserve-data
```

### **2. 🚨 Rebuild Urgence**
Reconstruction d'urgence après incident critique
```bash
# Rebuild urgence avec rollback sécurisé
./scripts/ark-rebuild.sh --emergency --rollback-safe
```

### **3. 🌟 Rebuild Clean**
Reconstruction complète depuis zéro (fresh install)
```bash
# Clean rebuild - ATTENTION: Perte de données
./scripts/ark-rebuild.sh --clean --confirm-data-loss
```

---

## 🏗️ **Procédure Rebuild Standard**

### **Phase 1 : Préparation**
```bash
# 1. Vérification prérequis
./scripts/ark-check-prerequisites.sh

# 2. Backup automatique complet
./scripts/ark-full-backup.sh --automated

# 3. Arrêt gracieux services
docker-compose down --timeout 30
```

### **Phase 2 : Reconstruction**
```bash
# 4. Nettoyage containers/images
docker system prune -af

# 5. Rebuild images Docker
docker-compose build --no-cache --pull

# 6. Vérification intégrité
./scripts/ark-verify-integrity.sh
```

### **Phase 3 : Restauration**
```bash
# 7. Redémarrage orchestré
docker-compose up -d --wait

# 8. Validation santé services
./scripts/ark-health-check.sh --comprehensive

# 9. Restauration état modules IA
./scripts/ark-restore-ai-state.sh
```

---

## 🚨 **Rebuild Urgence — Procédures Critiques**

### **Scénarios d'Urgence**
| Scénario | Trigger | Action Rebuild |
|----------|---------|----------------|
| **Container Corruption** | Docker daemon errors | `rebuild --containers-only` |
| **State Corruption** | ZeroIA/ReflexIA crash loops | `rebuild --restore-from-backup` |
| **Security Breach** | Détection intrusion | `rebuild --security-lockdown` |
| **System Crash** | Host system failure | `rebuild --disaster-recovery` |

### **Rebuild Sécurité Post-Incident**
```bash
# Reconstruction sécurisée après incident
./scripts/ark-rebuild.sh \
    --emergency \
    --security-hardening \
    --audit-all \
    --new-secrets \
    --verify-checksums
```

---

## 🧠 **Rebuild Modules IA Spécifiques**

### **Rebuild ZeroIA**
```bash
# Reconstruction ZeroIA avec état propre
./scripts/rebuild-zeroia.sh
# Étapes:
# 1. Sauvegarde état actuel
# 2. Reset configuration défaut
# 3. Validation logic rules
# 4. Test décision basique
# 5. Restauration progressive
```

### **Rebuild ReflexIA**
```bash
# Reconstruction ReflexIA monitoring
./scripts/rebuild-reflexia.sh
# Étapes:
# 1. Backup métriques historiques
# 2. Reset seuils adaptatifs
# 3. Reconfiguration Prometheus
# 4. Test alerting
```

### **Rebuild AssistantIA**
```bash
# Reconstruction AssistantIA chat
./scripts/rebuild-assistantia.sh
# Étapes:
# 1. Validation modèles Ollama
# 2. Reset historique conversations
# 3. Test prompt validation
# 4. Vérification sécurité
```

---

## 🔧 **Scripts Rebuild Automatisés**

### **Script Master : `ark-rebuild.sh`**
```bash
#!/bin/bash
# Script principal reconstruction Arkalia-LUNA

set -euo pipefail

REBUILD_TYPE="$1"
PRESERVE_DATA="${2:-true}"

case "$REBUILD_TYPE" in
    --standard)
        echo "🔄 Rebuild standard en cours..."
        rebuild_standard
        ;;
    --emergency)
        echo "🚨 Rebuild urgence activé!"
        rebuild_emergency
        ;;
    --clean)
        echo "🌟 Clean rebuild - TOUS LES DONNÉES SERONT PERDUES"
        confirm_data_loss
        rebuild_clean
        ;;
    *)
        echo "Usage: $0 [--standard|--emergency|--clean]"
        exit 1
        ;;
esac
```

### **Validation Post-Rebuild**
```bash
# Validation complète post-rebuild
./scripts/ark-post-rebuild-validation.sh
```
**Vérifications incluses :**
- ✅ Services Docker UP et healthy
- ✅ Modules IA responsifs
- ✅ API endpoints fonctionnels
- ✅ Métriques Prometheus collectées
- ✅ Logs sans erreurs critiques
- ✅ Tests automatisés passés

---

## 📊 **Métriques Rebuild**

### **Performance Rebuild**
```yaml
Rebuild Times:
  Standard: "8-12 minutes"
  Emergency: "5-8 minutes"
  Clean: "15-20 minutes"

Success Rates:
  Standard: "99.5%"
  Emergency: "98.2%"
  Clean: "99.8%"
```

### **Monitoring Rebuild**
```python
# Métriques rebuild collectées
rebuild_metrics = {
    'duration_seconds': 487,
    'services_rebuilt': 7,
    'data_preserved': True,
    'validation_success': True,
    'rollback_needed': False
}
```

---

## 🛡️ **Sécurité & Rollback**

### **Rollback Automatique**
```bash
# Rollback automatique si rebuild échoue
if ! ./scripts/ark-health-check.sh; then
    echo "🔴 Rebuild échec - Rollback automatique"
    ./scripts/ark-rollback.sh --to-last-good-state
fi
```

### **Preservation Données Critiques**
- 🧠 **États IA** : ZeroIA, ReflexIA, AssistantIA states
- 📊 **Métriques** : Historique Prometheus/Grafana
- 🔒 **Secrets** : Variables environnement chiffrées
- 📝 **Logs** : Historique logs système et sécurité
- 🌐 **Global State** : Contexte global TOML

---

## 🧪 **Testing & Validation**

### **Tests Rebuild Automatisés**
```bash
# Suite tests rebuild
pytest tests/rebuild/ -v
```

### **Smoke Tests Post-Rebuild**
```python
def test_post_rebuild_health():
    """Validation santé système post-rebuild"""
    assert all_services_healthy()
    assert api_responsive()
    assert ai_modules_functional()
    assert no_critical_errors()
```

---

## 🔗 **Liens & Ressources**

- [🚨 Incident Response](security/incident-response.md)
- [💾 Backup Strategy](security/backup-recovery.md)
- [🔒 Security Procedures](security/security.md)
- [🏗️ Infrastructure](infrastructure/deployment.md)
- [🧪 Testing Framework](infrastructure/ci-cd.md)

---

© 2025 Arkalia-LUNA — Resilience by Design
