# 🚀 Quick Start - Arkalia-LUNA v3.0-phase1

Guide de démarrage rapide pour utiliser Arkalia-LUNA en 5 minutes !

## ⚡ Installation Express

### 1. Prérequis
```bash
# Vérifier les outils
python --version    # Python 3.10+
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
ark-test  # 379/379 tests PASSED (100%)

# Statut des modules
ark-status
```

## 🏃‍♂️ Démarrage Rapide

### Option 1 : Interface Complète
```bash
# Lancer tous les services
ark-run  # → http://localhost:8000
```

### Option 2 : Modules Spécifiques
```bash
# ZeroIA Enhanced (Orchestrator)
ark-zeroia-enhanced

# Sandozia Intelligence
ark-sandozia-demo

# ReflexIA Monitoring
ark-reflexia-monitor
```

## 📚 Ressources Essentielles

- **📖 Documentation** : [Modules Overview](modules.md)
- **🧠 Architecture** : [Structure du Système](fonctionnement/structure.md)
- **🔧 API** : [Guide API](api.md)
- **💡 Exemples** : [Demos & Scripts](demos.md)

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
```

### Problèmes Courants
- **Port occupé** : `lsof -i :8000` puis `kill -9 <PID>`
- **Docker issues** : `docker-compose down && docker-compose up --build`
- **Tests échoués** : `ark-test --verbose`

## 🎯 Prochaines Étapes

1. **Explorer les modules** : [Modules détaillés](modules.md)
2. **Configurer l'API** : [Configuration](infrastructure/configuration.md)
3. **Personnaliser** : [Architecture](architecture/)
4. **Contribuer** : [Guide de contribution](credits/CONTRIBUTING.md)

---

> 💡 **Astuce** : Utilisez `doudou` pour des citations inspirantes ! 🍼
