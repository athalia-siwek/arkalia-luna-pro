# 🔗 Endpoints API Arkalia-LUNA Pro

## 🎯 Vue d'ensemble

Cette page documente tous les endpoints API disponibles dans Arkalia-LUNA Pro v2.8.1.

---

## 🌐 **API Principale (Helloria)**

### **Base URL**

```
http://localhost:8000
```

### **Endpoints Principaux**

#### **GET /** - Page d'accueil

```http
GET /
```

**Description** : Page d'accueil de l'API
**Réponse** : HTML de la page d'accueil

#### **GET /health** - Health Check

```http
GET /health
```

**Description** : Vérification de l'état de santé
**Réponse** :

```json
{
  "status": "healthy",
  "timestamp": "2025-06-30T21:10:00Z",
  "version": "2.8.1"
}
```

#### **GET /status** - Statut détaillé

```http
GET /status
```

**Description** : Statut détaillé de tous les modules
**Réponse** :

```json
{
  "overall_status": "good",
  "components": {
    "arkalia_api": "healthy",
    "zeroia": "healthy",
    "reflexia": "healthy",
    "sandozia": "healthy",
    "cognitive_reactor": "healthy",
    "assistantia": "healthy"
  },
  "metrics": {
    "total_requests": 1234,
    "active_connections": 5,
    "uptime": "2d 5h 30m"
  }
}
```

#### **GET /metrics** - Métriques Prometheus

```http
GET /metrics
```

**Description** : Métriques au format Prometheus
**Réponse** : Métriques au format Prometheus

---

## 🧠 **ZeroIA - Décisionneur Autonome**

### **Base URL**

```
http://localhost:8001
```

### **Endpoints**

#### **POST /decide** - Prise de décision

```http
POST /decide
Content-Type: application/json

{
  "context": "string",
  "options": ["option1", "option2"],
  "confidence_threshold": 0.8
}
```

**Réponse** :

```json
{
  "decision": "option1",
  "confidence": 0.85,
  "reasoning": "string",
  "timestamp": "2025-06-30T21:10:00Z"
}
```

#### **GET /patterns** - Patterns comportementaux

```http
GET /patterns
```

**Réponse** :

```json
{
  "patterns": [
    {
      "id": "pattern_1",
      "name": "High CPU Usage",
      "confidence": 0.9,
      "last_seen": "2025-06-30T21:10:00Z"
    }
  ]
}
```

---

## 👁️ **Reflexia - Observateur Cognitif**

### **Base URL**

```
http://localhost:8002
```

### **Endpoints**

#### **GET /monitor** - Monitoring système

```http
GET /monitor
```

**Réponse** :

```json
{
  "system": {
    "cpu_usage": 45.2,
    "memory_usage": 67.8,
    "disk_usage": 23.1,
    "network_io": {
      "bytes_sent": 1024000,
      "bytes_recv": 2048000
    }
  },
  "timestamp": "2025-06-30T21:10:00Z"
}
```

#### **GET /observations** - Observations cognitives

```http
GET /observations
```

**Réponse** :

```json
{
  "observations": [
    {
      "id": "obs_1",
      "type": "anomaly",
      "severity": "medium",
      "description": "Unusual CPU pattern detected",
      "timestamp": "2025-06-30T21:10:00Z"
    }
  ]
}
```

---

## 🔍 **Sandozia - Intelligence Croisée**

### **Base URL**

```
http://localhost:8003
```

### **Endpoints**

#### **POST /analyze** - Analyse croisée

```http
POST /analyze
Content-Type: application/json

{
  "data": "string",
  "context": "string",
  "analysis_type": "pattern"
}
```

**Réponse** :

```json
{
  "analysis": {
    "result": "string",
    "confidence": 0.85,
    "patterns_found": 3,
    "recommendations": ["rec1", "rec2"]
  },
  "timestamp": "2025-06-30T21:10:00Z"
}
```

---

## 🎯 **Cognitive Reactor - Orchestrateur Central**

### **Base URL**

```
http://localhost:8004
```

### **Endpoints**

#### **GET /orchestration** - État de l'orchestration

```http
GET /orchestration
```

**Réponse** :

```json
{
  "orchestration": {
    "status": "active",
    "modules_coordinated": 6,
    "patterns_managed": 12,
    "optimizations_applied": 3
  },
  "timestamp": "2025-06-30T21:10:00Z"
}
```

---

## 🤖 **AssistantIA - Assistant IA**

### **Base URL**

```
http://localhost:8005
```

### **Endpoints**

#### **POST /chat** - Conversation IA

```http
POST /chat
Content-Type: application/json

{
  "message": "string",
  "context": "string",
  "user_id": "string"
}
```

**Réponse** :

```json
{
  "response": "string",
  "confidence": 0.9,
  "suggestions": ["suggestion1", "suggestion2"],
  "timestamp": "2025-06-30T21:10:00Z"
}
```

#### **POST /validate** - Validation de prompt

```http
POST /validate
Content-Type: application/json

{
  "prompt": "string",
  "user_id": "string"
}
```

**Réponse** :

```json
{
  "valid": true,
  "risk_level": "low",
  "warnings": [],
  "timestamp": "2025-06-30T21:10:00Z"
}
```

---

## 📊 **Monitoring - Métriques**

### **Prometheus**

```
http://localhost:9090/metrics
```

### **Grafana**

```
http://localhost:3000
```

### **AlertManager**

```
http://localhost:9093
```

### **Loki (Logs)**

```
http://localhost:3100
```

---

## 🔒 **Sécurité**

### **Authentification**

Tous les endpoints sensibles nécessitent une authentification via header :

```http
Authorization: Bearer <token>
```

### **Rate Limiting**

- **Limite** : 1000 requêtes par minute par IP
- **Headers** : `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

### **CORS**

```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
```

---

## 📝 **Codes de Réponse**

| Code | Description |
|------|-------------|
| 200 | Succès |
| 201 | Créé |
| 400 | Requête invalide |
| 401 | Non autorisé |
| 403 | Interdit |
| 404 | Non trouvé |
| 429 | Trop de requêtes |
| 500 | Erreur serveur |

---

## 🔧 **Exemples d'Utilisation**

### **cURL - Health Check**

```bash
curl -X GET http://localhost:8000/health
```

### **cURL - Décision ZeroIA**

```bash
curl -X POST http://localhost:8001/decide \
  -H "Content-Type: application/json" \
  -d '{
    "context": "High CPU usage detected",
    "options": ["scale_up", "optimize", "ignore"],
    "confidence_threshold": 0.8
  }'
```

### **cURL - Chat AssistantIA**

```bash
curl -X POST http://localhost:8005/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the current system status?",
    "context": "system_monitoring",
    "user_id": "admin"
  }'
```

---

## 📚 **Documentation Complète**

- [📖 API Documentation](api.md)
- [📊 Métriques](metrics.md)
- [🔧 Configuration](../infrastructure/configuration.md)

---

**Arkalia-LUNA Pro v2.8.1** - Documentation des endpoints API
**Dernière mise à jour** : 30 juin 2025
