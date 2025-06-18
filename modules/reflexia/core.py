# modules/reflexia/core.py


def monitor_status(metrics):
    """
    Analyse les métriques et retourne un statut simple.
    """
    if metrics.get("cpu", 0) > 90:
        return "🛑 surcharge CPU"
    elif metrics.get("memory", 0) > 80:
        return "⚠️ haute mémoire"
    return "✅ stable"
