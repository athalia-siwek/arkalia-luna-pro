# 📬 API Arkalia-LUNA (`/chat`, `/status`, `/metrics`)

![Version](https://img.shields.io/badge/version-v2.4.0-blue)
![CI](https://github.com/athalia-siwek/arkalia-luna-pro/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-Proprietary-red)
![Coverage](https://img.shields.io/badge/coverage-93%25-brightgreen)

Bienvenue dans la documentation officielle de l’API de **Helloria**, le point d’entrée HTTP de votre système IA local Arkalia-LUNA.

> Cette API est gérée par le module `Helloria`, et permet d’interagir avec les assistants IA (`AssistantIA`, `Reflexia`, etc.), d’effectuer des tests, de surveiller le système et de lancer des actions intelligentes.

---

## 🚀 Endpoints principaux

### `POST /chat`

- **Description** : Envoie une requête textuelle à l’assistant IA (`AssistantIA`).
- **Payload JSON** :
  ```json
  {
    "message": "Quelle est l'état de ReflexIA ?",
    "user_id": "athalia-01"
  }
  ```

- **Test rapide** :
  > 🧪 Test rapide :
  >
  > ```bash
  > curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" \
  > -d '{"message": "Statut ZeroIA"}'
  > ```

- **Authentification** :
  > 🔒 Cette API est locale, mais une gestion future des tokens/JWT est prévue pour renforcer la sécurité.

### `GET /status`
- **Description** : Retourne l'état global de l'instance Arkalia (modules actifs, statut, etc.)
- **Réponse** :
  ```json
  {
    "status": "running",
    "modules": ["reflexia", "assistantia", "zeroia", "nyxalia"]
  }
  ```

### `GET /metrics`
- **Description** : Renvoie des métriques sur les appels API, temps de réponse, et éventuelles erreurs.
- **Exemple** :
  ```json
  {
    "uptime": "3h12m",
    "requests_handled": 103,
    "average_response_ms": 217
  }
  ```

---

## 🧪 Routes de test & développement

### `POST /debug/echo`
- **Payload** : n'importe quelle chaîne JSON
- **Réponse** : renvoie exactement ce qui a été envoyé (utile pour debug)
- **Exemple** :
  ```bash
  curl -X POST http://localhost:8000/debug/echo -H "Content-Type: application/json" -d '{"test": "ping"}'
  ```

---

## ⚙️ Headers recommandés
- `Content-Type: application/json`
- `Authorization: Bearer <token>` (si futur système de jetons activé)

---

## 🔒 Sécurité

Cette API est locale, non exposée publiquement par défaut. Si un reverse proxy est mis en place (type Nginx), veillez à :
- Restreindre l'accès IP
- Activer HTTPS si utilisé sur un réseau

---

## 🧪 Exemple d'appel en terminal

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Qui es-tu ?"}'
```

---

## 📚 Voir aussi
- [Guide API](api.md) dans les pages [index.md](index.md) et [Helloria](modules/helloria.md) pour une meilleure navigation.

---

## 📂 Fichier à créer

```bash
touch docs/api.md

Puis colle le contenu ci-dessus. Tu peux ensuite l'intégrer dans mkdocs.yml comme ceci :

- 📬 API Arkalia: api.md

```

---

© 2025 **Athalia** – Tous droits réservés.
🤖 Powered by Arkalia ReflexIA `v1.x`
