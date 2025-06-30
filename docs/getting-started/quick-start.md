# 🚀 Quick Start - Arkalia-LUNA v2.8.0

Guide de démarrage rapide pour utiliser Arkalia-LUNA en 5 minutes !

## ⚡ Installation Express

### 1. Prérequis
```bash
# Vérifier les outils
python --version    # Python 3.11+
docker --version    # Docker requis
git --version       # Git requis
```

### 2. Clone & Setup
```bash
# Clone du projet
git clone https://github.com/arkalia-luna-system/arkalia-luna-pro.git
cd arkalia-luna-pro

# Setup automatique
./ark-start.sh
```

### 3. Test Système
```bash
# Vérifier l'installation
ark-test  # 99.5% tests PASSED

# Statut des modules
ark-status
```

## 🏃‍♂️ Démarrage Rapide

### Option 1 : Interface Complète avec Monitoring
```bash
# Lancer tous les services
ark-run  # → http://localhost:8000

# Démarrer le monitoring
cd infrastructure/monitoring
docker-compose -f docker-compose.monitoring.yml up -d

# Valider l'installation
python scripts/ark-validate-monitoring.py
```

### Option 2 : Modules Spécifiques
```bash
# ZeroIA Enhanced (Orchestrator)
ark-zeroia-enhanced

# Sandozia Intelligence
ark-sandozia-demo

# Reflexia Monitoring
ark-reflexia-monitor

# Generative AI
ark-generative-ai-demo (désactivé)
```

## 📊 Services Monitoring

Une fois le monitoring démarré, accédez aux services :

| Service | URL | Description | Credentials |
|---------|-----|-------------|-------------|
| **Grafana** | http://localhost:3000 | Dashboards temps réel | admin / arkalia-secure-2025 |
| **Prometheus** | http://localhost:9090 | Métriques système | - |
| **AlertManager** | http://localhost:9093 | Gestion alertes | - |
| **Loki** | http://localhost:3100 | Centralisation logs | - |
| **cAdvisor** | http://localhost:8080 | Métriques conteneurs | - |
| **Arkalia API** | http://localhost:8000 | API principale + métriques | - |

### Validation Monitoring
```bash
# Validation complète
python scripts/ark-validate-monitoring.py

# Vérification services
docker-compose -f infrastructure/monitoring/docker-compose.monitoring.yml ps

# Métriques Arkalia
curl http://localhost:8000/metrics
```

## 📚 Ressources Essentielles

- **📖 Documentation** : [Modules Overview](../modules/index.md)
- **🧠 Architecture** : [Structure du Système](../fonctionnement/structure.md)
- **🔧 API** : [Guide API](../reference/api.md)
- **📊 Monitoring** : [Guide Monitoring](../infrastructure/monitoring.md)

## 🆘 Aide Rapide

### Commandes Essentielles
```bash
# Aide générale
ark-help

# Nettoyage
ark-clean

# Monitoring
ark-monitor

# Documentation locale
ark-docs-local  # → http://127.0.0.1:9000

# Validation monitoring
python scripts/ark-validate-monitoring.py
```

### Problèmes Courants
- **Port occupé** : `lsof -i :8000` puis `kill -9 <PID>`
- **Docker issues** : `docker-compose down && docker-compose up --build`
- **Tests échoués** : `ark-test --verbose`
- **Monitoring down** : `cd infrastructure/monitoring && docker-compose -f docker-compose.monitoring.yml restart`

### Monitoring Troubleshooting
```bash
# Vérifier les services
docker ps | grep monitoring

# Logs Prometheus
docker logs prometheus

# Logs Grafana
docker logs grafana

# Redémarrer monitoring
cd infrastructure/monitoring
docker-compose -f docker-compose.monitoring.yml down
docker-compose -f docker-compose.monitoring.yml up -d
```

## 🎯 Prochaines Étapes

1. **Explorer les modules** : [Modules détaillés](../modules/index.md)
2. **Configurer l'API** : [Configuration](../infrastructure/configuration.md)
3. **Personnaliser** : [Architecture](../fonctionnement/structure.md)
4. **Monitoring** : [Guide Monitoring](../infrastructure/monitoring.md)
5. **Contribuer** : [Guide de contribution](../credits/CONTRIBUTING.md)

## 📊 Métriques Disponibles

Le monitoring expose **34 métriques Arkalia** :

- **Système** : CPU, mémoire, disque, uptime
- **API** : requêtes, latence, erreurs, durée
- **Modules** : statut, performance, confiance
- **Sécurité** : blocages, rate limits, violations
- **ZeroIA** : décisions, confiance, contradictions
- **AssistantIA** : prompts, temps de réponse, sécurité
- **Reflexia** : monitoring système, latence

### Dashboard Principal
- **URL** : http://localhost:3000/d/arkalia-monitoring
- **Panels** : 8 panels spécialisés
- **Refresh** : 30 secondes
- **Thème** : Dark mode

---

> 💡 **Astuce** : Commencez par Grafana pour visualiser l'état complet du système ! 📊
