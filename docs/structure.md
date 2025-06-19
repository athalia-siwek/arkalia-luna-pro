# 🧬 Structure du Noyau — Arkalia-LUNA

> Arkalia-LUNA repose sur une architecture **modulaire, lisible, performante** et 100 % locale. Chaque composant est isolé, orchestrable et testable de manière indépendante.

---

## 📂 Structure Principale

```plaintext
arkalia-luna-pro/
├── core/        # Logique partagée multi-modules
├── modules/     # Modules IA indépendants (Reflexia, Nyxalia, etc.)
├── config/      # Fichiers .toml, .json (centrés)
├── logs/        # Journaux d'activité (journalisation réflexive)
├── state/       # États internes persistants (sauvegardes IA)
├── utils/       # Fonctions techniques et connecteurs externes
├── tests/       # Tests unitaires et d’intégration (pytest)
├── docs/        # Documentation publique (MkDocs, Mermaid, etc.)
└── scripts/     # Scripts automatisés (build, test, docker, backup)

🧪 Devstation IA Professionnelle

Composant
Statut
Description technique
🔁 Git & Tags
✅
Dépôt propre, versionné via bumpver, avec branche main
🧼 Qualité Code
✅
pre-commit actif : black, ruff, pytest, auto-formatage
🧪 Tests
✅
Couverture ≥ 85 %, pytest, pytest-cov, alias ark-test
🐳 Docker
✅
Conteneurisation complète (Dockerfile, docker-compose)
🌍 API FastAPI
✅
Serveur local uvicorn, endpoints /status, /chat, /echo
📘 MkDocs
✅
Documentation publique auto-déployée (GitHub Pages)
🚦 CI/CD
✅
Workflows GitHub Actions (tests, lint, build, doc, deploy)


🧠 Kernel vs Devstation

Composant
Description
/arkalia-luna-core/
Noyau stable, sans logique métier. Config, bootstrap, sécurité
/arkalia-luna-pro/
Devstation active IA : modulaire, locale, dockerisée, versionnée


🛰 Architecture Dynamique (Mermaid)

graph TD
  ReflexIA --> ZeroIA
  ZeroIA --> ArkaliaLoop
  ArkaliaLoop --> Nyxalia
  Nyxalia --> User

  📦 Exemples de Blocs Riches (Markdown)

➕ Code multi-langages

=== "Python"
    ```python
    print("Hello, Arkalia-LUNA!")
    ```

=== "JavaScript"
    ```javascript
    console.log("Hello, Arkalia-LUNA!");
    ```

    🎯 Objectifs Stratégiques
	•	🔒 Aucune dette technique persistante
	•	🧩 Modules IA orchestrables et autonomes
	•	🧠 Architecture cognitive interconnectée
	•	🌍 Déploiement local prêt production
	•	📚 Documentation publique automatisée et stylisée

⸻

🧠 La force d’Arkalia réside dans sa clarté structurelle, sa cohérence cognitive et son évolutivité modulaire.
