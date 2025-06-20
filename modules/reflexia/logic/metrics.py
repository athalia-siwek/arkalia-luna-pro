def read_metrics() -> dict:
    """
    Simule la collecte de métriques système.
    Peut être remplacée plus tard par psutil ou outils réels.
    """
    return {
        "cpu": 72.5,
        "ram": 61.8,
        "latency": 145,
    }
