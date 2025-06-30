from collections.abc import Callable
from typing import Any, Optional

import requests
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, generate_latest
from pydantic import BaseModel

from .utils.ollama_connector import query_ollama as real_query_ollama
from .utils.processing import process_input

# Métriques Prometheus locales pour AssistantIA
assistantia_prompts_total = Counter(
    "assistantia_prompts_total",
    "Nombre total de prompts traités par AssistantIA",
    ["status", "security_level"],
)

assistantia_response_time = Gauge(
    "assistantia_response_time_seconds", "Temps de réponse AssistantIA"
)

router = APIRouter()


class MessageInput(BaseModel):
    message: str


# 👇 Correction ici : Callable[[str], str], car on n'utilisera qu'un seul argument
def get_query_ollama() -> Callable[[str], str]:
    # On fixe le modèle ici via une fonction curryée
    return lambda prompt: real_query_ollama(prompt, "mistral")


@router.post("/chat")
async def post_chat(
    data: MessageInput,
    query_ollama: Callable[[str], str] = Depends(get_query_ollama),
) -> dict[str, str]:
    message = data.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message vide")

    try:
        # 🔥 NOUVELLE INTÉGRATION - Contexte Arkalia
        arkalia_context = get_arkalia_context()

        # Enrichir le message avec le contexte
        enriched_message = f"{message}\n\nContexte système: {arkalia_context}"

        processed = process_input(enriched_message)
        response = query_ollama(processed)  # 👈 Appel direct avec un seul argument

        # Enregistrer métriques
        assistantia_prompts_total.labels(status="success", security_level="medium").inc()

        return {"réponse": response}
    except requests.exceptions.Timeout:
        assistantia_prompts_total.labels(status="timeout", security_level="medium").inc()
        raise HTTPException(status_code=500, detail="Erreur : délai dépassé") from None
    except Exception as e:
        assistantia_prompts_total.labels(status="error", security_level="medium").inc()
        raise HTTPException(status_code=500, detail=f"Erreur interne : {str(e)}") from e


def get_arkalia_context() -> str:
    """Récupère le contexte des autres modules Arkalia"""
    context_parts: list[Any] = []

    try:
        # État ZeroIA
        import json
        from pathlib import Path

        zeroia_dashboard = Path("state/zeroia_dashboard.json")
        if zeroia_dashboard.exists():
            try:
                with open(zeroia_dashboard) as f:
                    dashboard = json.load(f)
                context_parts.append(f"ZeroIA: {dashboard.get('last_decision', 'unknown')}")
            except (json.JSONDecodeError, KeyError, OSError):
                context_parts.append("ZeroIA: unavailable")
        else:
            context_parts.append("ZeroIA: inactive")
    except Exception:
        context_parts.append("ZeroIA: unavailable")

    try:
        # État Reflexia
        import toml

        reflexia_state = Path("state/reflexia_state.toml")
        if reflexia_state.exists():
            try:
                reflexia_data = toml.load(reflexia_state)
                context_parts.append(f"Reflexia: {reflexia_data.get('status', 'unknown')}")
            except (toml.TomlDecodeError, KeyError, OSError):
                context_parts.append("Reflexia: unavailable")
        else:
            context_parts.append("Reflexia: inactive")
    except Exception:
        context_parts.append("Reflexia: unavailable")

    try:
        # État Sandozia
        sandozia_state = Path("state/sandozia")
        if sandozia_state.exists():
            context_parts.append("Sandozia: active")
        else:
            context_parts.append("Sandozia: inactive")
    except Exception:
        context_parts.append("Sandozia: unavailable")

    return " | ".join(context_parts) if context_parts else "Système Arkalia-LUNA"


app = FastAPI()
app.include_router(router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/metrics")
async def get_metrics():
    """
    📊 Endpoint métriques Prometheus pour AssistantIA
    """
    try:
        # Générer le format Prometheus
        prometheus_data = generate_latest()

        return PlainTextResponse(content=prometheus_data, media_type=CONTENT_TYPE_LATEST)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Erreur métriques : {str(e)}"},
        )
