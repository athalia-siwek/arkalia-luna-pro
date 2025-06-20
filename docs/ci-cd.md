---

## ✅ FICHIER `ci-cd.md` — Version améliorée

# 🧪 Tests Automatiques

## Structure

- `tests/unit/` : fonctions isolées (modules, utils…)
- `tests/integration/` : endpoints, FastAPI, interactions
- `tests/scripts/` : vérif sitemap, auto-clean, etc.

## Commandes Utiles

- `ark-test` : tous les tests + coverage HTML
- `ark-test-modules` : focus sur `modules/`
- `pytest --cov=...` pour custom

## Couverture Actuelle

- ✅ 92 % au 20 juin 2025
- ✅ 35 tests passés

---

🧭 BONUS UX :
- Activer les collapsibles (details) dans api.md ou modules.md
- Ajouter liens internes entre les fichiers ([voir structure](structure.md))

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