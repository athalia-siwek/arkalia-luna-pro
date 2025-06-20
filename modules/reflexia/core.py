from modules.reflexia.logic.decision import monitor_status
from modules.reflexia.logic.metrics import read_metrics
from modules.reflexia.logic.snapshot import save_snapshot


def launch_reflexia_check() -> dict:
    """
    Lance un scan réflexif complet : collecte métriques + évalue + snapshot.
    """
    metrics = read_metrics()
    status = monitor_status(metrics)
    save_snapshot(metrics, status)
    return {"status": status, "metrics": metrics}
