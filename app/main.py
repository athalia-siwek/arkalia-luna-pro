import logging
import time
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Union

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from modules.assistantia.core import router as assistantia_router
from modules.monitoring.prometheus_metrics import ArkaliaMetrics
from modules.reflexia.core_api import router as reflexia_router
from modules.zeroia.core import router as zeroia_router

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Instance globale des métriques avec registre unique
metrics = ArkaliaMetrics()

# Variables globales pour le suivi
start_time = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Gestion du cycle de vie de l'application"""
    logger.info("🚀 Démarrage Arkalia-LUNA API")

    # Initialiser les métriques
    metrics.arkalia_system_uptime.set(0)
    metrics.arkalia_modules_status.labels(module_name="assistantia").set(1)
    metrics.arkalia_modules_status.labels(module_name="reflexia").set(1)
    metrics.arkalia_modules_status.labels(module_name="zeroia").set(1)

    yield

    logger.info("🛑 Arrêt Arkalia-LUNA API")


# Création de l'application FastAPI
app = FastAPI(
    title="Arkalia-LUNA Pro API",
    description="API principale du système Arkalia-LUNA Pro",
    version="2.8.0",
    lifespan=lifespan,
)

# Configuration CORS corrigée
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permettre toutes les origines pour les tests
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# Middleware pour les métriques
@app.middleware("http")
async def metrics_middleware(request: Request, call_next) -> PlainTextResponse:
    start_time = time.time()

    response = await call_next(request)

    # Calculer la durée
    duration = time.time() - start_time

    # Incrémenter les compteurs
    metrics.arkalia_requests_total.labels(
        method=request.method, endpoint=request.url.path, status=str(response.status_code)
    ).inc()

    # Enregistrer la durée
    metrics.arkalia_request_duration.labels(
        method=request.method, endpoint=request.url.path
    ).observe(duration)

    return response


@app.get("/")
async def root() -> dict:
    """Endpoint racine"""
    return {
        "message": "🌕 Arkalia-LUNA Pro API",
        "version": "2.8.0",
        "status": "active",
        "modules": ["assistantia", "reflexia", "zeroia"],
        "uptime": time.time() - start_time,
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/health")
async def health() -> dict:
    """Health check"""
    return {"status": "ok", "service": "arkalia-api"}


@app.get("/status")
async def get_status() -> dict:
    """Statut détaillé de l'API"""
    import psutil

    return {
        "service": "arkalia-api",
        "version": "2.8.0",
        "status": "active",
        "uptime_seconds": time.time() - start_time,
        "modules": {"assistantia": "active", "reflexia": "active", "zeroia": "active"},
        "metrics": "available",
        "system": {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage("/").percent,
        },
    }


@app.get("/metrics")
async def get_metrics():
    """
    📊 Endpoint métriques Prometheus pour l'API principale
    """
    try:
        # Mettre à jour les métriques système
        import psutil

        # Uptime
        metrics.arkalia_system_uptime.set(time.time() - start_time)

        # Mémoire
        memory = psutil.virtual_memory()
        metrics.arkalia_memory_usage.set(memory.used)

        # CPU
        cpu_percent = psutil.cpu_percent(interval=0.1)
        metrics.arkalia_cpu_usage.set(cpu_percent)

        # Générer le format Prometheus avec le registre unique
        prometheus_data = generate_latest(metrics.get_registry())

        return PlainTextResponse(content=prometheus_data, media_type=CONTENT_TYPE_LATEST)
    except Exception as e:
        logger.error(f"Erreur métriques : {e}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Erreur métriques : {str(e)}"},
        )


# Inclusion des routers
app.include_router(assistantia_router, prefix="/assistantia")
app.include_router(reflexia_router, prefix="/reflexia")
app.include_router(zeroia_router, prefix="/zeroia")


def print_status() -> None:
    from rich import print

    print("[green bold]Arkalia-LUNA is active and running.[/green bold]")
