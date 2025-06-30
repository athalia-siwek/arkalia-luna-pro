# 🧠 AssistantIA — Module Cognitif Intégré

![Version](https://img.shields.io/badge/version-v3.0--phase1-blue)
![CI](https://github.com/athalia-siwek/arkalia-luna-pro/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-Proprietary-red)
![Coverage](https://img.shields.io/badge/coverage-36%25-brightgreen)

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
```

📍 **Port configurable** dans `docker-compose.yml` ou `config/`.

---

## 🔄 Endpoints disponibles

| Méthode | URL    | Description                      |
|---------|--------|----------------------------------|
| POST    | /chat  | Envoie un message à l’IA locale  |
| GET     | /status| État du module assistantia       |

---

## 🧪 Tests associés

- **Fichiers** :
  - `test_assistantia.py` (unitaires)
  - `test_assistantia_integration.py` (intégration)

✅ **Couverture** : 81 % — avec plan d’extension vers les cas d’erreur et logs détaillés.

---

## 🌐 Connectivité modulaire

Le module est connecté à :
- `helloria/` (API externe)
- `reflexia/` (logs et surveillance IA)
- `nyxalia/` (interprétation mobile)

💡 **Prêt pour une extension** vers Ollama, Langchain, ou des modèles hybrides.

---

🎯 **Objectif futur** : une IA embarquée réflexive, contextuelle, auto-ajustable.

---

## 🧠 AssistantIA — Utilisation et Intégration LLM

L'AssistantIA est conçu pour offrir une interaction fluide et intelligente avec les utilisateurs, en intégrant des modèles de langage de pointe (LLM) pour comprendre et répondre aux requêtes de manière contextuelle.

---

## 🚀 Fonctionnalités Principales

- **Réponses Contextuelles** : Grâce à l'intégration de modèles LLM comme Mistral et Llama2, l'AssistantIA peut fournir des réponses précises et adaptées au contexte de la conversation.
- **Personnalisation** : L'AssistantIA s'adapte aux préférences de l'utilisateur, offrant une expérience personnalisée.
- **Intégration Facile** : Peut être intégré dans diverses applications via des API REST, facilitant l'interaction avec d'autres systèmes.

---

## 🌐 Exemple d'Utilisation

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Quelle est la philosophie d'Arkalia ?"}'
```

---

## 🧠 Modèles LLM Intégrés

L'AssistantIA utilise des modèles LLM locaux pour garantir la confidentialité et l'efficacité. Les modèles sont stockés localement et peuvent être mis à jour ou remplacés selon les besoins.

---

## 📊 Structure JSON Entrante/Sortante

### Requête

```json
{
  "message": "Bonjour Arkalia",
  "mode": "empathique",
  "lang": "fr",
  "user_id": "12345"
}
```

### Réponse

```json
{
  "réponse": "Bonjour ! Je suis AssistantIA, prêt à vous aider."
}
```

---

## ⚙️ Paramètres Optionnels

- **mode** : Définit le mode de raisonnement de l'IA (ex: neutre, empathique).
- **lang** : Langue de réponse attendue (ex: fr, en).
- **user_id** : Identifiant utilisateur pour personnalisation.

---

## 📊 Schéma d'Interaction

```mermaid
sequenceDiagram
    participant U as Utilisateur
    participant A as AssistantIA
    participant O as Ollama
    U->>A: POST /chat (message)
    A->>O: Query modèle
    O-->>A: Réponse IA
    A-->>U: JSON { "réponse": "..." }
```

---

🧠 *L'AssistantIA est votre partenaire intelligent pour une interaction IA enrichissante et sécurisée.*

Pour des considérations de sécurité, veuillez consulter [la section Sécurité](../../security/security.md).

---

© 2025 **Athalia** – Tous droits réservés.
🤖 Powered by Arkalia ReflexIA `v1.x`

# Documentation du Module Assistantia

## Introduction
Le module Assistantia est un composant clé du projet Arkalia-LUNA, conçu pour fournir des fonctionnalités avancées d'assistance et d'automatisation. Il joue un rôle crucial dans l'amélioration de l'efficacité opérationnelle et la réduction des erreurs humaines.

## Fonctionnalités
- **Automatisation des tâches** : Assistantia peut automatiser des tâches répétitives, libérant ainsi du temps pour des activités plus stratégiques.
- **Intégration transparente** : S'intègre facilement avec d'autres modules pour offrir une expérience utilisateur fluide.
- **Personnalisation** : Permet une personnalisation avancée pour répondre aux besoins spécifiques des utilisateurs.

## Configuration
Pour configurer le module Assistantia, modifiez le fichier `assistantia_config.toml` et ajustez les paramètres suivants :
- `enable_feature_x`: Active ou désactive la fonctionnalité X.
- `api_key`: Clé API nécessaire pour l'authentification.

## API
Le module expose plusieurs points d'entrée API :
- `GET /assistantia/status`: Retourne le statut actuel du module.
- `POST /assistantia/execute`: Exécute une commande spécifique.

## Dépannage
En cas de problème avec le module Assistantia, vérifiez les logs dans `logs/assistantia.log` pour des messages d'erreur détaillés. Assurez-vous que toutes les dépendances sont correctement installées.
