# modules/assistantia/utils/ollama_connector.py

import requests


def query_ollama(prompt: str) -> str:
    try:
        base_context = (
            "Tu es ReflexIA, un module IA du système Arkalia-LUNA. "
            "Tu es spécialisé dans la surveillance adaptative, l’analyse système, "
            "et la prise de décision automatique en cas d’alerte cognitive. "
            "Réponds toujours de manière claire, synthétique et professionnelle."
        )

        full_prompt = f"{base_context}\n\nQuestion utilisateur : {prompt.strip()}"

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": full_prompt, "stream": False},
            timeout=20,
        )

        if response.status_code != 200:
            return f"[⚠️ Erreur API Ollama] {response.status_code} : {response.text}"

        data = response.json()
        return data.get("response", "[⚠️ Réponse IA vide]")

    except requests.exceptions.RequestException as req_err:
        return f"[⚠️ Erreur réseau Ollama] {str(req_err)}"
    except Exception as e:
        return f"[❌ Erreur interne] {str(e)}"
