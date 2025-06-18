# 🧪 Intégration Continue (CI) & Tests — Arkalia-LUNA

Arkalia-LUNA suit une discipline stricte de **testabilité** et de **qualité de code automatisée**, pour garantir un cycle de vie logiciel durable et sans dette technique.

---

## ✅ Couverture de Tests

- `pytest` + `pytest-cov`
- **Couverture actuelle : 100%**
- Rapport HTML généré automatiquement : `htmlcov/index.html`

---

## ✅ Linting & Qualité de Code

- `black` → Formatage automatique du code Python
- `ruff` → Analyse de code statique rapide
- `pre-commit` → Lancement automatique à chaque commit Git

💡 *Chaque commit est bloqué si le code est mal formaté ou comporte des erreurs non corrigées.*

---

## ✅ Pipeline CI/CD — GitHub Actions

> Le dépôt utilise **GitHub Actions** pour :

| Étape             | Description                                  |
|-------------------|----------------------------------------------|
| 🔍 `Lint`         | Vérifie tout le code (`ruff`, `black`)       |
| 🧪 `Tests`        | Lance `pytest`, génère couverture            |
| 📚 `Docs Deploy` | Déploie automatiquement la doc MkDocs vers GitHub Pages |

Fichier de workflow :
```bash
.github/workflows/ci.yml