# Changelog Minimal

## Nouveautés

### feat: Rollback
- Implémentation de la fonctionnalité de rollback pour ZeroIA.

### fix: Pre-push
- Correction des erreurs de pre-push pour assurer la stabilité du système.

### docs: Mise à jour de la documentation
- Ajout des pages `cognitive-levels.md` et `rebuild.md` dans la navigation officielle.

## Checklist des Modules Vérifiés
- ZeroIA
- ReflexIA
- Arkalia Monitor

## État CI/Docker/Tests
- **CI** : Toutes les vérifications passent sauf quelques lignes trop longues (E501).
- **Docker** : Tous les conteneurs sont actifs, sauf ZeroIA qui est "unhealthy".
- **Tests** : Tous les tests unitaires et d'intégration passent.

## Lien GitHub Pages
- [Documentation Arkalia-LUNA](https://github.com/arkalia-luna-system/arkalia-luna-pro)

# 📋 CHANGELOG.md — Historique des versions Arkalia-LUNA

Ce fichier retrace les évolutions majeures du système IA modulaire Arkalia-LUNA.

## [v2.1.2] — 2025-06-24

### ✅ Stabilisation du système complet (CI + Tests + Docs)
- 🧪 70 tests unitaires passés avec succès (pytest)
- 📊 Couverture globale : 93 % (htmlcov/index.html)
- 📁 Rapport HTML généré automatiquement

### 🧠 Modules actifs validés
- assistantia : IA locale avec Ollama
- reflexia : IA cognitive adaptative + monitoring
- helloria : FastAPI + points de contrôle
- nyxalia : passerelle externe (mobile/API)

### ⚙️ CI/CD et automatisation
- CI GitHub Actions totalement verte (black, ruff, pytest, mkdocs)
- Rebuild Docker : ✅ (ark-docker)
- Simulations locales via act : validées (ark-act)
- Alias actifs : ark-run, ark-test, ark-docs, ark-ci-check, ark-fixall

### 📘 Documentation
- ✅ Site MkDocs à jour : arkalia-luna-pro
- 🧭 Sitemap dynamique : /sitemap.xml
- 🎨 Style personnalisé (extra.css, favicon, Mermaid, collapsibles…)
- 📄 Pages clés enrichies : ci-cd.md, tests.md, modules.md, api.md

### 🧼 Nettoyage & Tags
- .gitignore optimisé (._*, .DS_Store, site/, etc.)
- Suppression de 15 tags Git inutiles
- Fichier reflexia_state.toml exclu et nettoyé

### 🧰 Bonus techniques
- sitemap_generator.py exécuté automatiquement
- test_sitemap.py ajouté (valide sitemap.xml)
- Lint 100 % clean (black, ruff, pre-commit)
- Version bump : v2.1.2

📦 État actuel : stable, publié, dockerisé, industrialisé.

---

## [helloria-v1.0.0] — 2025-06-19

### ✅ Fonctionnalités
- Endpoints `/`, `/status`, gestion état via `HelloriaStateManager`
- Exécution directe via `main.py`, tests unitaire `test_helloria.py`
- Couverture : 100 %

🔗 Modules Arkalia

---

## [v1.2.2] — 2025-06-20

### 🧠 Création de assistantia
- Endpoint `/chat`, IA locale avec Ollama
- Gestion des erreurs, prompt vide, modèles invalides
- 35 tests unitaires, couverture : 92 %
- Docker stable + CI verte

---

## [v1.0.6 → v1.1.x → v1.3.x] — Consolidation intermédiaire

### 🚀 Progressions notables (regroupées)
- Ajout de tous les fichiers pro (ENHANCEMENTS.md, CONTRIBUTING.md, SECURITY.md)
- Lint, CI/CD, couverture, tests, Docker validés
- Documentation MkDocs activée + stylée
- Sitemap + ci-cd.md enrichis

🟢 Plusieurs tags expérimentaux entre v1.0.6 et v1.3.4 ont été fusionnés ici pour clarté.

---

## [0.1.1 – 0.1.2] — Initialisation GitHub (2025-06-17/18)

### ✅ Structure de base
- Dépôt GitHub créé
- README propre
- pre-commit activé
- Premiers tests, première couverture CI
- Ajout roadmap (ENHANCEMENTS.md), badges pro

---

🧭 Prochaine étape : v2.2.0
➡️ Démarrage de la phase Nexus : ZeroIA, Psykalia, surcouche cognitive, IA réflexive complète.

## [v1.3.5] - 2025-06-24

### ✨ Améliorations majeures
- Relecture et réécriture complète de la documentation (`docs/*.md`)
- Normalisation de la syntaxe Markdown et des titres
- Ajout de visuels Mermaid interactifs (graphes et mindmaps)
- Uniformisation du style rédactionnel et structure des fichiers

### 🛠️ Technique
- Nettoyage des fichiers orphelins (`._*`)
- Mise à jour automatique du site via `mkdocs gh-deploy --force`

### 📚 Docs
- `assistantia.md`, `api.md`, `reflexia.md` restructurés
- `kernel.md`, `modules.md`, `automation.md` clarifiés
- Ajout d'exemples concrets dans `ollama.md`, `ci-cd.md`, `faqs.md`

---

## 🔖 v2.5.3 — CI verte + tests 100% (26 juin 2025)

### ✅ Nouveautés

- Ajout des scripts Fail2Ban (jail, filter, test)
- Intégration complète de ZeroIA (reason_loop, snapshot, orchestrator)
- Dockerfile sécurisés (cap_drop, no-new-privileges)
- Couverture de tests portée à 113 tests, 67 %
- Monitoring actif (Reflexia, dashboard, Prometheus config)
- Résolution des erreurs TOML invalides dans `snapshot_generator`
- Tests croisés ReflexIA ↔ ZeroIA : validés

### 🔐 Sécurité

- Mise en place d'une simulation de pare-feu avec bannissement automatique
- Tests automatisés : `fail2ban_test.sh` validé en CI
- Fichiers parasites `.DS_Store`, `._*` supprimés

### 📄 Documentation

- `docs/docker_hardening.md` ajouté
- `deployment/render_helloria.yml` préparé

### 🧪 CI/CD

- Tous les tests (`act` + GitHub Actions) passés
- pre-commit : `black`, `ruff`, EOF, trailing ✔️

> Version stable, dockerisée, supervisée, avec agents cognitifs coopérants.

---
