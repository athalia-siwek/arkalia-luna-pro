# 📁 modules/reflexia/core_api.py

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from modules.reflexia.core import launch_reflexia_check

# 🧩 Router Reflexia
router = APIRouter(
    prefix="/reflexia",
    tags=["Reflexia"],
)


@router.get("/check")
async def check_reflexia_status():
    """
    ✅ Endpoint de vérification réflexive.
    Retourne l'état des métriques système (CPU, RAM, etc.)
    """
    try:
        result = launch_reflexia_check()
        return JSONResponse(content={"status": "ok", "metrics": result["metrics"]})

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Erreur réflexive : {str(e)}"},
        )
