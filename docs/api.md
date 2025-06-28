# 🌐 API Arkalia-LUNA v3.x — Enterprise REST

![Version](https://img.shields.io/badge/version-v3.0--phase2-blue)
![CI](https://github.com/athalia-siwek/arkalia-luna-pro/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-Proprietary-red)
![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen)

Bienvenue dans la documentation de l'**API REST Enterprise** d'Arkalia-LUNA v3.x, orchestrée par le module `Helloria` avec intelligence croisée `Sandozia`.

> L'API v3.x intègre la **validation intelligente cross-modules**, le **scoring de confiance** et les **métriques temps réel** pour une expérience enterprise robuste.

---

## 🚀 Endpoints Principaux v3.x

### `POST /api/v1/chat`

**Description :** Chat intelligent avec validation Sandozia automatique
```json
{
  "message": "Analyse l'état global du système Arkalia",
  "user_id": "athalia-enterprise",
  "context": "monitoring"
}
```

**Réponse avec Métadonnées v3.x :**
```json
{
  "response": "État système excellent - Score cohérence: 0.98",
  "confidence_score": 0.96,
  "sandozia_validation": {
    "coherence_score": 0.98,
    "behavioral_health": 0.94,
    "cross_validation": "PASSED"
  },
  "modules_status": {
    "reflexia": "active",
    "zeroia": "monitoring",
    "assistantia": "ready"
  },
  "timestamp": "2025-06-27T20:30:00Z"
}
```

**Test Enterprise :**
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <jwt-token>" \
  -d '{
    "message": "Status Sandozia Intelligence Croisée",
    "context": "admin"
  }'
```

### `GET /api/v1/status`

**Description :** État système enterprise avec métriques Sandozia
```json
{
  "status": "operational",
  "version": "v3.0-phase2",
  "modules": {
    "sandozia": "active",
    "reflexia": "active",
    "zeroia": "active",
    "assistantia": "active",
    "taskia": "active",
    "nyxalia": "active",
    "helloria": "active",
    "global_state": "synced"
  },
  "sandozia_metrics": {
    "global_score": 0.95,
    "coherence": 0.98,
    "behavioral_health": 0.94,
    "last_validation": "2025-06-27T20:29:45Z"
  },
  "performance": {
    "uptime": "99.9%",
    "avg_response_ms": 185,
    "requests_per_min": 847
  }
}
```

### `GET /api/v1/sandozia/intelligence`

**Description :** Snapshot intelligence croisée temps réel
```json
{
  "intelligence_snapshot": {
    "timestamp": "2025-06-27T20:30:00Z",
    "global_coherence": 0.98,
    "cross_correlations": {
      "reflexia_zeroia": 0.996,
      "assistantia_confidence": 0.94
    },
    "behavioral_patterns": [
      {
        "type": "decision_consistency",
        "score": 0.97,
        "trend": "stable"
      }
    ],
    "recommendations": [
      "Système opérationnel - Aucune action requise"
    ]
  }
}
```

### `POST /api/v1/sandozia/validate`

**Description :** Validation croisée manuelle
```json
{
  "validation_request": {
    "modules": ["reflexia", "zeroia", "assistantia"],
    "scope": "comprehensive"
  }
}
```

---

## 🔐 Authentification v3.x

### JWT Tokens
```bash
# Obtenir un token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -d '{"username": "admin", "password": "secure_pass"}'

# Utiliser le token
curl -H "Authorization: Bearer <jwt-token>" \
  http://localhost:8000/api/v1/status
```

### Rate Limiting
- **Free Tier :** 100 req/min
- **Enterprise :** 1000 req/min
- **Admin :** Illimité

---

## 🧪 Endpoints Développement

### `POST /api/v1/debug/echo`
Test de connectivité avec validation
```bash
curl -X POST http://localhost:8000/api/v1/debug/echo \
  -H "Content-Type: application/json" \
  -d '{"test": "sandozia_validation"}'
```

### `GET /api/v1/debug/modules`
État détaillé tous modules
```json
{
  "modules_debug": {
    "sandozia": {
      "status": "active",
      "last_intelligence_collection": "2025-06-27T20:29:30Z",
      "coherence_score": 0.98
    },
    "reflexia": {
      "status": "active",
      "decision_confidence": 0.95
    }
  }
}
```

---

## 📊 Métriques et Monitoring

### `GET /api/v1/metrics/prometheus`
Métriques Prometheus format
```
# HELP sandozia_coherence_score Score cohérence inter-modules
# TYPE sandozia_coherence_score gauge
sandozia_coherence_score 0.98

# HELP sandozia_behavioral_health Santé comportementale
# TYPE sandozia_behavioral_health gauge
sandozia_behavioral_health 0.94
```

### `GET /api/v1/metrics/dashboard`
Données dashboard temps réel
```json
{
  "dashboard_data": {
    "global_health": 0.95,
    "module_correlations": {
      "reflexia_zeroia": 0.996
    },
    "performance_metrics": {
      "avg_response_time": 185,
      "throughput": 847
    },
    "alerts": []
  }
}
```

---

## 🔍 WebSocket Temps Réel

### `/ws/sandozia/live`
Stream métriques intelligence croisée
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/sandozia/live');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Score cohérence:', data.coherence_score);
};
```

---

## 🛡️ Sécurité Enterprise

### Headers Requis
```
Content-Type: application/json
Authorization: Bearer <jwt-token>
X-API-Version: v3.0
X-Request-ID: <uuid>
```

### Protection
- 🔒 **HTTPS obligatoire** en production
- 🛡️ **Rate limiting** avec backoff exponential
- 🔐 **JWT avec expiration** (1h par défaut)
- 🚫 **CORS configuré** pour domaines autorisés

---

## 📚 SDKs et Intégrations

### Python SDK
```python
from arkalia_sdk import ArkaliaClient

client = ArkaliaClient(
    base_url="http://localhost:8000",
    token="jwt-token"
)

# Chat avec validation Sandozia
response = client.chat.send(
    message="Analyse système",
    context="monitoring"
)
print(f"Confiance: {response.confidence_score}")
```

### JavaScript SDK
```javascript
import { ArkaliaClient } from '@arkalia/sdk';

const client = new ArkaliaClient({
  baseUrl: 'http://localhost:8000',
  token: 'jwt-token'
});

const status = await client.status.get();
console.log(`Score Sandozia: ${status.sandozia_metrics.global_score}`);
```

---

## 🔧 Configuration Production

### Variables d'environnement
```bash
export ARKALIA_API_HOST=0.0.0.0
export ARKALIA_API_PORT=8000
export ARKALIA_JWT_SECRET=your-secret-key
export ARKALIA_SANDOZIA_ENABLED=true
export ARKALIA_MONITORING_ENABLED=true
```

### Docker Compose
```yaml
services:
  arkalia-api:
    image: arkalia-luna:v3.0
    ports:
      - "8000:8000"
    environment:
      - ARKALIA_SANDOZIA_ENABLED=true
    depends_on:
      - postgres
      - redis
```

---

## 📞 Support API

- **📖 Documentation Interactive :** `/api/v1/docs` (Swagger UI)
- **🔧 OpenAPI Schema :** `/api/v1/openapi.json`
- **📊 Health Check :** `/api/v1/health`
- **🧪 Status Page :** `ark-status`

---

**© 2025 Arkalia-LUNA Team** — API Enterprise v3.x
🌐 *Powered by Sandozia Intelligence Croisée + Helloria REST*

# 🌐 API Arkalia-LUNA Enhanced v2.7.1

Documentation complète de l'API REST d'Arkalia-LUNA Enhanced avec les **nouveaux endpoints Framework Enhanced**.

**Version API** : `v2.7.1-enhanced` | **Base URL** : `http://localhost:8000`

---

## 🚀 **Nouveautés Enhanced v2.7.1**

### ✅ **Endpoints Framework Enhanced**

#### 🎯 **Orchestrator Enhanced**
- `GET /api/v1/zeroia/orchestrator/status` - Status Orchestrator Enhanced
- `POST /api/v1/zeroia/orchestrator/run` - Exécution boucle Enhanced
- `GET /api/v1/zeroia/orchestrator/metrics` - Métriques performance

#### 🔒 **Circuit Breaker**
- `GET /api/v1/zeroia/circuit-breaker/status` - État circuit breaker
- `POST /api/v1/zeroia/circuit-breaker/reset` - Reset circuit breaker
- `GET /api/v1/zeroia/circuit-breaker/metrics` - Métriques protection

#### 📊 **Event Store Enhanced**
- `GET /api/v1/zeroia/events` - Liste événements récents
- `POST /api/v1/zeroia/events` - Ajout nouvel événement
- `GET /api/v1/zeroia/events/analytics` - Analytics Event Store
- `GET /api/v1/zeroia/events/recovery-status` - Status auto-recovery

#### 🛡️ **Error Recovery**
- `GET /api/v1/zeroia/error-recovery/status` - Status Error Recovery
- `POST /api/v1/zeroia/error-recovery/test` - Test récupération
- `GET /api/v1/zeroia/graceful-degradation/status` - Status degradation

---

## 🧪 **ZeroIA Enhanced API**

### 🚀 **Orchestrator Enhanced**

#### `GET /api/v1/zeroia/orchestrator/status`
Status détaillé de l'Orchestrator Enhanced.

**Response** :
```json
{
  "status": "operational",
  "version": "enhanced-v2.6.0",
  "current_state": "idle",
  "last_execution": {
    "timestamp": "2024-12-29T20:51:00Z",
    "loops_completed": 5,
    "success_rate": 100.0,
    "duration_seconds": 1.7,
    "failures": 0
  },
  "circuit_breaker": {
    "state": "CLOSED",
    "failure_count": 0,
    "last_failure": null
  },
  "event_store": {
    "total_events": 11,
    "cache_status": "healthy",
    "auto_recovery_active": true
  }
}
```

#### `POST /api/v1/zeroia/orchestrator/run`
Exécution de la boucle Orchestrator Enhanced.

**Request** :
```json
{
  "max_loops": 5,
  "interval_seconds": 0.3,
  "mode": "quick"
}
```

**Response** :
```json
{
  "execution_id": "exec_20241229_205100",
  "status": "completed",
  "results": {
    "loops_executed": 5,
    "success_rate": 100.0,
    "duration_seconds": 1.7,
    "decisions_made": 5,
    "events_created": 11,
    "circuit_breaker_openings": 0
  },
  "performance": {
    "avg_loop_time": 0.34,
    "min_loop_time": 0.31,
    "max_loop_time": 0.38
  }
}
```

### 🔒 **Circuit Breaker API**

#### `GET /api/v1/zeroia/circuit-breaker/status`
État détaillé du Circuit Breaker.

**Response** :
```json
{
  "state": "CLOSED",
  "failure_count": 0,
  "failure_threshold": 5,
  "timeout_seconds": 60,
  "success_threshold": 3,
  "last_failure_time": null,
  "last_success_time": "2024-12-29T20:51:00Z",
  "total_requests": 156,
  "successful_requests": 156,
  "failed_requests": 0,
  "success_rate": 100.0
}
```

### 📊 **Event Store Enhanced API**

#### `GET /api/v1/zeroia/events`
Liste des événements récents avec auto-recovery.

**Query Parameters** :
- `limit` : Nombre d'événements (défaut: 10)
- `event_type` : Filtrage par type d'événement

**Response** :
```json
{
  "events": [
    {
      "id": "evt_20241229_205100_001",
      "timestamp": "2024-12-29T20:51:00Z",
      "event_type": "DECISION_MADE",
      "data": {
        "decision": "normal",
        "confidence": 0.8,
        "reasoning": "System stable, no anomalies detected"
      },
      "metadata": {
        "source": "orchestrator_enhanced",
        "execution_id": "exec_20241229_205100"
      }
    }
  ],
  "total_count": 11,
  "cache_status": "healthy",
  "auto_recovery": {
    "enabled": true,
    "last_recovery": null,
    "recovery_count": 0
  }
}
```

#### `GET /api/v1/zeroia/events/analytics`
Analytics avancées de l'Event Store.

**Response** :
```json
{
  "summary": {
    "total_events": 11,
    "events_last_hour": 11,
    "events_last_24h": 11,
    "cache_size_mb": 0.049
  },
  "event_types": {
    "DECISION_MADE": 5,
    "SYSTEM_HEALTHY": 3,
    "CIRCUIT_BREAKER_CLOSED": 2,
    "ERROR_RECOVERY_SUCCESS": 1
  },
  "performance": {
    "avg_write_time_ms": 2.3,
    "avg_read_time_ms": 1.1,
    "cache_hit_rate": 0.85
  },
  "health": {
    "status": "excellent",
    "cache_corruption_count": 0,
    "auto_recovery_count": 0,
    "last_health_check": "2024-12-29T20:51:00Z"
  }
}
```

### 🛡️ **Error Recovery API**

#### `GET /api/v1/zeroia/error-recovery/status`
Status complet du système Error Recovery.

**Response** :
```json
{
  "status": "operational",
  "version": "enhanced-v2.7.1",
  "recovery_systems": {
    "sqlite_corruption": {
      "enabled": true,
      "status": "monitoring",
      "recoveries_performed": 0,
      "last_recovery": null
    },
    "cache_corruption": {
      "enabled": true,
      "status": "monitoring",
      "auto_cleanup": true,
      "cleanups_performed": 0
    },
    "typing_errors": {
      "enabled": true,
      "status": "resolved",
      "errors_fixed": 14,
      "last_fix": "2024-12-29T20:45:00Z"
    }
  },
  "graceful_degradation": {
    "enabled": true,
    "services_count": 15,
    "priority_levels": 5,
    "degraded_services": 0
  }
}
```

#### `GET /api/v1/zeroia/graceful-degradation/status`
Status détaillé du Graceful Degradation.

**Response** :
```json
{
  "status": "nominal",
  "services": {
    "critical": {
      "count": 3,
      "operational": 3,
      "services": ["system_monitoring", "error_recovery", "circuit_breaker"]
    },
    "high": {
      "count": 3,
      "operational": 3,
      "services": ["zeroia_core", "reflexia_core", "event_sourcing"]
    },
    "medium": {
      "count": 3,
      "operational": 3,
      "services": ["sandozia_intelligence", "assistantia_api", "prometheus_metrics"]
    },
    "low": {
      "count": 3,
      "operational": 3,
      "services": ["advanced_analytics", "ui_enhancements", "caching_layer"]
    },
    "optional": {
      "count": 3,
      "operational": 3,
      "services": ["debug_tools", "dev_utilities", "performance_profiling"]
    }
  },
  "degradation_level": "none",
  "last_degradation": null,
  "recovery_time_estimate": null
}
```

---

## 🧠 **Sandozia Intelligence API**

### 🔍 **CrossModule Validation**

#### `GET /api/v1/sandozia/validation/status`
Status validation croisée inter-modules.

**Response** :
```json
{
  "global_coherence_score": 0.98,
  "validations_performed": 156,
  "contradictions_detected": 0,
  "last_validation": "2024-12-29T20:51:00Z",
  "module_coherence": {
    "reflexia_zeroia": 0.99,
    "assistantia_sandozia": 0.97,
    "global_state_sync": 0.98
  }
}
```

### 📈 **Behavior Analysis**

#### `GET /api/v1/sandozia/behavior/analysis`
Analyse comportementale avancée.

**Response** :
```json
{
  "behavioral_health_score": 0.94,
  "anomalies_detected": 0,
  "patterns_analyzed": 45,
  "statistical_analysis": {
    "z_score_threshold": 2.0,
    "outliers_detected": 0,
    "trend_analysis": "stable"
  }
}
```

---

## 🔄 **Reflexia Decision API**

### 🎯 **Decision Engine**

#### `POST /api/v1/reflexia/decision`
Demande de décision au moteur Reflexia.

**Request** :
```json
{
  "context": {
    "system_status": "normal",
    "load": 0.45,
    "memory_usage": 0.62
  },
  "priority": "high",
  "timeout_seconds": 5
}
```

**Response** :
```json
{
  "decision": "monitor",
  "confidence": 0.85,
  "reasoning": "System metrics within normal range",
  "execution_time_ms": 234,
  "recommendations": [
    "Continue monitoring",
    "No immediate action required"
  ]
}
```

---

## 🤖 **AssistantIA Conversation API**

### 💬 **Chat Interface**

#### `POST /api/v1/assistantia/chat`
Interface de conversation avec l'assistant IA.

**Request** :
```json
{
  "message": "Comment va le système Arkalia ?",
  "conversation_id": "conv_20241229_205100",
  "model": "llama3.2",
  "context": {
    "include_system_status": true,
    "include_metrics": true
  }
}
```

**Response** :
```json
{
  "response": "Le système Arkalia-LUNA Enhanced v2.7.1 fonctionne parfaitement ! 🚀\n\n✅ Orchestrator Enhanced : 100% succès\n✅ Tests : 373/374 PASSED (99.7%)\n✅ Circuit Breaker : État fermé stable\n✅ Event Store : Auto-recovery opérationnel\n\nTous les modules sont opérationnels et les performances sont exceptionnelles !",
  "conversation_id": "conv_20241229_205100",
  "timestamp": "2024-12-29T20:51:00Z",
  "model_used": "llama3.2",
  "processing_time_ms": 1247,
  "system_context": {
    "orchestrator_status": "operational",
    "test_success_rate": 96.6,
    "circuit_breaker_state": "CLOSED"
  }
}
```

---

## 📊 **Monitoring & Metrics API**

### 🎯 **Global Health Check**

#### `GET /api/v1/health`
Health check global du système Enhanced.

**Response** :
```json
{
  "status": "healthy",
  "version": "enhanced-v2.7.1",
  "timestamp": "2024-12-29T20:51:00Z",
  "components": {
    "orchestrator_enhanced": "operational",
    "circuit_breaker": "closed",
    "event_store": "healthy",
    "error_recovery": "monitoring",
    "graceful_degradation": "nominal",
    "sandozia_intelligence": "excellent",
    "reflexia_engine": "operational",
    "assistantia": "ready",
    "api_gateway": "healthy"
  },
  "metrics": {
    "uptime_seconds": 172800,
    "total_requests": 15647,
    "success_rate": 99.98,
    "avg_response_time_ms": 145,
    "test_success_rate": 96.6
  }
}
```

### 📈 **Performance Metrics**

#### `GET /api/v1/metrics/performance`
Métriques de performance détaillées.

**Response** :
```json
{
  "orchestrator_enhanced": {
    "total_executions": 234,
    "success_rate": 100.0,
    "avg_execution_time": 1.7,
    "last_24h_executions": 45
  },
  "circuit_breaker": {
    "total_requests": 15647,
    "failed_requests": 0,
    "success_rate": 100.0,
    "state_changes": 0
  },
  "event_store": {
    "total_events": 1247,
    "events_per_hour": 52,
    "cache_hit_rate": 0.85,
    "auto_recoveries": 0
  },
  "api_performance": {
    "requests_per_minute": 234,
    "avg_response_time": 145,
    "p95_response_time": 287,
    "p99_response_time": 456
  }
}
```

---

## 🔐 **Authentication & Security**

### 🛡️ **API Key Authentication**

Toutes les requêtes API Enhanced nécessitent une authentification :

```bash
# Header requis
Authorization: Bearer <api_key>

# Exemple avec curl
curl -H "Authorization: Bearer ark_enhanced_v271_key" \
     http://localhost:8000/api/v1/zeroia/orchestrator/status
```

### 🔒 **Rate Limiting**

- **Standard** : 1000 req/min
- **Enhanced** : 5000 req/min
- **Monitoring** : 10000 req/min

---

## 🚀 **Exemples d'Utilisation**

### 🎯 **Test Complet Enhanced**

```bash
# Status global
curl http://localhost:8000/api/v1/health

# Exécution Orchestrator Enhanced
curl -X POST http://localhost:8000/api/v1/zeroia/orchestrator/run \
  -H "Content-Type: application/json" \
  -d '{"max_loops": 5, "mode": "quick"}'

# Vérification Circuit Breaker
curl http://localhost:8000/api/v1/zeroia/circuit-breaker/status

# Analytics Event Store
curl http://localhost:8000/api/v1/zeroia/events/analytics
```

### 🧠 **Intelligence Croisée**

```bash
# Validation cross-module
curl http://localhost:8000/api/v1/sandozia/validation/status

# Analyse comportementale
curl http://localhost:8000/api/v1/sandozia/behavior/analysis

# Conversation avec AssistantIA
curl -X POST http://localhost:8000/api/v1/assistantia/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Status du système Enhanced ?", "include_metrics": true}'
```

---

## 📚 **Documentation Interactive**

### 🌐 **OpenAPI/Swagger**

Documentation interactive disponible :
- **Swagger UI** : `http://localhost:8000/docs`
- **ReDoc** : `http://localhost:8000/redoc`
- **OpenAPI JSON** : `http://localhost:8000/openapi.json`

### 🔗 **Liens Utiles**

- **API Locale** : `http://localhost:8000`
- **Health Check** : `http://localhost:8000/api/v1/health`
- **Métriques** : `http://localhost:8000/api/v1/metrics/performance`
- **Documentation** : `http://localhost:8000/docs`

---

## 🏆 **Conclusion**

L'**API Arkalia-LUNA Enhanced v2.7.1** offre :

✅ **Framework Enhanced** - Orchestrator, Circuit Breaker, Event Store
✅ **Error Recovery** - Gestion gracieuse toutes erreurs
✅ **Intelligence Croisée** - Validation et consensus multi-modules
✅ **Performance Exceptionnelle** - 96.6% tests, 100% succès orchestrator
✅ **Documentation Complète** - OpenAPI/Swagger intégré

**🌟 Une API enterprise-ready pour l'IA de nouvelle génération !**
