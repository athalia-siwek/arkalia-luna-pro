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
