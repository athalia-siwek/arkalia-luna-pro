# 📊 Monitoring Complet - Arkalia-LUNA v2.8.0

> Guide complet pour l'infrastructure de monitoring d'Arkalia-LUNA avec observabilité totale, métriques avancées et alertes intelligentes.

---

## 🎯 Vue d'ensemble

Arkalia-LUNA v2.8.0 intègre une infrastructure de monitoring complète et professionnelle :

- **📊 Grafana** : Dashboards temps réel avec 8 panels spécialisés
- **📈 Prometheus** : Collecte et stockage de 34 métriques Arkalia
- **🚨 AlertManager** : 15 règles d'alertes intelligentes
- **📝 Loki** : Centralisation des logs système
- **🐳 cAdvisor** : Métriques des conteneurs Docker
- **🔌 Arkalia API** : Endpoints métriques intégrés

---

## 🚀 Démarrage Rapide

### 1. Démarrer le Monitoring
```bash
# Aller dans le dossier monitoring
cd infrastructure/monitoring

# Démarrer tous les services
docker-compose -f docker-compose.monitoring.yml up -d

# Vérifier le statut
docker-compose -f docker-compose.monitoring.yml ps
```

### 2. Validation Automatique
```bash
# Validation complète
python scripts/ark-validate-monitoring.py

# Vérification des métriques
curl http://localhost:8000/metrics
```

### 3. Accès aux Services
| Service | URL | Description | Credentials |
|---------|-----|-------------|-------------|
| **Grafana** | http://localhost:3000 | Dashboards temps réel | admin / arkalia-secure-2025 |
| **Prometheus** | http://localhost:9090 | Métriques système | - |
| **AlertManager** | http://localhost:9093 | Gestion alertes | - |
| **Loki** | http://localhost:3100 | Centralisation logs | - |
| **cAdvisor** | http://localhost:8080 | Métriques conteneurs | - |
| **Arkalia API** | http://localhost:8000 | API principale + métriques | - |

---

## 📊 Métriques Arkalia

### Métriques Système
- `arkalia_system_cpu_usage` : Utilisation CPU en pourcentage
- `arkalia_system_memory_usage` : Utilisation mémoire en bytes
- `arkalia_system_disk_usage` : Utilisation disque en pourcentage
- `arkalia_system_uptime` : Temps de fonctionnement en secondes
- `arkalia_system_load_average` : Charge système moyenne

### Métriques API
- `arkalia_api (port 8000)_requests_total` : Nombre total de requêtes
- `arkalia_api (port 8000)_request_duration_seconds` : Durée des requêtes
- `arkalia_api (port 8000)_requests_in_progress` : Requêtes en cours
- `arkalia_api (port 8000)_errors_total` : Nombre total d'erreurs
- `arkalia_api (port 8000)_response_size_bytes` : Taille des réponses

### Métriques Modules
- `arkalia_module_status` : Statut des modules (0=inactif, 1=actif)
- `arkalia_module_performance_score` : Score de performance (0-1)
- `arkalia_module_confidence_score` : Score de confiance (0-1)
- `arkalia_module_decision_count` : Nombre de décisions prises
- `arkalia_module_error_count` : Nombre d'erreurs

### Métriques ZeroIA
- `arkalia_zeroia_decisions_total` : Décisions prises
- `arkalia_zeroia_confidence_average` : Confiance moyenne
- `arkalia_zeroia_contradictions_detected` : Contradictions détectées
- `arkalia_zeroia_processing_time_seconds` : Temps de traitement
- `arkalia_zeroia_circuit_breaker_status` : Statut circuit breaker

### Métriques AssistantIA
- `arkalia_assistantia_prompts_total` : Prompts traités
- `arkalia_assistantia_response_time_seconds` : Temps de réponse
- `arkalia_assistantia_security_blocks` : Blocages de sécurité
- `arkalia_assistantia_rate_limit_hits` : Limites de taux atteintes
- `arkalia_assistantia_model_usage` : Utilisation des modèles

### Métriques Reflexia
- `arkalia_reflexia_monitoring_checks` : Vérifications monitoring
- `arkalia_reflexia_system_latency_ms` : Latence système
- `arkalia_reflexia_health_score` : Score de santé
- `arkalia_reflexia_alerts_generated` : Alertes générées
- `arkalia_reflexia_recovery_actions` : Actions de récupération

### Métriques Sécurité
- `arkalia_security_blocks_total` : Blocages totaux
- `arkalia_security_rate_limit_violations` : Violations rate limit
- `arkalia_security_invalid_requests` : Requêtes invalides
- `arkalia_security_authentication_failures` : Échecs authentification
- `arkalia_security_authorization_failures` : Échecs autorisation

---

## 🎨 Dashboards Grafana

