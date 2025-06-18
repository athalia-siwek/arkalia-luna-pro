# 🚀 API FastAPI — Arkalia-LUNA

L’API FastAPI d’Arkalia-LUNA permet d’interagir avec le système IA **depuis des requêtes HTTP locales**, tout en garantissant modularité, sécurité et scalabilité.

---

## 🌐 Endpoint de base

- **URL locale** : `http://127.0.0.1:8000/`
- **Serveur** : `Uvicorn` via Docker ou lancement manuel
- **Script de démarrage** :
```bash
uvicorn helloria.core:app --reload