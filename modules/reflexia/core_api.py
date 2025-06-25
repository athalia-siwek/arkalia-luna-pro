# 📁 modules/reflexia/core_api.py

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from modules.reflexia.core import launch_reflexia_check

# 🧩 Router Reflexia
router = APIRouter(
    prefix="/reflexia",
    tags=["Reflexia"],
)


def get_reflexia_status() -> dict:
    """
    Fonction testable indépendamment de l'API FastAPI.
    Retourne un dictionnaire avec les métriques du système.
    """
    result = launch_reflexia_check()
    return {"status": "ok", "metrics": result["metrics"]}


@router.get("/check")
async def check_reflexia_status():
    """
    ✅ Endpoint de vérification réflexive.
    Retourne l'état des métriques système (CPU, RAM, etc.)
    """
    try:
        return JSONResponse(content=get_reflexia_status())
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Erreur réflexive : {str(e)}"},
        )