### Dashboard Principal
- **URL** : http://localhost:3000/d/arkalia-monitoring
- **Panels** : 8 panels spécialisés
- **Refresh** : 30 secondes
- **Thème** : Dark mode

### Panels Disponibles

#### 1. Système CPU & Mémoire
- Utilisation CPU en temps réel
- Utilisation mémoire avec seuils
- Charge système moyenne
- Tendances sur 24h

#### 2. Statut des Modules Arkalia
- Statut de chaque module (actif/inactif)
- Score de performance
- Score de confiance
- Indicateurs de santé

#### 3. Requêtes API en Temps Réel
- Nombre de requêtes par minute
- Répartition par endpoint
- Codes de statut HTTP
- Taux d'erreur

#### 4. Durée des Requêtes (P50/P95)
- Latence moyenne
- Percentiles P50 et P95
- Tendances de performance
- Seuils d'alerte

#### 5. ZeroIA - Confiance & Décisions
- Décisions prises par minute
- Score de confiance moyen
- Contradictions détectées
- Temps de traitement

#### 6. AssistantIA - Prompts & Réponses
- Prompts traités
- Temps de réponse moyen
- Blocages de sécurité
- Utilisation des modèles

#### 7. Reflexia - Monitoring Système
- Vérifications monitoring
- Latence système
- Score de santé
- Actions de récupération

#### 8. Erreurs & Alertes
- Erreurs par type
- Alertes actives
- Violations de sécurité
- Actions correctives

---

## 🚨 Système d'Alertes

### Niveaux de Sévérité
- **Critical** : Modules inactifs, erreurs 5xx, ressources critiques
- **Warning** : Performance dégradée, ressources élevées, seuils approchés
- **Info** : Blocages de sécurité, événements normaux, métriques

### Alertes Principales

#### Alertes Système
- **ArkaliaHighCPU** : CPU > 80% pendant 5 minutes
- **ArkaliaHighMemory** : RAM > 6GB pendant 5 minutes
- **ArkaliaHighDiskUsage** : Disque > 85% utilisé
- **ArkaliaSystemLoad** : Charge système > 5.0

#### Alertes Modules
- **ModuleInactive** : Module Arkalia inactif pendant 2 minutes
- **ModuleLowPerformance** : Performance < 0.5 pendant 5 minutes
- **ModuleLowConfidence** : Confiance < 0.3 pendant 3 minutes
- **ModuleHighErrorRate** : Taux d'erreur > 10%

#### Alertes API
- **HighErrorRate** : > 5% erreurs 5xx pendant 2 minutes
- **HighRequestLatency** : Latence P95 > 2s pendant 3 minutes
- **HighRequestVolume** : > 1000 req/min pendant 5 minutes
- **APIUnavailable** : API inaccessible pendant 1 minute

#### Alertes ZeroIA
- **ZeroIALowConfidence** : Confiance < 30% pendant 3 minutes
- **ZeroIAHighContradictions** : > 5 contradictions/min pendant 2 minutes
- **ZeroIACircuitBreakerOpen** : Circuit breaker ouvert
- **ZeroIAHighProcessingTime** : Temps traitement > 5s

#### Alertes AssistantIA
- **AssistantIAHighResponseTime** : Temps réponse > 10s
- **AssistantIAHighSecurityBlocks** : > 10 blocages/min
- **AssistantIARateLimitExceeded** : Rate limit dépassé
- **AssistantIAModelError** : Erreur modèle détectée

#### Alertes Sécurité
- **SecurityHighBlockRate** : > 20 blocages/min
- **SecurityRateLimitViolation** : Violation rate limit
- **SecurityAuthenticationFailure** : Échec authentification
- **SecurityAuthorizationFailure** : Échec autorisation

---

## 🔧 Configuration

### Variables d'Environnement
```bash
# Monitoring
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000
ALERTMANAGER_PORT=9093
LOKI_PORT=3100
CADVISOR_PORT=8080

# Grafana
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=arkalia-secure-2025

# Prometheus
PROMETHEUS_RETENTION_DAYS=30
PROMETHEUS_SCRAPE_INTERVAL=15s

# AlertManager
ALERTMANAGER_SMTP_HOST=smtp.gmail.com
ALERTMANAGER_SMTP_PORT=587
ALERTMANAGER_SMTP_USER=alerts@arkalia-luna.com
ALERTMANAGER_SMTP_PASSWORD=secure-password
```

### Configuration Prometheus
```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "rules/*.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets: ["alertmanager:9093"]

scrape_configs:
  - job_name: 'arkalia-api (port 8000)'
    static_configs:
      - targets: ['host.docker.internal:8000']
    metrics_path: '/metrics'
    scrape_interval: 15s
```

