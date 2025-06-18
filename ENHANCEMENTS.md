# ✨ ENHANCEMENTS.md — Améliorations Arkalia-LUNA

Fichier maintenu pour professionnaliser, optimiser et sécuriser le dépôt [`arkalia-luna-pro`](https://github.com/athalia-siwek/arkalia-luna-pro).

Dernière mise à jour : **2025-06-18**

---

## 🧱 Structure du Dépôt

- [x] Dossier `modules/<nom>/` isolé par fonction IA
- [x] Structure standardisée : `core.py`, `config/`, `state/`, `logs/`, `tests/`, `utils/`
- [x] `README.md` pro et structuré
- [ ] Ajouter `CONTRIBUTING.md` pour les règles de contribution
- [ ] Ajouter un `SECURITY.md` clair
- [ ] Ajouter `CODE_OF_CONDUCT.md` professionnel
- [ ] Dossier `docs/` avec doc indexée
- [ ] Ajouter un `CHANGELOG.md` par version

---

## 🧪 Qualité du Code

- [x] `black` actif via `pre-commit`
- [x] `ruff` actif pour le linting
- [x] `pre-commit` hook vérifié
- [ ] Activer `pytest` dans `/tests`
- [ ] Ajouter un badge de couverture (`coverage`)
- [ ] Ajouter des tests pour `core.py` et `reflexia/`

---

## 🔧 Automatisations GitHub

- [ ] Créer `.github/workflows/test.yml` avec :
  - `black`
  - `ruff`
  - `pytest`
- [ ] Badges CI/CD (`build`, `tests`, `release`)
- [ ] Release notes automatiques (`release-please`)
- [ ] Script de post-install (`ark-init.sh`)

---

## 🧠 Documentation

- [ ] Initier `docs/index.md` + `mkdocs.yml`
- [ ] Lier `mkdocs` à GitHub Pages (ou repo dédié)
- [ ] Ajouter des exemples d’usage CLI/API
- [ ] Cartographie des modules (diagramme Mermaid ou Markdown)

---

## 📦 Packaging & Distribution

- [x] `pyproject.toml` de base
- [ ] Compléter `pyproject.toml` (auteur, version, classifiers)
- [ ] Rendre le projet installable via `pip install .`
- [ ] Ajouter `bumpver` pour les versions clean
- [ ] Inclure un `setup.cfg` (optionnel)

---

## 🛡️ Sécurité & Conformité

- [ ] `SECURITY.md` avec procédure de signalement
- [ ] Script de vérification des dépendances (`safety`, `pip-audit`)
- [ ] Git secrets ou pre-commit secrets scan

---

## 🧩 Suggestions Modules

- [ ] `Nyxalia` → Interface externe (mobile / vocal)
- [ ] `Psykalia` → Module IA d’analyse émotionnelle
- [ ] `Logaria` → Superviseur de logs IA
- [ ] `Chronalia` → Gestion intelligente du temps et des priorités
- [ ] `Sandozia` → Sécurité système IA + sauvegardes

---

*© Athalia — Arkalia System, 2025*
