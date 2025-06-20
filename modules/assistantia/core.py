# modules/assistantia/core.py

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse

from modules.assistantia.utils.ollama_connector import query_ollama

router = APIRouter()


def process_input(message: str) -> str:
    return f"Tu as dit : {message}"


@router.post("/chat", tags=["IA"])
async def chat(request: Request):
    try:
        data = await request.json()
        prompt = data.get("message", "").strip()

        if not prompt:
            return JSONResponse(
                status_code=400, content={"error": "Aucun message reçu."}
            )

        response_text = query_ollama(prompt)
        return {"réponse": response_text}

    except Exception as e:
        return JSONResponse(
            status_code=500, content={"error": f"Erreur interne : {str(e)}"}
        )


# API exposée
app = FastAPI()
app.include_router(router)
