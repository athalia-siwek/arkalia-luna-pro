# 🚀 API FastAPI — Arkalia-LUNA

L’API FastAPI permet à des agents externes, humains ou systèmes, de communiquer avec Arkalia-LUNA de manière **locale, modulaire et sécurisée**.

---

## 🌐 Endpoint principal

- **URL locale** : `http://127.0.0.1:8000/`
- **Serveur** : `Uvicorn` (via Docker ou en local)
- **Point d’entrée** : `helloria.core:app`

### ▶️ Commande de démarrage manuelle

```bash
uvicorn helloria.core:app --reload

💡 Alternativement, utiliser docker-compose up ou le script ark-docker.

Méthode
URL
Description
GET
/
Test de vie : “Bienvenue dans Helloria”
POST
/chat
Envoie un prompt à l’IA locale (assistantia)
GET
/status
Retourne l’état général du système
GET
/echo?msg=x
Répond avec le message donné


⸻

🔐 Sécurité & accès
	•	API uniquement exposée en local
	•	Possibilité future d’ajouter :
	•	Authentification par clé
	•	Rate limiting
	•	Journalisation des accès via reflexia

⸻

📦 Design modulaire

Chaque endpoint est délégué à un module :
	•	helloria/ = orchestration API
	•	assistantia/ = génération IA
	•	reflexia/ = métriques & diagnostics
	•	nyxalia/ = interprétation mobile

⸻

✅ Architecture pensée pour l’extensibilité et le contrôle par module.