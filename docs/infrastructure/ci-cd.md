# 🧑‍💻 Intégration Continue & Qualité — Arkalia-LUNA

![Version](https://img.shields.io/badge/version-v2.4.0-blue)
![CI](https://github.com/athalia-siwek/arkalia-luna-pro/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-Proprietary-red)
![Coverage](https://img.shields.io/badge/coverage-93%25-brightgreen)

Arkalia suit une philosophie de **code propre**, **tests exhaustifs** et **automatisation CI/CD** complète via GitHub Actions.

---

## ✅ Tests & couverture

- **Framework** : `pytest`
- **Couverture** : `pytest-cov`
- **Rapport** : `htmlcov/index.html`

📊 **Couverture actuelle** : **100 %** validée en CI.

---

## ✅ Linting & pré-commit

| Outil     | Rôle                                      |
|-----------|-------------------------------------------|
| `black`   | Formatage PEP8 automatique                |
| `ruff`    | Lint rapide et strict                     |
| `pre-commit` | Bloque les commits si le code n'est pas conforme |

💡 *Chaque `git commit` déclenche une vérification complète.*

---

## ✅ CI/CD — GitHub Actions

> Pipeline professionnel automatisé sur chaque `push`, `PR` ou `release`.

### 🔄 Étapes exécutées (`.github/workflows/ci.yml`)

| Étape           | Description                                          |
|------------------|------------------------------------------------------|
| 🔍 **Lint**      | `black`, `ruff`                                      |
| 🧪 **Tests**     | `pytest`, génération couverture HTML                 |
| 📚 **Docs**      | Build `mkdocs`, déploiement GitHub Pages             |
| 🧹 **Nettoyage** | Optionnel : purge des caches, artefacts              |

---

## 🧑‍💻 Automatisation CLI

Commandes utiles :

```bash
ark-test        # Lance tests + couverture
ark-docs        # Génère et ouvre la doc MkDocs
ark-docker      # Lance l'API dans un conteneur local
ark-clean-push  # Formate, vérifie, commit propre
```

---

💡 *Cette intégration continue assure une qualité constante et une livraison rapide des fonctionnalités.*

---

© 2025 **Athalia** – Tous droits réservés.
🤖 Powered by Arkalia ReflexIA `v1.x`

```markdown
# 🧪 Intégration Continue & Qualité — Arkalia-LUNA

Arkalia suit une philosophie de **code propre**, **tests exhaustifs** et **automatisation CI/CD** complète via GitHub Actions.

---

## ✅ Tests & couverture

- Framework : `pytest`
- Couverture : `pytest-cov`
- Rapport : `htmlcov/index.html`

📈 Couverture actuelle : **100 %** validée en CI.

---

## ✅ Linting & pré-commit

| Outil     | Rôle                                      |
|-----------|-------------------------------------------|
| `black`   | Formatage PEP8 automatique                |
| `ruff`    | Lint rapide et strict                     |
| `pre-commit` | Bloque les commits si le code n'est pas conforme |

💡 *Chaque `git commit` déclenche une vérification complète.*

---

## ✅ CI/CD — GitHub Actions

> Pipeline professionnel automatisé sur chaque `push`, `PR` ou `release`.

### 🔄 Étapes exécutées (`.github/workflows/ci.yml`)

| Étape           | Description                                          |
|------------------|------------------------------------------------------|
| 🔍 **Lint**      | `black`, `ruff`                                      |
| 🧪 **Tests**     | `pytest`, génération couverture HTML                 |
| 📘 **Docs**      | Build `mkdocs`, déploiement GitHub Pages             |
| 🧼 **Nettoyage** | Optionnel : purge des caches, artefacts              |

---

## 🧠 Automatisation CLI

Commandes utiles :

```bash
ark-test        # Lance tests + couverture
ark-docs        # Génère et ouvre la doc MkDocs
ark-docker      # Lance l'API dans un conteneur local
ark-clean-push  # Formate, vérifie, commit propre
