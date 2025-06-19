# 🤖 AssistantIA — Module Cognitif Intégré

Le module `assistantia/` est l’interface d’assistance IA locale d’Arkalia-LUNA. Il agit comme **guide conversationnel**, interface cognitive et **répondant intelligent** aux requêtes utilisateurs.

---

## 🧠 Rôle du module

- Dialogue IA avec l’utilisateur
- Réponses contextuelles personnalisées
- Interface évolutive vers l’IA autonome embarquée
- Support aux modules (Helloria, Reflexia…)

---

## 🚀 Lancement manuel

```bash
uvicorn modules.assistantia.core:app --port 8001

📍 Port configurable dans docker-compose.yml ou config/.

⸻

🔁 Endpoints disponibles

Méthode
URL
Description
POST
/chat
Envoie un message à l’IA locale
GET
/status
État du module assistantia

🧪 Tests associés

Fichiers :
	•	test_assistantia.py (unitaires)
	•	test_assistantia_integration.py (intégration)

✅ Couverture : 81 % — avec plan d’extension vers les cas d’erreur et logs détaillés.

⸻

🌐 Connectivité modulaire

Le module est connecté à :
	•	helloria/ (API externe)
	•	reflexia/ (logs et surveillance IA)
	•	nyxalia/ (interprétation mobile)

💡 Il est prêt pour une extension vers Ollama, Langchain, ou des modèles hybrides.

⸻

🎯 Objectif futur : une IA embarquée réflexive, contextuelle, auto-ajustable.