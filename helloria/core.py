# 📁 helloria/core.py

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse

router = APIRouter()


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
        return JSONResponse(
            status_code=500, content={"error": f"Erreur interne : {str(e)}"}
        )


@router.get("/", tags=["Root"])
async def root():
    return {"message": "Arkalia-LUNA API active"}


# ✅ On expose ici l'app FastAPI avec les routes
app = FastAPI()
app.include_router(router)
