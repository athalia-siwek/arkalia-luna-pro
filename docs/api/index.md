# API Documentation

Documentation de l'API REST d'Arkalia-LUNA.

## Vue d'ensemble

Pour consulter la documentation complète de l'API, voir [Documentation API](../api.md).

## Endpoints Principaux

### 🤖 AssistantIA API
```
POST /api/v1/chat
GET  /api/v1/status
```

### 🔄 Reflexia API
```
POST /api/v1/reflexia/analyze
GET  /api/v1/reflexia/metrics
```

### 🧠 Sandozia API
```
GET  /api/v1/sandozia/intelligence
POST /api/v1/sandozia/validate
```

### 🧪 ZeroIA API
```
GET  /api/v1/zeroia/status
POST /api/v1/zeroia/check
```

## Authentification

L'API utilise des tokens JWT pour l'authentification.

## Rate Limiting

- 100 requêtes/minute par défaut
- 1000 requêtes/minute pour les comptes premium

[📖 Documentation API Complète →](../api.md)
