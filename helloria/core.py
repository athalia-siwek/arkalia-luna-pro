# 📁 helloria/core.py

import logging

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse

# 📦 Import des routes externes (modules IA)
from modules.reflexia.core_api import router as reflexia_router

# 🚦 Router principal
router = APIRouter()

# 🧾 Logging d’erreurs
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="app_errors.log",
)


# 🎯 Endpoint principal IA
@router.post("/chat", tags=["IA"])
async def chat(request: Request):
    try:
        data = await request.json()
        prompt = data.get("message", "").strip()

        if not prompt:
            return JSONResponse(
                status_code=400, content={"error": "Aucun message reçu."}
            )

        # Placeholder IA
        response_text = f"Tu as dit : '{prompt}' (réponse IA à coder 🎯)"
        return {"réponse": response_text}

    except Exception as e:
        logging.error(f"Erreur interne : {str(e)}")
        return JSONResponse(
            status_code=500, content={"error": f"Erreur interne : {str(e)}"}
        )


# 🌐 Racine API
@router.get("/", tags=["Root"])
async def root():
    return {"message": "Arkalia-LUNA API active"}


# 🚀 Application FastAPI
app = FastAPI(
    title="Arkalia-LUNA API",
    version="v2.1.1",
    description="API principale des modules IA Arkalia",
)

# 🧩 Inclusion des routers
app.include_router(router)
app.include_router(reflexia_router)  # ✅ Active le endpoint /reflexia/check