### Configuration AlertManager
```yaml
# alertmanager.yml
global:
  smtp_smarthost: 'smtp.gmail.com:587'
  smtp_from: 'alerts@arkalia-luna.com'
  smtp_auth_username: 'alerts@arkalia-luna.com'
  smtp_auth_password: 'secure-password'

route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'arkalia-alerts'

receivers:
  - name: 'arkalia-alerts'
    email_configs:
      - to: 'admin@arkalia-luna.com'
```

---

## 🛠️ Maintenance

### Logs
```bash
# Logs Prometheus
docker logs prometheus

# Logs Grafana
docker logs grafana

# Logs AlertManager
docker logs alertmanager

# Logs Loki
docker logs loki

# Logs cAdvisor
docker logs cadvisor
```

### Sauvegarde
```bash
# Sauvegarder les configurations
docker cp prometheus:/etc/prometheus ./backup/prometheus/
docker cp grafana:/etc/grafana ./backup/grafana/
docker cp alertmanager:/etc/alertmanager ./backup/alertmanager/

# Sauvegarder les données
docker cp prometheus:/prometheus ./backup/prometheus-data/
docker cp grafana:/var/lib/grafana ./backup/grafana-data/
```

### Mise à Jour
```bash
# Arrêter les services
cd infrastructure/monitoring
docker-compose -f docker-compose.monitoring.yml down

# Mettre à jour les images
docker-compose -f docker-compose.monitoring.yml pull

# Redémarrer
docker-compose -f docker-compose.monitoring.yml up -d
```

### Nettoyage
```bash
# Nettoyer les anciennes données
docker volume prune

# Nettoyer les logs
docker system prune -f

# Redémarrer proprement
cd infrastructure/monitoring
docker-compose -f docker-compose.monitoring.yml down
docker-compose -f docker-compose.monitoring.yml up -d
```

---

## 🔍 Troubleshooting

### Problèmes Courants

#### Prometheus ne scrape pas les métriques
```bash
# Vérifier la connectivité
curl http://localhost:8000/metrics

# Vérifier la configuration
docker exec prometheus cat /etc/prometheus/prometheus.yml

# Redémarrer Prometheus
docker restart prometheus
```

#### Grafana ne se connecte pas
```bash
# Vérifier les logs
docker logs grafana

# Réinitialiser le mot de passe
docker exec grafana grafana-cli admin reset-admin-password arkalia-secure-2025

# Redémarrer Grafana
docker restart grafana
```

#### Alertes ne fonctionnent pas
```bash
# Vérifier AlertManager
curl http://localhost:9093/api/v1/alerts

# Vérifier les règles Prometheus
docker exec prometheus cat /etc/prometheus/rules/alerts.yml

# Redémarrer AlertManager
docker restart alertmanager
```

#### Métriques manquantes
```bash
# Vérifier l'API Arkalia
curl http://localhost:8000/status

# Vérifier les endpoints
curl http://localhost:8000/metrics | grep arkalia

# Redémarrer l'API
docker restart arkalia-api (port 8000)
```

---

## 📈 Métriques de Performance

### Objectifs SLO/SLI
- **Disponibilité** : 99.9% uptime
- **Latence** : P95 < 2s
- **Erreurs** : < 0.1% taux d'erreur
- **Throughput** : 1000+ req/min soutenus

### Métriques Clés
- **Temps de réponse** : < 2s (P95)
- **Disponibilité** : 99.9%+
- **Latence système** : < 100ms
- **Recovery Time** : < 100ms automatique
- **Error Rate** : < 0.1% (warnings seulement)

---

## 🎯 Roadmap Future

### v2.8.1 - Monitoring Avancé
- [ ] Métriques business (KPI)
- [ ] Alertes par email/Slack
- [ ] Dashboards personnalisables
- [ ] Machine learning pour prédiction

### v3.0.0 - Observabilité Complète
- [ ] Distributed tracing
- [ ] APM (Application Performance Monitoring)
- [ ] SLO/SLI définis
- [ ] Chaos engineering

---

## 📝 Commandes Utiles

### Validation
```bash
# Validation complète
python scripts/ark-validate-monitoring.py

# Vérification services
docker-compose -f infrastructure/monitoring/docker-compose.monitoring.yml ps

# Test métriques
curl http://localhost:8000/metrics
```

### Monitoring
```bash
# Statut services
docker ps | grep monitoring

# Logs temps réel
docker-compose -f infrastructure/monitoring/docker-compose.monitoring.yml logs -f

# Métriques système
curl http://localhost:9090/api/v1/query?query=up
```

### Maintenance
```bash
# Redémarrer monitoring
cd infrastructure/monitoring
docker-compose -f docker-compose.monitoring.yml restart

# Nettoyer
docker system prune -f

# Sauvegarder
./scripts/ark-backup-monitoring.sh
```

---

💡 **Le monitoring Arkalia-LUNA v2.8.0 offre une observabilité totale avec 34 métriques, 8 dashboards et 15 alertes pour garantir la fiabilité et les performances du système IA.**
