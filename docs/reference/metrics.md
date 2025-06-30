# 📊 Métriques Arkalia-LUNA Pro

## 🎯 Vue d'ensemble

Cette page documente toutes les métriques Prometheus exposées par Arkalia-LUNA Pro v2.8.0.

---

## 📈 **Métriques Globales**

### **Statut des Métriques**
- **Total métriques** : 34
- **Modules couverts** : 6
- **Métriques système** : 8
- **Métriques sécurité** : 6
- **Métriques performance** : 14

---

## 🌐 **API Principale (Helloria) - 34 métriques**

### **Métriques Système**
```prometheus
# CPU Usage
arkalia_cpu_usage_percent{module="helloria"} 45.2

# Memory Usage
arkalia_memory_usage_bytes{module="helloria"} 1073741824
arkalia_memory_usage_percent{module="helloria"} 67.8

# Disk Usage
arkalia_disk_usage_bytes{module="helloria"} 5368709120
arkalia_disk_usage_percent{module="helloria"} 23.1

# Network I/O
arkalia_network_bytes_sent_total{module="helloria"} 1024000
arkalia_network_bytes_received_total{module="helloria"} 2048000

# Uptime
arkalia_uptime_seconds{module="helloria"} 172800
```

### **Métriques API**
```prometheus
# HTTP Requests
arkalia_http_requests_total{module="helloria",method="GET",endpoint="/health"} 1234
arkalia_http_requests_total{module="helloria",method="POST",endpoint="/api/chat"} 567

# Request Duration
arkalia_http_request_duration_seconds{module="helloria",quantile="0.5"} 0.1
arkalia_http_request_duration_seconds{module="helloria",quantile="0.95"} 0.5
arkalia_http_request_duration_seconds{module="helloria",quantile="0.99"} 1.0

# HTTP Status Codes
arkalia_http_responses_total{module="helloria",status_code="200"} 1100
arkalia_http_responses_total{module="helloria",status_code="400"} 50
arkalia_http_responses_total{module="helloria",status_code="500"} 10

# Active Connections
arkalia_active_connections{module="helloria"} 5
```

### **Métriques Modules**
```prometheus
# Module Status
arkalia_module_status{module="helloria"} 1
arkalia_module_status{module="zeroia"} 1
arkalia_module_status{module="reflexia"} 1
arkalia_module_status{module="sandozia"} 1
arkalia_module_status{module="cognitive_reactor"} 1
arkalia_module_status{module="assistantia"} 1

# Module Performance
arkalia_module_response_time_seconds{module="helloria"} 0.05
arkalia_module_response_time_seconds{module="zeroia"} 0.2
arkalia_module_response_time_seconds{module="reflexia"} 0.1
arkalia_module_response_time_seconds{module="sandozia"} 0.3
arkalia_module_response_time_seconds{module="cognitive_reactor"} 0.15
arkalia_module_response_time_seconds{module="assistantia"} 0.8
```

### **Métriques Sécurité**
```prometheus
# Security Events
arkalia_security_events_total{module="helloria",event_type="blocked_request"} 25
arkalia_security_events_total{module="helloria",event_type="rate_limit"} 10
arkalia_security_events_total{module="helloria",event_type="invalid_token"} 5

# Rate Limiting
arkalia_rate_limit_hits_total{module="helloria"} 15
arkalia_rate_limit_remaining{module="helloria"} 985

# Authentication
arkalia_auth_failures_total{module="helloria"} 3
arkalia_auth_successes_total{module="helloria"} 1200
```

---

## 🧠 **ZeroIA - 12 métriques**

### **Métriques de Décision**
```prometheus
# Decisions Made
zeroia_decisions_total{decision_type="automatic"} 150
zeroia_decisions_total{decision_type="manual"} 25

# Decision Confidence
zeroia_decision_confidence{decision_id="dec_001"} 0.85
zeroia_decision_confidence{decision_id="dec_002"} 0.92

# Decision Response Time
zeroia_decision_response_time_seconds{quantile="0.5"} 0.1
zeroia_decision_response_time_seconds{quantile="0.95"} 0.3
```

### **Métriques de Patterns**
```prometheus
# Patterns Detected
zeroia_patterns_detected_total{pattern_type="cpu_spike"} 5
zeroia_patterns_detected_total{pattern_type="memory_leak"} 2
zeroia_patterns_detected_total{pattern_type="network_anomaly"} 3

# Pattern Confidence
zeroia_pattern_confidence{pattern_id="pat_001"} 0.9
zeroia_pattern_confidence{pattern_id="pat_002"} 0.75

# Contradictions
zeroia_cognitive_contradictions_total 1
```

---

## 👁️ **Reflexia - 8 métriques**

### **Métriques de Monitoring**
```prometheus
# System Monitoring
reflexia_system_cpu_usage_percent 45.2
reflexia_system_memory_usage_percent 67.8
reflexia_system_disk_usage_percent 23.1

# Network Monitoring
reflexia_network_io_bytes_sent_total 1024000
reflexia_network_io_bytes_received_total 2048000

# Observations
reflexia_observations_total{observation_type="anomaly"} 8
reflexia_observations_total{observation_type="normal"} 120

# Monitoring Latency
reflexia_monitoring_latency_seconds 0.05
```

