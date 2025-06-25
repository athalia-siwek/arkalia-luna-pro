# 🧪 Tests Arkalia-LUNA

Bienvenue dans la suite de tests officielle du projet **Arkalia LUNA**.
Tous les tests sont organisés de manière modulaire, maintenable et orientée production.

---

## 📂 Structure des tests

```text
tests/
├── base/         → Tests de base du système (connexion, structure, validité initiale)
├── core/         → Tests des fonctions centrales (core logique, scheduler, etc.)
├── scripts/      → Tests des scripts utilitaires (sitemap, backup, docker, etc.)
├── modules/      → Tests unitaires des modules IA (assistantia, reflexia, etc.)
├── integration/  → Tests croisés entre modules IA (communication, orchestration)

🔍 Exécution des tests

Pour exécuter tous les tests avec couverture :

ark-test

Ou manuellement :

pytest --cov=modules --cov=core --cov=tests --cov-report=term --cov-report=html

La couverture sera générée dans htmlcov/index.html.

✅ Bonnes pratiques
	•	Chaque fichier de test doit commencer par test_*.py.
	•	Les assertions doivent être explicites (assert response.status_code == 200, etc.).
	•	Utiliser pytest uniquement (pas de unittest classique).
	•	Regrouper les tests par module IA ou composant métier clair.

⸻

🚀 Objectif de couverture

🎯 Objectif : 80 % de couverture minimale par module IA
Tests critiques (exécution, sécurité, routing) obligatoires à 100 %.

⸻

🧠 Cette structure fait partie du standard Arkalia System Next (ASN), phase v1.2.x+.
