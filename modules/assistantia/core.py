import requests
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from pydantic import BaseModel

from modules.assistantia.utils.ollama_connector import query_ollama as real_query_ollama
from modules.assistantia.utils.processing import process_input

router = APIRouter()


class MessageInput(BaseModel):
    message: str


def get_query_ollama():
    return real_query_ollama


@router.post("/chat")
async def post_chat(data: MessageInput, query_ollama=Depends(get_query_ollama)) -> dict:
    message = data.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message vide")

    try:
        processed = process_input(message)
        response = query_ollama(processed, model="mistral")
        return {"réponse": response}
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=500, detail="Erreur : délai dépassé")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne : {str(e)}")


app = FastAPI()
app.include_router(router)
