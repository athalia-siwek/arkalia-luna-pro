# 🚀 Workflows GitHub Actions - Arkalia-LUNA Pro

## 📋 Vue d'ensemble

Cette section contient tous les workflows GitHub Actions professionnels pour Arkalia-LUNA Pro, conçus pour une CI/CD robuste, sécurisée et scalable.

## 🔧 Workflows Disponibles

### 1. 🚀 `ci.yml` - Pipeline CI Principal

**Objectif** : Pipeline de CI complet avec tests, linting, sécurité et couverture.

**Fonctionnalités** :
- ✅ Linting et formatage (black, isort, ruff, mypy)
- ✅ Tests unitaires avec couverture (pytest + coverage)
- ✅ Tests d'intégration
- ✅ Tests de sécurité (bandit, safety)
- ✅ Tests de performance (pytest-benchmark)
- ✅ Tests de chaos
- ✅ Cache des dépendances
- ✅ Timeouts configurables
- ✅ Rapports détaillés

**Déclencheurs** :
- Push sur `main`, `develop`, `dev-migration`, `refonte-stable`
- Pull requests sur les mêmes branches

**Jobs** :
- `lint` : Vérification du code (10 min timeout)
- `test` : Tests unitaires et intégration (30 min timeout)
- `security` : Tests de sécurité (15 min timeout)
- `performance` : Tests de performance (20 min timeout, nightly)
- `chaos` : Tests de chaos (25 min timeout, nightly)
- `report` : Rapport final (10 min timeout)

### 2. 🧪 `e2e.yml` - Tests End-to-End

**Objectif** : Tests E2E complets avec Docker et tests de charge.

**Fonctionnalités** :
- ✅ Construction et démarrage des services Docker
- ✅ Health checks avec retry
- ✅ Tests E2E avec pytest
- ✅ Tests de charge avec Locust
- ✅ Cache Docker layers
- ✅ Nettoyage automatique

**Déclencheurs** :
- Push sur `main`, `develop`, `dev-migration`
- Pull requests sur les mêmes branches

**Jobs** :
- `e2e-tests` : Tests E2E complets (45 min timeout)
- `load-tests` : Tests de charge (30 min timeout)
- `e2e-report` : Rapport final (10 min timeout)

### 3. 🚀 `deploy.yml` - Pipeline de Déploiement

**Objectif** : Déploiement automatique avec validation et rollback.

**Fonctionnalités** :
- ✅ Validation pré-déploiement
- ✅ Construction Docker avec cache
- ✅ Tests E2E post-build
- ✅ Déploiement staging/production
- ✅ Health checks post-déploiement
- ✅ Rollback automatique
- ✅ Smoke tests

**Déclencheurs** :
- Push sur `main`, `develop`, `dev-migration`
- Pull requests sur les mêmes branches

**Jobs** :
- `pre-deploy-validation` : Validation (15 min timeout)
- `build` : Construction Docker (30 min timeout)
- `e2e` : Tests E2E post-build (45 min timeout)
- `deploy-staging` : Déploiement staging (20 min timeout)
- `deploy-production` : Déploiement production (30 min timeout)
- `rollback` : Rollback automatique (15 min timeout)
- `deployment-report` : Rapport final (10 min timeout)

### 4. 📘 `docs.yml` - Déploiement Documentation

**Objectif** : Construction et déploiement automatique de la documentation.

**Fonctionnalités** :
- ✅ Validation de la configuration MkDocs
- ✅ Construction de la documentation
- ✅ Déploiement GitHub Pages
- ✅ Health checks de la documentation
- ✅ Validation des fichiers Markdown

**Déclencheurs** :
- Push sur `main`, `dev-migration`, `refonte-stable`
- Pull requests sur les mêmes branches

**Jobs** :
- `validate-docs` : Validation (10 min timeout)
- `build-docs` : Construction (15 min timeout)
- `deploy-docs` : Déploiement (10 min timeout)
- `docs-report` : Rapport final (5 min timeout)

### 5. 🚀 `performance-tests.yml` - Tests de Performance

**Objectif** : Tests de performance avancés avec métriques détaillées.

**Fonctionnalités** :
- ✅ Tests de performance ZeroIA, API, intégration
- ✅ Tests de charge avec Locust
- ✅ Métriques système et Docker
- ✅ Tests de régression
- ✅ Alertes automatiques

**Déclencheurs** :
- Push sur `main`, `develop`, `dev-migration`
- Pull requests sur les mêmes branches
- Schedule quotidien à 2h du matin

**Jobs** :
- `performance-tests` : Tests de performance (45 min timeout)
- `performance-analysis` : Analyse des résultats (15 min timeout)
- `regression-tests` : Tests de régression (20 min timeout)

## 🔧 Configuration et Variables

### Variables d'Environnement

