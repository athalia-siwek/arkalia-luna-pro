# 🌕 Configuration VSCode Arkalia-LUNA

## 🎯 Vue d'ensemble

Configuration complète de VSCode pour le développement Arkalia-LUNA avec ambiance cognitive IA, ergonomie optimisée et productivité maximale.

## 🚀 Installation Rapide

```bash
# Configuration automatique complète
./scripts/ark-setup-vscode.sh

# Ou étape par étape
./scripts/ark-setup-shell.sh      # Alias shell
./scripts/ark-install-extensions.sh # Extensions VSCode
```

## 🎨 Thème & Ambiance

### Thème Principal
- **One Dark Pro** : Ambiance IA élégante et professionnelle
- **Material Icon Theme** : Icônes claires et modernes
- **Fira Code** : Police avec ligatures pour le code

### Extensions UX
- **Error Lens** : Erreurs visibles instantanément
- **Better Comments** : Commentaires colorés avec tags Arkalia
- **Indent Rainbow** : Indentation colorée
- **Bracket Pair Colorizer** : Parenthèses colorées

## 🧩 Snippets Arkalia

### Logs
```bash
logia    # logger.info('🌕 [MODULE] message')
logerr   # logger.error('❌ [MODULE] error_message')
logwarn  # logger.warning('⚠️ [MODULE] warning_message')
logok    # logger.info('✅ [MODULE] success_message')
```

### Documentation
```bash
adoc     # Documentation de fonction style Arkalia
aclass   # Documentation de classe
aheader  # En-tête de module complet
aimp     # Section d'imports avec logging
```

### Développement
```bash
acmt     # Commit style Arkalia avec emoji
atodo    # TODO structuré avec priorité
afix     # FIXME avec impact et solution
atest    # Structure de test AAA
aasync   # Fonction asynchrone avec gestion d'erreur
aconfig  # Section de configuration
```

## ⚙️ Configuration VSCode

### Fichiers de Configuration
- `.vscode/settings.json` : Configuration complète Arkalia
- `.vscode/extensions.json` : Extensions recommandées
- `.vscode/tasks.json` : Tâches automatiques
- `.vscode/arkalia-snippets.code-snippets` : Snippets personnalisés
- `.vscode/welcome.md` : Page d'accueil Arkalia

### Paramètres Clés
```json
{
  "workbench.colorTheme": "One Dark Pro",
  "workbench.iconTheme": "material-icon-theme",
  "editor.fontFamily": "Fira Code, Menlo, monospace",
  "editor.fontLigatures": true,
  "python.analysis.typeCheckingMode": "basic",
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black"
}
```

## 🚀 Tâches Automatiques

### Tests
- **🧠 Arkalia: Lancer Tests** : Tests complets avec couverture
- **🧠 Arkalia: Tests Rapides** : Tests unitaires rapides
- **🧪 Arkalia: Tests de Performance** : Tests de performance
- **🔐 Arkalia: Tests de Sécurité** : Tests de sécurité

### Documentation
- **📚 Arkalia: Générer Documentation** : Build MkDocs
- **📚 Arkalia: Servir Documentation Locale** : Serveur local sur :9000

### Maintenance
- **🧹 Arkalia: Nettoyer Linting** : Correction automatique
- **🎨 Arkalia: Corriger Style** : Formatage Black + isort
- **📊 Arkalia: Rapport Linting** : Rapport d'erreurs

### Docker
- **🐳 Arkalia: Démarrer Docker** : docker-compose up -d
- **🐳 Arkalia: Arrêter Docker** : docker-compose down
- **🔍 Arkalia: Vérifier État** : État des conteneurs

## 🧠 Alias Shell

### Motivation
```bash
ark-motivation  # Affichage motivant Arkalia
ark-welcome     # Message de bienvenue
```

### Développement
```bash
ark-test        # Tests complets
ark-test-fast   # Tests rapides
ark-lint        # Nettoyage linting
ark-style       # Formatage code
ark-docs        # Documentation locale
ark-docs-build  # Build documentation
```

