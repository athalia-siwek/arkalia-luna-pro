#!/usr/bin/env python3

"""
🚀 Lancement du serveur FastAPI pour Cognitive Reactor

Ce script démarre :
1. Le serveur FastAPI qui expose les endpoints du Cognitive Reactor

Endpoints exposés :
- /health : État de santé du service
- /metrics : Métriques Prometheus
"""

import uvicorn
from fastapi import FastAPI

from modules.cognitive_reactor.core import app as cognitive_app

app = FastAPI(
    title="Cognitive Reactor API",
    description="API REST pour le module d'intelligence avancée d'Arkalia",
    version="2.7.0",
)

# Inclure les routes du Cognitive Reactor
app.mount("/cognitive", cognitive_app)

@app.get("/health")
async def health_check() -> dict:
    """Endpoint de santé pour le healthcheck Docker"""
    return {"status": "healthy", "service": "cognitive_reactor"}

if __name__ == "__main__":
    # Démarrer le serveur FastAPI
    uvicorn.run(
        app, host="0.0.0.0", port=8003
    )  # Interface accessible depuis l'extérieur du conteneur 