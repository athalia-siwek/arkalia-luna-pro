# ✨ ENHANCEMENTS.md — Améliorations Arkalia-LUNA

[![Version](https://img.shields.io/badge/version-v1.2.1-blue)](https://github.com/athalia-siwek/arkalia-luna-pro/releases)
[![Build](https://github.com/athalia-siwek/arkalia-luna-pro/actions/workflows/ci.yml/badge.svg)](https://github.com/athalia-siwek/arkalia-luna-pro/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-mkdocs-blueviolet)](https://athalia-siwek.github.io/arkalia-luna-pro/)

Fichier de suivi des améliorations techniques et qualité pour le dépôt [`arkalia-luna-pro`](https://github.com/athalia-siwek/arkalia-luna-pro).

🗓️ Dernière mise à jour : **2025-06-19** — Version : `v1.2.1`

---

## 🧱 Structure du Dépôt

- [x] Modules IA isolés dans `modules/<nom>/`
- [x] Structure standard par module : `core.py`, `config/`, `state/`, `logs/`, `tests/`, `utils/`
- [x] `README.md` professionnel avec badges
- [x] `CHANGELOG.md` versionné
- [x] Dossier `docs/` avec `mkdocs.yml` actif
- [ ] Ajouter `CONTRIBUTING.md` clair pour les PR
- [ ] Ajouter `SECURITY.md` explicite
- [ ] Ajouter `CODE_OF_CONDUCT.md` (community standard)

---

## 🧪 Qualité du Code

- [x] Lint `ruff` actif (CI + pre-commit)
- [x] Formatage `black` actif
- [x] `pre-commit` automatisé
- [x] Tests `pytest` actifs dans `/tests`
- [x] Badge de couverture (CI) à ajouter
- [ ] Étendre les tests `core.py` et `reflexia/`
- [ ] Couverture > 90 % sur tous les modules

---

## 🔧 Automatisations GitHub (CI/CD)

- [x] `.github/workflows/ci.yml` avec `black`, `ruff`, `pytest`
- [x] CI testée localement avec `act`
- [x] Génération `sitemap.xml` via `mkdocs-simple-hooks`
- [ ] Ajouter `release-please` pour les versions automatisées
- [ ] Ajouter `ark-init.sh` (post-install setup)
- [ ] Badges `coverage`, `release` à compléter

---

## 🧠 Documentation (MkDocs)

- [x] `docs/index.md`, `mkdocs.yml` opérationnels
- [x] Déploiement GitHub Pages fonctionnel
- [x] Sitemap intégré
- [x] Cartographie interactive (Mermaid) des modules
- [ ] Ajouter exemples CLI / API (usage intelligent)
- [ ] Ajouter encadrés visuels (ArkaliaBox, footer personnalisé)

---

## 📦 Packaging & Distribution

- [x] `pyproject.toml` propre et versionné
- [x] `bumpver` actif pour versions propres
- [ ] Compléter `pyproject.toml` (métadonnées pro)
- [ ] Rendre le dépôt installable (`pip install .`)
- [ ] Ajouter `setup.cfg` (optionnel pour distutils)

---

## 🛡️ Sécurité & Conformité

- [ ] `SECURITY.md` + procédure de signalement
- [ ] Ajouter `safety` ou `pip-audit` (CI scan vulnérabilités)
- [ ] Ajouter `git-secrets` ou équivalent dans `pre-commit`

---

## 🧩 Suggestions Modules à venir

- [x] `Nyxalia` → Interface mobile / vocale
- [x] `Reflexia` → Superviseur réflexif IA
- [ ] `Psykalia` → Analyse émotionnelle & signaux cognitifs
- [ ] `Logaria` → Analyseur de logs en temps réel
- [ ] `Chronalia` → Planification / priorisation IA
- [ ] `Sandozia` → Sécurité interne & backups IA

---

*© Athalia — Arkalia System, 2025*