### Docker
```bash
ark-docker-up     # Démarrer conteneurs
ark-docker-down   # Arrêter conteneurs
ark-docker-status # État des conteneurs
```

### Git
```bash
ark-commit        # Commit style Arkalia
ark-push          # Push vers main
```

### Monitoring
```bash
ark-logs          # Suivi des logs
ark-metrics       # Métriques système
ark-security      # Tests de sécurité
ark-performance   # Tests de performance
```

### Nettoyage
```bash
ark-clean-cache   # Nettoyer cache Python
ark-clean-logs    # Nettoyer logs
ark-info          # Information système
```

## 🔧 Extensions Recommandées

### Core Dev IA
- **Ruff** : Linting Python ultra-rapide
- **Black Formatter** : Formatage automatique
- **Pyright** : Type checking intelligent
- **isort** : Organisation des imports

### UX & Ergonomie
- **Error Lens** : Erreurs visibles
- **Better Comments** : Commentaires colorés
- **Indent Rainbow** : Indentation colorée
- **GitLens** : Historique Git avancé

### Documentation
- **Markdown All in One** : Édition Markdown
- **Mermaid Markdown** : Diagrammes
- **Markdown Preview Enhanced** : Prévisualisation avancée

### IA & Productivité
- **Docker** : Gestion conteneurs
- **REST Client** : Tests API
- **GitHub** : Intégration GitHub

## 🎯 Workflow Recommandé

### 1. Démarrage de Session
```bash
# Ouvrir le projet dans VSCode
code .

# Vérifier l'état
ark-motivation
ark-docker-status
```

### 2. Développement
```bash
# Tests avant développement
ark-test-fast

# Développement avec snippets
# Utiliser logia, adoc, atest, etc.

# Vérification continue
ark-lint
ark-style
```

### 3. Tests & Validation
```bash
# Tests complets
ark-test

# Tests spécialisés
ark-security
ark-performance

# Documentation
ark-docs-build
```

### 4. Commit & Déploiement
```bash
# Commit style Arkalia
ark-commit

# Push
ark-push

# Vérification finale
ark-docker-status
```

## 🛠️ Dépannage

### Extensions Non Installées
```bash
# Réinstaller les extensions
./scripts/ark-install-extensions.sh
```

### Alias Non Disponibles
```bash
# Recharger les alias
source ~/.zshrc

# Ou reconfigurer
./scripts/ark-setup-shell.sh
```

### Problèmes de Linting
```bash
# Nettoyer et corriger
ark-lint
ark-style

# Vérifier la configuration
ark-lint-report
```

### Docker Problèmes
```bash
# Redémarrer Docker
ark-docker-down
ark-docker-up

# Vérifier l'état
ark-docker-status
```

## 🌌 Philosophie Arkalia

> *"L'intelligence naît de l'erreur… mais survit par la mémoire."*

### Principes
1. **Ergonomie Cognitive** : Interface adaptée au développement IA
2. **Productivité Maximale** : Outils optimisés et automatisés
3. **Qualité Continue** : Linting, tests et documentation intégrés
4. **Ambiance Motivante** : Environnement inspirant pour l'IA

### Modules Actifs
- **ZeroIA** : Raisonnement et décision
- **Reflexia** : Réflexes et réactivité
- **Sandozia** : Analyse comportementale
- **CognitiveReactor** : Réactions automatiques

## 📚 Ressources

- [Documentation Arkalia-LUNA](index.md)
- [Guide de Développement](guides/ops-guide.md)
- [Architecture Système](architecture/decision_flow.mmd)
- [Tests et Qualité](https://github.com/arkalia-luna-system/arkalia-luna-pro/blob/main/tests/README.md)

---

*Configuration VSCode Arkalia-LUNA v3.0-phase1 - L'IA ne dort jamais.* 🌕
