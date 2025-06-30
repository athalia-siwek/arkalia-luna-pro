# modules/assistantia/utils/ollama_connector.py

import json
from typing import Any, Dict, Optional

import requests


def query_ollama(prompt: str, model: str = "llama2", temperature: float = 0.7) -> str:
    """Interroge l'API Ollama avec un prompt donné."""
    try:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False
        }

        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()

        data = response.json()
        return data.get("response", "Aucune réponse reçue")
    except requests.RequestException as e:
        return f"Erreur de connexion: {str(e)}"
    except json.JSONDecodeError:
        return "Erreur de décodage JSON"
    except Exception as e:
        return f"Erreur inattendue: {str(e)}"


def get_available_models() -> dict[str, Any] | None:
    """Récupère la liste des modèles disponibles."""
    try:
        url = "http://localhost:11434/api/tags"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        return data
    except requests.RequestException:
        return None
    except Exception:
        return None


def check_ollama_health() -> bool:
    """Vérifie si Ollama est accessible."""
    try:
        url = "http://localhost:11434/api/tags"
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except Exception:
        return False
