# 📋 CHANGELOG.md — Historique des versions Arkalia-LUNA

Ce fichier retrace les changements apportés à chaque version publique d'Arkalia-LUNA.

## [helloria-v1.0.0] — 2025-06-19

### ✅ Ajouts
- Endpoint `GET /` pour ping racine (`core.py`)
- Endpoint `GET /status` pour état opérationnel (`core.py`)
- Gestion d'état via `HelloriaStateManager` (`state.py`)
- Ajout de `main.py` pour exécution directe via Uvicorn
- Test unitaire minimal (`test_helloria.py`)

### ♻️ Refactoring
- Nettoyage et normalisation via `black` et `ruff`

### 📄 Documentation
- `README.md` : objectif, routes, exemple de requête, lien vers MkDocs

🔁 **Couverture test :** 100 % sur `test_helloria.py`  
🔗 **Documentation :** [https://athalia-siwek.github.io/arkalia-luna-pro/modules](https://athalia-siwek.github.io/arkalia-luna-pro/modules)

---

## [0.1.2] - 2025-06-18
### Ajouté
- ENHANCEMENTS.md avec roadmap d'amélioration IA
- CONTRIBUTING.md avec règles de contribution
- Badges pro dans README

## [0.1.1] - 2025-06-17
### Initialisation
- Dépôt GitHub mis en ligne
- README.md structuré
- Pre-commit activé (`black`, `ruff`)
