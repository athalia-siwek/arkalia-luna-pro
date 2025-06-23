# 📁 helloria/core.py

import logging

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse

from modules.reflexia.core_api import router as reflexia_router

router = APIRouter()

# Configuration de base du logging
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="app_errors.log",
)


@router.post("/chat", tags=["IA"])
async def chat(request: Request):
    try:
        data = await request.json()
        prompt = data.get("message", "").strip()

        if not prompt:
            return JSONResponse(
                status_code=400, content={"error": "Aucun message reçu."}
            )

        response_text = f"Tu as dit : '{prompt}' (réponse IA à coder 🎯)"
        return {"réponse": response_text}

    except Exception as e:
        logging.error(f"Erreur interne : {str(e)}")
        return JSONResponse(
            status_code=500, content={"error": f"Erreur interne : {str(e)}"}
        )


@router.get("/", tags=["Root"])
async def root():
    return {"message": "Arkalia-LUNA API active"}


# ✅ On expose ici l'app FastAPI avec les routes
app = FastAPI()
app.include_router(router)
app.include_router(reflexia_router)