```yaml
# Python
PYTHON_VERSION: "3.10"

# Docker
DOCKER_REGISTRY: "ghcr.io"
DOCKER_BUILDKIT: 1
COMPOSE_DOCKER_CLI_BUILD: 1

# Couverture
COVERAGE_MIN: 28
SECURITY_COVERAGE_MIN: 10
PERFORMANCE_COVERAGE_MIN: 10
CHAOS_COVERAGE_MIN: 10

# Timeouts
TEST_TIMEOUT: 1800  # 30 minutes
BUILD_TIMEOUT: 900  # 15 minutes
```

### Permissions

```yaml
permissions:
  contents: read
  packages: write
  security-events: write
  actions: read
  pages: write
  id-token: write
```

## 🛡️ Sécurité

### Bonnes Pratiques Implémentées

1. **Permissions minimales** : Chaque workflow utilise les permissions minimales nécessaires
2. **Scan de sécurité** : Bandit et Safety pour détecter les vulnérabilités
3. **Validation des dépendances** : Vérification des vulnérabilités des packages
4. **Cache sécurisé** : Cache des dépendances avec validation
5. **Timeouts** : Évite les jobs bloqués
6. **Rollback automatique** : En cas d'échec de déploiement

### Outils de Sécurité

- **Bandit** : Scan de vulnérabilités Python
- **Safety** : Vérification des dépendances
- **Ruff** : Linting avec règles de sécurité
- **Mypy** : Type checking

## 📊 Monitoring et Rapports

### Métriques Collectées

1. **Couverture de code** : Rapport détaillé par module
2. **Performance** : Temps de réponse, débit, latence
3. **Sécurité** : Vulnérabilités détectées
4. **Déploiement** : Statut des environnements
5. **Tests** : Résultats et tendances

### Artifacts Générés

- `test-results-*.xml` : Résultats des tests
- `coverage.xml` : Couverture de code
- `bandit-report.json` : Rapport de sécurité
- `performance-metrics-*.md` : Métriques de performance
- `load-test-report-*.html` : Rapports de charge
- `deployment-report.md` : Rapport de déploiement

## 🔄 Gestion des Erreurs

### Stratégies d'Erreur

1. **Retry automatique** : Health checks avec retry
2. **Fallback** : Tests avec avertissements au lieu d'échec
3. **Rollback** : Retour automatique en cas d'échec
4. **Notifications** : Alertes en cas de problème
5. **Logs détaillés** : Traçabilité complète

### Codes de Sortie

- `0` : Succès
- `1` : Échec critique
- `2` : Échec avec avertissements
- `3` : Timeout

## 🚀 Optimisations

### Performance

1. **Cache intelligent** : Cache pip, Docker, et dépendances
2. **Parallélisation** : Jobs en parallèle quand possible
3. **Matrix builds** : Tests sur plusieurs configurations
4. **Artifacts** : Partage entre jobs
5. **Timeouts** : Évite les jobs bloqués

### Coût

1. **Runners optimisés** : Ubuntu latest uniquement
2. **Cache efficace** : Réduction des téléchargements
3. **Nettoyage** : Suppression des artifacts anciens
4. **Scheduling** : Tests lourds en dehors des heures de pointe

## 📝 Maintenance

### Tâches Régulières

1. **Mise à jour des actions** : GitHub Actions v4+
2. **Révision des permissions** : Sécurité
3. **Optimisation des timeouts** : Performance
4. **Mise à jour des dépendances** : Sécurité
5. **Révision des seuils** : Couverture et performance

### Monitoring

1. **Temps d'exécution** : Optimisation continue
2. **Taux de succès** : Qualité des tests
3. **Utilisation des ressources** : Coût
4. **Alertes** : Réactivité

## 🔗 Intégrations

### Services Externes

- **Codecov** : Couverture de code
- **GitHub Pages** : Documentation
- **Docker Hub** : Images Docker
- **Slack** : Notifications (optionnel)
- **Email** : Alertes (optionnel)

### Secrets Requis

```yaml
# GitHub
GITHUB_TOKEN: # Automatique

# Codecov (optionnel)
CODECOV_TOKEN: # Pour rapports détaillés

# Notifications (optionnels)
SLACK_WEBHOOK: # Pour alertes Slack
EMAIL_NOTIFICATION: # Pour alertes email
```

## 📚 Ressources

### Documentation

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Buildx](https://docs.docker.com/buildx/)
- [MkDocs](https://www.mkdocs.org/)
- [Pytest](https://docs.pytest.org/)
- [Bandit](https://bandit.readthedocs.io/)

### Exemples

- [GitHub Actions Examples](https://github.com/actions/examples)
- [Docker Compose CI](https://docs.docker.com/compose/ci-cd/)
- [Python Testing](https://docs.python-guide.org/writing/tests/)

---

**Dernière mise à jour** : Janvier 2025
**Version** : 2.0.0
**Mainteneur** : Arkalia-LUNA Team
