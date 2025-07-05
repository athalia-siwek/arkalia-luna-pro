#!/usr/bin/env python3
"""
📊 Metrics Manager - Gestionnaire de métriques pour ZeroIA

Responsabilité : Collecte et exposition des métriques Prometheus.
"""

import logging
import time
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

# === Métriques globales ===
_zeroia_metrics = {
    "decision_count": 0,
    "error_count": 0,
    "last_decision_time": None,
    "uptime_start": time.time(),
    "cognitive_score": 0.0,
    "processing_times": [],
    "decision_types": {},
}


def update_zeroia_metrics(
    operation: str,
    status: str,
    duration: float,
    cognitive_score: Optional[float] = None,
    decision_type: Optional[str] = None,
) -> None:
    """
    Met à jour les métriques ZeroIA
    
    Args:
        operation: Nom de l'opération
        status: Statut (success/error)
        duration: Durée en secondes
        cognitive_score: Score cognitif (optionnel)
        decision_type: Type de décision (optionnel)
    """
    try:
        # Incrémenter les compteurs
        if status == "success":
            _zeroia_metrics["decision_count"] += 1
        else:
            _zeroia_metrics["error_count"] += 1
        
        # Mettre à jour le temps de dernière décision
        _zeroia_metrics["last_decision_time"] = datetime.now().isoformat()
        
        # Mettre à jour le score cognitif
        if cognitive_score is not None:
            _zeroia_metrics["cognitive_score"] = cognitive_score
        
        # Ajouter le temps de traitement
        _zeroia_metrics["processing_times"].append(duration)
        
        # Garder seulement les 100 derniers temps
        if len(_zeroia_metrics["processing_times"]) > 100:
            _zeroia_metrics["processing_times"] = _zeroia_metrics["processing_times"][-100:]
        
        # Compter les types de décisions
        if decision_type:
            _zeroia_metrics["decision_types"][decision_type] = _zeroia_metrics["decision_types"].get(decision_type, 0) + 1
        
        logger.debug(f"📊 Métriques mises à jour: {operation} ({status})")
        
    except Exception as e:
        logger.error(f"Erreur mise à jour métriques: {e}")


def get_zeroia_metrics() -> dict:
    """Récupère toutes les métriques ZeroIA"""
    try:
        uptime = time.time() - _zeroia_metrics["uptime_start"]
        
        # Calculer les statistiques de temps de traitement
        processing_times = _zeroia_metrics["processing_times"]
        avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0.0
        max_processing_time = max(processing_times) if processing_times else 0.0
        min_processing_time = min(processing_times) if processing_times else 0.0
        
        return {
            "arkalia_module_name": "zeroia",
            "uptime_seconds": uptime,
            "last_successful_interaction_timestamp": _zeroia_metrics["last_decision_time"],
            "cognitive_score": _zeroia_metrics["cognitive_score"],
            "decision_count": _zeroia_metrics["decision_count"],
            "error_count": _zeroia_metrics["error_count"],
            "success_rate": _zeroia_metrics["decision_count"] / max(_zeroia_metrics["decision_count"] + _zeroia_metrics["error_count"], 1),
            "processing_time": {
                "average_seconds": avg_processing_time,
                "max_seconds": max_processing_time,
                "min_seconds": min_processing_time,
                "total_operations": len(processing_times),
            },
            "decision_types": _zeroia_metrics["decision_types"],
            "status": "operational" if _zeroia_metrics["error_count"] < 10 else "degraded",
        }
        
    except Exception as e:
        logger.error(f"Erreur récupération métriques: {e}")
        return {
            "arkalia_module_name": "zeroia",
            "uptime_seconds": 0,
            "last_successful_interaction_timestamp": None,
            "cognitive_score": 0.0,
            "status": "error",
        }


def generate_prometheus_metrics() -> str:
    """Génère les métriques au format Prometheus"""
    try:
        metrics = get_zeroia_metrics()
        
        prometheus_lines = [
            "# HELP zeroia_uptime_seconds Uptime de ZeroIA en secondes",
            "# TYPE zeroia_uptime_seconds gauge",
            f"zeroia_uptime_seconds {metrics['uptime_seconds']:.2f}",
            "",
            "# HELP zeroia_cognitive_score Score cognitif de ZeroIA",
            "# TYPE zeroia_cognitive_score gauge",
            f"zeroia_cognitive_score {metrics['cognitive_score']:.3f}",
            "",
            "# HELP zeroia_decision_count Nombre total de décisions",
            "# TYPE zeroia_decision_count counter",
            f"zeroia_decision_count {metrics['decision_count']}",
            "",
            "# HELP zeroia_error_count Nombre total d'erreurs",
            "# TYPE zeroia_error_count counter",
            f"zeroia_error_count {metrics['error_count']}",
            "",
            "# HELP zeroia_success_rate Taux de succès",
            "# TYPE zeroia_success_rate gauge",
            f"zeroia_success_rate {metrics['success_rate']:.3f}",
            "",
            "# HELP zeroia_avg_processing_time Temps de traitement moyen",
            "# TYPE zeroia_avg_processing_time gauge",
            f"zeroia_avg_processing_time {metrics['processing_time']['average_seconds']:.3f}",
            "",
            "# HELP zeroia_max_processing_time Temps de traitement maximum",
            "# TYPE zeroia_max_processing_time gauge",
            f"zeroia_max_processing_time {metrics['processing_time']['max_seconds']:.3f}",
            "",
        ]
        
        # Ajouter les métriques par type de décision
        for decision_type, count in metrics["decision_types"].items():
            prometheus_lines.extend([
                f"# HELP zeroia_decision_type_{decision_type} Décisions de type {decision_type}",
                f"# TYPE zeroia_decision_type_{decision_type} counter",
                f"zeroia_decision_type_{decision_type} {count}",
                "",
            ])
        
        return "\n".join(prometheus_lines)
        
    except Exception as e:
        logger.error(f"Erreur génération métriques Prometheus: {e}")
        return "# Erreur génération métriques"


def reset_metrics() -> None:
    """Remet à zéro toutes les métriques"""
    global _zeroia_metrics
    
    _zeroia_metrics = {
        "decision_count": 0,
        "error_count": 0,
        "last_decision_time": None,
        "uptime_start": time.time(),
        "cognitive_score": 0.0,
        "processing_times": [],
        "decision_types": {},
    }
    
    logger.info("🔄 Métriques remises à zéro")


def get_metrics_summary() -> dict:
    """Récupère un résumé des métriques pour l'API"""
    try:
        metrics = get_zeroia_metrics()
        
        return {
            "module": "zeroia",
            "status": metrics["status"],
            "uptime_hours": metrics["uptime_seconds"] / 3600,
            "cognitive_score": metrics["cognitive_score"],
            "total_decisions": metrics["decision_count"],
            "success_rate_percent": metrics["success_rate"] * 100,
            "avg_processing_time_ms": metrics["processing_time"]["average_seconds"] * 1000,
            "last_decision": metrics["last_successful_interaction_timestamp"],
        }
        
    except Exception as e:
        logger.error(f"Erreur résumé métriques: {e}")
        return {
            "module": "zeroia",
            "status": "error",
            "error": str(e),
        } 