# modules/assistantia/core.py

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

from modules.assistantia.utils.ollama_connector import query_ollama

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


def process_input(message: str) -> str:
    return f"Tu as dit : {message}"


@router.post("/chat", tags=["IA"])
async def chat_route(request: ChatRequest):
    response = query_ollama(request.message)
    return {"réponse": response}


# API exposée
app = FastAPI()
app.include_router(router)
