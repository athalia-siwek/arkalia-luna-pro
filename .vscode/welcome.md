# 🌕 Bienvenue dans Arkalia-LUNA v3.x

## 🚀 Démarrage Rapide

### Commandes Essentielles
- **🧪 Tests** : `Ctrl+Shift+P` → "Tasks: Run Task" → "🧪 Run Tests"
- **🎨 Formatage** : `Ctrl+Shift+P` → "Tasks: Run Task" → "🎨 Black Format"
- **🔍 Linting** : `Ctrl+Shift+P` → "Tasks: Run Task" → "🔍 Lint Ruff"
- **🚀 API** : `F5` → "🚀 Run Arkalia API"

### Raccourcis Clavier
- `Ctrl+Shift+P` : Palette de commandes
- `Ctrl+Shift+E` : Explorateur de fichiers
- `Ctrl+Shift+G` : Git
- `Ctrl+Shift+X` : Extensions
- `Ctrl+Shift+D` : Débogage

## 📁 Structure du Projet

```
arkalia-luna-pro/
├── modules/           # Modules IA principaux
│   ├── zeroia/       # Système de raisonnement
│   ├── reflexia/     # Réflexion cognitive
│   ├── sandozia/     # Intelligence croisée
│   └── helloria/     # API FastAPI
├── tests/            # Tests unitaires et intégration
├── scripts/          # Scripts utilitaires
├── docs/             # Documentation MkDocs
└── state/            # États persistants
```

## 🧠 Modules IA

### ZeroIA - Système de Raisonnement
- **Fichier principal** : `modules/zeroia/reason_loop_enhanced.py`
- **État** : `state/zeroia_state.toml`
- **Tests** : `tests/unit/zeroia/`

### Reflexia - Réflexion Cognitive
- **Fichier principal** : `modules/reflexia/core.py`
- **État** : `state/reflexia_state.toml`
- **Tests** : `tests/unit/reflexia/`

### Sandozia - Intelligence Croisée
- **Fichier principal** : `modules/sandozia/core/sandozia_core.py`
- **État** : `state/sandozia/latest_metrics.json`
- **Tests** : `tests/unit/sandozia/`

### Helloria - API FastAPI
- **Fichier principal** : `helloria/core.py`
- **Port** : `8000`
- **Documentation** : `http://localhost:8000/docs`

## 🛠️ Outils de Développement

### Formatage et Linting
- **Black** : Formatage automatique du code
- **Ruff** : Linting rapide et moderne
- **Mypy** : Vérification de types statiques
- **isort** : Organisation des imports

### Tests
- **pytest** : Framework de tests
- **coverage** : Couverture de code
- **chaos** : Tests de résilience

### Documentation
- **MkDocs** : Documentation statique
- **Material Theme** : Interface moderne
- **GitHub Pages** : Déploiement automatique

## 🐳 Docker

### Services Disponibles
- **zeroia** : Module de raisonnement
- **reflexia** : Module de réflexion
- **sandozia** : Module d'intelligence croisée
- **helloria** : API FastAPI

### Commandes Docker
```bash
# Démarrer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter tous les services
docker-compose down
```

## 📊 Monitoring

### Métriques Prometheus
- **Endpoint** : `http://localhost:8000/metrics`
- **Grafana** : `http://localhost:3000`
- **Prometheus** : `http://localhost:9090`

### Logs
- **Logs système** : `logs/arkalia_master.log`
- **Logs ZeroIA** : `logs/zeroia/`
- **Logs Reflexia** : `logs/reflexia/`

## 🔧 Configuration

### Variables d'Environnement
```bash
export ARKALIA_LUNA="/Volumes/T7/devstation/cursor/arkalia-luna-pro"
export ARKALIA_VENV="/Volumes/T7/arkalia-luna-venv"
export PYTHONPATH="$ARKALIA_LUNA/modules:$PYTHONPATH"
```

### Extensions Recommandées
- **Python** : Support Python complet
- **Pylance** : IntelliSense avancé
- **Ruff** : Linting rapide
- **Black Formatter** : Formatage automatique
- **GitLens** : Git avancé
- **Material Icon Theme** : Icônes modernes

## 🎯 Bonnes Pratiques

### Code
- Utiliser les snippets personnalisés (`zeroia-loop`, `circuit`, etc.)
- Respecter la limite de 88 caractères (Black)
- Ajouter des annotations de type
- Documenter les fonctions complexes

### Tests
- Écrire des tests pour chaque nouvelle fonctionnalité
- Utiliser des fixtures pytest
- Maintenir une couverture > 80%

### Git
- Commits atomiques et descriptifs
- Utiliser les conventions de commit
- Branches feature pour les nouvelles fonctionnalités

## 🆘 Support

### Ressources
- **Documentation** : `https://athalia-siwek.github.io/arkalia-luna-pro`
- **GitHub** : `https://github.com/arkalia-luna-system/arkalia-luna-pro`
- **Issues** : `https://github.com/arkalia-luna-system/arkalia-luna-pro/issues`

### Commandes de Diagnostic
```bash
# Vérifier l'état du système
ark-status

# Nettoyer le projet
ark-clean

# Relancer VSCode
ark-vscode-reload
```

---

**🌕 Arkalia-LUNA - Industrial AI Core v3.x**
*Kernel IA ultra-protection active* ✅
