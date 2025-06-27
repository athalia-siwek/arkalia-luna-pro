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
