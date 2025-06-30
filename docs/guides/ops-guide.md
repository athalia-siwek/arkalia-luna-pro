# 🛠️ Operations & Maintenance - Arkalia-LUNA v2.8.1

Documentation complète des opérations et maintenance d'Arkalia-LUNA avec monitoring intégré.

## 🚀 Guide Operations Complet

### Monitoring et Observabilité
```bash
# Validation monitoring complet
python scripts/ark-validate-monitoring.py

# Vérification services monitoring
docker-compose -f infrastructure/monitoring/docker-compose.monitoring.yml ps

# Métriques temps réel
curl http://localhost:8000/metrics

# Dashboards Grafana
open http://localhost:3000  # admin / arkalia-secure-2025
```

### Services Monitoring
| Service | URL | Description | Credentials |
|---------|-----|-------------|-------------|
| **Grafana** | http://localhost:3000 | Dashboards temps réel | admin / arkalia-secure-2025 |
| **Prometheus** | http://localhost:9090 | Métriques système | - |
| **AlertManager** | http://localhost:9093 | Gestion alertes | - |
| **Loki** | http://localhost:3100 | Centralisation logs | - |
| **cAdvisor** | http://localhost:8080 | Métriques conteneurs | - |
| **Arkalia API** | http://localhost:8000 | API principale + métriques | - |

## 📊 Commandes Rapides

### Monitoring
```bash
# Statut système complet
ark-status

# Health check complet
ark-check-all

# Logs en temps réel
ark-zeroia-logs

# Validation monitoring
python scripts/ark-validate-monitoring.py

# Métriques Arkalia
curl http://localhost:8000/metrics | grep arkalia

# Dashboard principal
open http://localhost:3000/d/arkalia-monitoring
```

### Maintenance
```bash
# Nettoyage automatique
ark-clean

# Backup complet
ark-backup

# Health check ZeroIA
ark-zeroia-health

# Redémarrer monitoring
cd infrastructure/monitoring
docker-compose -f docker-compose.monitoring.yml restart

# Nettoyer monitoring
docker system prune -f
```

### Troubleshooting
```bash
# Vérifier services monitoring
docker ps | grep monitoring

# Logs Prometheus
docker logs prometheus

# Logs Grafana
docker logs grafana

# Logs AlertManager
docker logs alertmanager

# Redémarrer services
cd infrastructure/monitoring
docker-compose -f docker-compose.monitoring.yml down
docker-compose -f docker-compose.monitoring.yml up -d
```

## 🎯 Métriques Clés

### Performance
- **Temps de réponse** : < 2s (P95)
- **Disponibilité** : 99.9%+
- **Latence système** : < 100ms
- **Recovery Time** : < 100ms automatique

### Monitoring
- **Métriques exposées** : 34 métriques Arkalia
- **Dashboards** : 8 panels Grafana
- **Alertes actives** : 15 règles Prometheus
- **Services monitoring** : 7 composants

### Modules
- **ZeroIA** : Score de confiance > 0.8
- **AssistantIA** : Temps de réponse < 5s
- **Reflexia** : Monitoring système actif
- **Tous modules** : Statut actif

## 🚨 Alertes Principales

### Alertes Critiques
- **ModuleInactive** : Module Arkalia inactif
- **HighErrorRate** : > 5% erreurs 5xx
- **HighRequestLatency** : Latence > 2s
- **ArkaliaHighCPU** : CPU > 80%

### Alertes Warning
- **ZeroIALowConfidence** : Confiance < 30%
- **AssistantIAHighResponseTime** : Temps réponse > 10s
- **ArkaliaHighMemory** : RAM > 6GB
- **SecurityHighBlockRate** : > 20 blocages/min

## 🔧 Maintenance Avancée

### Sauvegarde Monitoring
```bash
# Sauvegarder configurations
docker cp prometheus:/etc/prometheus ./backup/prometheus/
docker cp grafana:/etc/grafana ./backup/grafana/
docker cp alertmanager:/etc/alertmanager ./backup/alertmanager/

# Sauvegarder données
docker cp prometheus:/prometheus ./backup/prometheus-data/
docker cp grafana:/var/lib/grafana ./backup/grafana-data/
```

### Mise à Jour
```bash
# Arrêter services
cd infrastructure/monitoring
docker-compose -f docker-compose.monitoring.yml down

# Mettre à jour images
docker-compose -f docker-compose.monitoring.yml pull

# Redémarrer
docker-compose -f docker-compose.monitoring.yml up -d
```

### Nettoyage
```bash
# Nettoyer anciennes données
docker volume prune

# Nettoyer logs
docker system prune -f

# Redémarrer proprement
cd infrastructure/monitoring
docker-compose -f docker-compose.monitoring.yml down
docker-compose -f docker-compose.monitoring.yml up -d
```

## 📈 Validation Continue

### Tests Automatisés
```bash
# Validation complète
python scripts/ark-validate-monitoring.py

# Tests modules
ark-test

# Tests performance
ark-test-performance

# Tests sécurité
ark-test-security
```

### Rapports
- **Rapport monitoring** : `logs/monitoring_validation_*.json`
- **Rapport tests** : `htmlcov/`
- **Rapport sécurité** : `logs/bandit_report.txt`
- **Rapport performance** : `benchmark_results/`

## 🎯 Prochaines Étapes

1. **Explorer Grafana** : http://localhost:3000
2. **Vérifier Prometheus** : http://localhost:9090
3. **Configurer alertes** : http://localhost:9093
4. **Analyser logs** : http://localhost:3100
5. **Monitorer conteneurs** : http://localhost:8080

---

[📖 Guide Complet →](ops-guide.md)

💡 **Le monitoring Arkalia-LUNA v2.8.1 offre une observabilité totale avec 34 métriques, 8 dashboards et 15 alertes pour garantir la fiabilité et les performances du système IA.**
