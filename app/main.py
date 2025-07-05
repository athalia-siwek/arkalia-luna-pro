import logging
import time
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    REGISTRY,
    Counter,
    Gauge,
    Histogram,
    Summary,
    generate_latest,
)

from core.ark_logger import ark_logger
from modules.assistantia.core import router as assistantia_router
from modules.monitoring.prometheus_metrics import ArkaliaMetrics
from modules.reflexia.core_api import router as reflexia_router
from modules.zeroia.core import router as zeroia_router

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Instance globale des métriques
metrics = ArkaliaMetrics()

# Variables globales pour le suivi
start_time = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
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

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# Middleware pour les métriques
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    request_start_time = time.time()

    response = await call_next(request)

    # Calculer la durée
    duration = time.time() - request_start_time

    # Incrémenter les compteurs
    metrics.arkalia_requests_total.labels(
        method=request.method, endpoint=request.url.path, status=response.status_code
    ).inc()

    # Enregistrer la durée
    metrics.arkalia_request_duration.labels(
        method=request.method, endpoint=request.url.path
    ).observe(duration)

    return response


@app.get("/")
async def root():
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
async def health():
    """Health check"""
    return {"status": "ok", "service": "arkalia-api"}


@app.get("/status")
async def get_status():
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

        # Générer le format Prometheus
        prometheus_data = generate_latest()

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

    ark_logger.info(
        "[green bold]Arkalia-LUNA is active and running.[/green bold]", extra={"module": "app"}
    )