---

## 🔍 **Sandozia - 6 métriques**

### **Métriques d'Analyse**
```prometheus
# Analysis Requests
sandozia_analysis_requests_total{analysis_type="pattern"} 45
sandozia_analysis_requests_total{analysis_type="anomaly"} 12

# Analysis Confidence
sandozia_analysis_confidence{analysis_id="ana_001"} 0.88
sandozia_analysis_confidence{analysis_id="ana_002"} 0.92

# Patterns Found
sandozia_patterns_found_total 15

# Analysis Response Time
sandozia_analysis_response_time_seconds{quantile="0.5"} 0.2
sandozia_analysis_response_time_seconds{quantile="0.95"} 0.8
```

---

## 🎯 **Cognitive Reactor - 4 métriques**

### **Métriques d'Orchestration**
```prometheus
# Orchestration Status
cognitive_reactor_orchestration_status 1

# Modules Coordinated
cognitive_reactor_modules_coordinated 6

# Patterns Managed
cognitive_reactor_patterns_managed 12

# Optimizations Applied
cognitive_reactor_optimizations_applied 3
```

---

## 🤖 **AssistantIA - 4 métriques**

### **Métriques d'Assistant**
```prometheus
# Chat Requests
assistantia_chat_requests_total 89

# Response Time
assistantia_response_time_seconds{quantile="0.5"} 0.5
assistantia_response_time_seconds{quantile="0.95"} 2.0

# Prompt Validation
assistantia_prompts_validated_total{validation_result="valid"} 85
assistantia_prompts_validated_total{validation_result="invalid"} 4

# Security Blocks
assistantia_security_blocks_total 2
```

---

## 📊 **Dashboards Grafana**

### **Dashboard Principal**
- **URL** : http://localhost:3000/d/arkalia-monitoring
- **Panels** : 8 panels spécialisés
- **Refresh** : 30 secondes
- **Thème** : Dark mode

### **Panels Disponibles**
1. **Système CPU & Mémoire**
2. **Statut des modules Arkalia**
3. **Requêtes API en temps réel**
4. **Durée des requêtes (P50/P95)**
5. **ZeroIA - Confiance & Décisions**
6. **AssistantIA - Prompts & Réponses**
7. **Reflexia - Monitoring Système**
8. **Erreurs & Alertes**

---

## 🚨 **Alertes Prometheus**

### **Règles d'Alertes**
```yaml
# CPU Usage High
- alert: HighCPUUsage
  expr: arkalia_cpu_usage_percent > 80
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "High CPU usage detected"

# Memory Usage High
- alert: HighMemoryUsage
  expr: arkalia_memory_usage_percent > 85
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "High memory usage detected"

# Module Down
- alert: ModuleDown
  expr: arkalia_module_status == 0
  for: 1m
  labels:
    severity: critical
  annotations:
    summary: "Module {{ $labels.module }} is down"

# High Response Time
- alert: HighResponseTime
  expr: arkalia_http_request_duration_seconds{quantile="0.95"} > 2
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "High response time detected"
```

---

## 🔧 **Configuration Prometheus**

### **Targets Configuration**
```yaml
scrape_configs:
  - job_name: 'arkalia-api (port 8000)'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
    scrape_interval: 15s

  - job_name: 'zeroia'
    static_configs:
      - targets: ['localhost:8001']
    metrics_path: '/metrics'
    scrape_interval: 15s

  - job_name: 'reflexia'
    static_configs:
      - targets: ['localhost:8002']
    metrics_path: '/metrics'
    scrape_interval: 15s

  - job_name: 'sandozia'
    static_configs:
      - targets: ['localhost:8003']
    metrics_path: '/metrics'
    scrape_interval: 15s

  - job_name: 'cognitive-reactor'
    static_configs:
      - targets: ['localhost:8004']
    metrics_path: '/metrics'
    scrape_interval: 15s

  - job_name: 'assistantia'
    static_configs:
      - targets: ['localhost:8005']
    metrics_path: '/metrics'
    scrape_interval: 15s
```

---

## 📈 **Requêtes PromQL Utiles**

### **Requêtes de Base**
```promql
# CPU Usage moyen
avg(arkalia_cpu_usage_percent)

# Memory Usage moyen
avg(arkalia_memory_usage_percent)

# Requests par seconde
rate(arkalia_http_requests_total[5m])

# Response time 95th percentile
histogram_quantile(0.95, rate(arkalia_http_request_duration_seconds_bucket[5m]))

# Module status
arkalia_module_status
```

### **Requêtes Avancées**
```promql
# Error rate
rate(arkalia_http_responses_total{status_code=~"5.."}[5m]) / rate(arkalia_http_responses_total[5m])

# ZeroIA decision confidence
avg(zeroia_decision_confidence)

# Security events rate
rate(arkalia_security_events_total[5m])
```

---

## 📚 **Documentation Complète**

- [🔗 Endpoints API](endpoints.md)
- [📖 API Documentation](api.md)
- [🔧 Configuration](../infrastructure/configuration.md)
- [📊 Monitoring](../infrastructure/monitoring.md)

---

**Arkalia-LUNA Pro v2.8.0** - Documentation des métriques Prometheus
**Dernière mise à jour** : 30 juin 2025
