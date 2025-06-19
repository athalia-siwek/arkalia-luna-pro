# modules/assistantia/utils/ollama_connector.py

import requests


def query_ollama(prompt: str) -> str:
    try:
        base_context = (
            "Tu es ReflexIA, un module IA du système Arkalia-LUNA. "
            "Tu es spécialisé dans la surveillance adaptative, l’analyse système, "
            "et la prise de décision automatique. Sois clair, synthétique et pro."
        )

        full_prompt = f"{base_context}\n\nQuestion utilisateur : {prompt}"

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": full_prompt, "stream": False},
            timeout=20,
        )

        data = response.json()
        return data.get("response", "[⚠️ Réponse IA vide]")

    except Exception as e:
        return f"[Erreur IA] {str(e)}"
