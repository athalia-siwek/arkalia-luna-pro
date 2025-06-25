# 📁 modules/reflexia/core.py

"""
Module principal pour lancer la logique réflexive :
- Check unique (snapshot + status)
- Boucle réflexive (surveillance continue)
"""

from modules.reflexia.logic.decision import monitor_status
from modules.reflexia.logic.metrics import read_metrics
from modules.reflexia.logic.snapshot import save_snapshot


def launch_reflexia_check() -> dict:
    """
    📍 Lance une vérification réflexive unique :
    - Collecte des métriques système
    - Évaluation de l'état via `monitor_status`
    - Sauvegarde snapshot dans `state/`

    :return: Dictionnaire contenant `status` (str) et `metrics` (dict)
    """
    metrics = read_metrics()
    status = monitor_status(metrics)

    # ✅ Sauvegarde même si status critique
    save_snapshot(metrics, status)

    return {"status": status, "metrics": metrics}


# ✅ Alias utilisé par l'API pour simplifier les imports
def get_metrics() -> dict:
    """
    🎯 Interface simple pour l'API REST :
    Retourne uniquement les métriques (sans logique réflexive complète).
    """
    return read_metrics()


def launch_reflexia_loop() -> None:
    """
    🔁 Lance la boucle réflexive automatique depuis `main_loop.py`.
    Utilisé pour un mode surveillance continue (via trigger ou cron).
    """
    from modules.reflexia.logic.main_loop import reflexia_loop

    reflexia_loop()


def load_reflexia_data() -> dict:
    return {
        "metrics": {
            "cpu": 42,
            "ram": 65,
        },
        "status": "ok",
    }
