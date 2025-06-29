from collections.abc import Callable
from typing import Any, Optional

import requests
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from pydantic import BaseModel

from modules.assistantia.utils.ollama_connector import query_ollama as real_query_ollama
from modules.assistantia.utils.processing import process_input

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
    query_ollama: Callable[[str], str] = None,
) -> dict[str, str]:
    if query_ollama is None:
        query_ollama = get_query_ollama()

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
        return {"réponse": response}
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=500, detail="Erreur : délai dépassé") from None
    except Exception as e:
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
            with open(zeroia_dashboard) as f:
                dashboard = json.load(f)
            context_parts.append(f"ZeroIA: {dashboard.get('last_decision', 'unknown')}")
    except Exception:
        context_parts.append("ZeroIA: unavailable")

    try:
        # État Reflexia
        import toml

        reflexia_state = Path("state/reflexia_state.toml")
        if reflexia_state.exists():
            reflexia_data = toml.load(reflexia_state)
            context_parts.append(f"Reflexia: {reflexia_data.get('status', 'unknown')}")
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
def health() -> None:
    return {"status": "ok"}
