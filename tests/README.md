# 🧪 Tests Arkalia-LUNA v2.8.0

## 📁 Structure des Tests

```
tests/
├── common/                    # Utilitaires partagés
│   ├── __init__.py
│   ├── helpers.py            # Helpers pour tous les tests
│   └── fixtures.py           # Fixtures communes
├── unit/                     # Tests unitaires par module
│   ├── assistantia/          # Tests AssistantIA
│   ├── zeroia/              # Tests ZeroIA
│   ├── reflexia/            # Tests ReflexIA
│   ├── sandozia/            # Tests Sandozia
│   ├── cognitive_reactor/   # Tests Cognitive Reactor
│   ├── generative_ai/       # Tests Generative AI
│   ├── security/            # Tests de sécurité
│   └── ...                  # Autres modules
├── integration/             # Tests d'intégration
│   ├── modules/             # Tests d'intégration des modules
│   ├── scripts/             # Tests d'intégration des scripts
│   └── api/                 # Tests d'intégration API
├── performance/             # Tests de performance
│   ├── zeroia/             # Performance ZeroIA
│   ├── assistantia/        # Performance AssistantIA
│   └── reflexia/           # Performance ReflexIA
├── security/               # Tests de sécurité
│   ├── assistantia/        # Sécurité AssistantIA
│   ├── zeroia/            # Sécurité ZeroIA
│   └── general/           # Sécurité générale
├── chaos/                  # Tests de chaos et résilience
│   ├── common.py          # Classes communes
│   ├── filesystem/        # Tests chaos système de fichiers
│   ├── system/            # Tests chaos système
│   ├── network/           # Tests chaos réseau
│   └── state/             # Tests chaos état
├── core/                   # Tests du core système
├── base/                   # Tests de base
├── matrix/                 # Tests de matrices
├── scripts/                # Tests des scripts
└── conftest.py            # Configuration pytest
```

## 🚀 Commandes de Test

### Tests Unitaires
```bash
# Tous les tests unitaires
pytest tests/unit/

# Tests d'un module spécifique
pytest tests/unit/zeroia/
pytest tests/unit/assistantia/

# Tests avec couverture
pytest --cov=modules tests/unit/
```

### Tests d'Intégration
```bash
# Tous les tests d'intégration
pytest tests/integration/

# Tests d'intégration des modules
pytest tests/integration/modules/

# Tests d'intégration API
pytest tests/integration/api/
```

### Tests de Performance
```bash
# Tous les tests de performance
pytest tests/performance/

# Tests de performance ZeroIA
pytest tests/performance/zeroia/

# Tests de performance avec métriques
pytest tests/performance/ --benchmark-only
```

### Tests de Sécurité
```bash
# Tous les tests de sécurité
pytest tests/security/

# Tests de sécurité AssistantIA
pytest tests/security/assistantia/

# Tests de sécurité générale
pytest tests/security/general/
```

### Tests de Chaos
```bash
# Tous les tests de chaos
pytest tests/chaos/

# Tests de chaos système de fichiers
pytest tests/chaos/filesystem/

# Tests de chaos système
pytest tests/chaos/system/
```

## 📊 Métriques et Rapports

### Couverture de Code
```bash
# Rapport HTML de couverture
pytest --cov=modules --cov-report=html tests/
open htmlcov/index.html

# Rapport terminal
pytest --cov=modules --cov-report=term-missing tests/
```

### Performance
```bash
# Benchmark complet
python scripts/ark-performance-benchmark.py

# Tests de performance rapides
pytest tests/performance/ -v -m performance
```

## 🔧 Configuration

### Fixtures Communes
Les fixtures communes sont définies dans `tests/common/fixtures.py` :
- `test_data_dir` : Répertoire temporaire pour les données
- `mock_config` : Configuration de test standard
- `setup_test_environment` : Setup automatique
- `clean_state_files` : Nettoyage des fichiers d'état

### Helpers Partagés
Les helpers partagés sont dans `tests/common/helpers.py` :
- `ensure_test_toml()` : Crée un fichier TOML de test
- `ensure_zeroia_state_file()` : Crée un fichier d'état ZeroIA

## 🧪 Bonnes Pratiques

### Organisation des Tests
1. **Tests unitaires** : Un fichier par module dans `tests/unit/`
2. **Tests d'intégration** : Par domaine dans `tests/integration/`
3. **Tests de performance** : Par module dans `tests/performance/`
4. **Tests de sécurité** : Par module dans `tests/security/`
5. **Tests de chaos** : Par type de chaos dans `tests/chaos/`

### Naming Convention
- Fichiers de test : `test_*.py`
- Classes de test : `Test*`
- Méthodes de test : `test_*`
- Fixtures : `*_fixture`

### Isolation des Tests
- Chaque test doit être indépendant
- Utiliser les fixtures pour le setup/teardown
- Nettoyer les ressources après les tests
- Éviter les dépendances entre tests

## 🔍 Debug et Maintenance

### Debug des Tests
```bash
# Mode verbose
pytest -v tests/

# Mode debug avec print
pytest -s tests/

# Debug d'un test spécifique
pytest tests/unit/zeroia/test_specific.py::test_function -v -s
```

### Nettoyage
```bash
# Nettoyer les fichiers temporaires
find tests/ -name "*.pyc" -delete
find tests/ -name "__pycache__" -type d -exec rm -rf {} +

# Nettoyer les rapports
rm -rf htmlcov/
rm -rf .pytest_cache/
```

## 📈 Statistiques

- **Total des tests** : ~104 fichiers
- **Lignes de code** : ~10,347 lignes
- **Couverture actuelle** : ~10% (à améliorer)
- **Modules testés** : 16 modules principaux

## 🎯 Objectifs d'Amélioration

1. **Augmenter la couverture** à 80% minimum
2. **Ajouter des tests de performance** pour tous les modules critiques
3. **Renforcer les tests de sécurité** avec plus de cas d'usage
4. **Étendre les tests de chaos** pour une meilleure résilience
5. **Automatiser les tests** dans la CI/CD 