import time

from modules.reflexia.logic.decision import monitor_status
from modules.reflexia.logic.metrics import read_metrics
from modules.reflexia.logic.snapshot import save_snapshot


def reflexia_loop(max_iterations: int = None, sleep_seconds: float = 5.0) -> None:
    """
    🔁 Boucle réflexive principale de ReflexIA.

    - Collecte les métriques système
    - Évalue l’état avec `monitor_status`
    - Sauvegarde un snapshot (metrics + status)
    - Peut être utilisée en mode infini (prod) ou limité (tests)

    :param max_iterations: Nombre max d’itérations (None = infini)
    :param sleep_seconds: Délai entre chaque itération (en secondes)
    """
    iteration = 0
    print("🔄 ReflexIA Loop started")

    while True:
        metrics = read_metrics()
        status = monitor_status(metrics)
        save_snapshot(metrics, status)
        print(f"✅ Status: {status} | Metrics: {metrics}")

        time.sleep(sleep_seconds)
        iteration += 1

        if max_iterations is not None and iteration >= max_iterations:
            print("🛑 ReflexIA Loop finished (max iterations reached)")
            break
