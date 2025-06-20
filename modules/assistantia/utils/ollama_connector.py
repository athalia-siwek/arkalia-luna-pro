# modules/assistantia/utils/ollama_connector.py

import requests


def query_ollama(prompt: str, model: str = "mistral") -> str:
    supported_models = ["mistral", "tinyllama"]

    if model not in supported_models:
        raise ValueError(f"Modèle non supporté : {model}")

    if not prompt or not prompt.strip():
        return "[⚠️ Réponse IA vide]"

    try:
        url = "http://localhost:11434/api/generate"
        payload = {"model": model, "prompt": prompt, "stream": False}
        response = requests.post(url, json=payload, timeout=20)

        if response.status_code == 200:
            return response.json().get("response", "[⚠️ Aucune réponse générée]")
        else:
            return f"[Erreur IA] {response.status_code} : {response.text}"

    except Exception as e:
        return f"[Erreur IA] {str(e)}"
