🧬 Structure du Noyau — Arkalia

Le noyau Arkalia est conçu comme une architecture IA industrielle modulaire, avec une séparation stricte entre le kernel pur et la Devstation de développement IA.

⸻

⚙️ 1️⃣ /arkalia-luna-core/ — Kernel IA Pur

Partie stable, figée, sans logique métier. C’est le socle d’exécution sécurisé.

	•	📁 Contenu : uniquement des fichiers de configuration système (.toml, scripts init)
	•	🔒 Aucune dette technique autorisée
	•	🚀 Script de démarrage : arkalia_devstation_bootstrap.sh
	•	🧱 Rôle : préparer, sécuriser, isoler la Devstation IA du reste du système

⸻

🧠 2️⃣ /arkalia-luna-pro/ — Devstation IA Modulaire

Environnement de développement local modulaire, dockerisé, testé, avec CI/CD active.

	•	🧩 Modules IA : reflexia, nyxalia, helloria, etc.
	•	🧪 Tests unitaires avec pytest
	•	🐳 Docker + Docker Compose
	•	🚦 GitHub Actions (CI/CD, lint, couverture)
	•	🌍 API FastAPI disponible localement
	•	🔖 Version actuelle : v1.0.6

⸻

📁 Structure Type — Devstation Pro

arkalia-luna-pro/
├── modules/               # Modules IA isolés
├── core/                  # Logique transversale
├── config/                # Fichiers .toml / .json
├── logs/                  # Journaux du système
├── state/                 # États persistants
├── scripts/               # Scripts utilitaires (build, docker, test)
├── docs/                  # Documentation MkDocs
├── tests/                 # Tests unitaires (pytest)
├── .github/workflows/     # Pipelines CI GitHub Actions

🧩 Philosophie de conception
	•	🔒 Stabilité garantie par séparation Kernel / Métier
	•	♻️ Modules IA interchangeables
	•	🧪 Tests et couverture obligatoires
	•	🛰 Déploiement local maîtrisé
	•	📚 Documentation publique automatisée
    