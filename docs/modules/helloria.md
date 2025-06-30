# Helloria

Helloria est le module central de coordination cognitive de l'application Arkalia-LUNA. Il gère les interactions de base avec l'API et orchestre les requêtes entrantes et sortantes.

## Objectif du Module
Helloria sert de point central pour la coordination des tâches cognitives au sein du système Arkalia-LUNA.

## Exemple de Requête
```python
import requests

response = requests.get("http://localhost:8000/")
print(response.json())
```

## Routes Exposées
- `GET /`: Retourne un message de bienvenue.
- `GET /status`: Retourne le statut opérationnel de Helloria.

## Documentation Générale
Pour plus de détails, consultez la [documentation générale](https://athalia-siwek.github.io/arkalia-luna-pro/).
