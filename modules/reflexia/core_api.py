# /Volumes/T7/devstation/cursor/arkalia-luna-pro/modules/reflexia/core_api.py

from fastapi import APIRouter

from modules.reflexia.core import launch_reflexia_check

router = APIRouter()


@router.get("/reflexia/check", tags=["Reflexia"])
def reflexia_check():
    """
    ✅ Lance une vérification réflexive instantanée.
    Retourne : status + métriques.
    """
    return launch_reflexia_check()
