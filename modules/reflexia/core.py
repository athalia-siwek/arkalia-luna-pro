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

    # Toujours sauvegarder, même en état dégradé
    if status.lower() in {"ok", "degraded", "critical"}:
        save_snapshot(metrics, status)

    return {"status": status, "metrics": metrics}


def launch_reflexia_loop() -> None:
    """
    🔁 Lance la boucle réflexive automatique depuis `main_loop`.
    Utilisé pour un mode surveillance continue.
    """
    from modules.reflexia.logic.main_loop import reflexia_loop

    reflexia_loop()
