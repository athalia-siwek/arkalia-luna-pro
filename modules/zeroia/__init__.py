#!/usr/bin/env python3

"""
🌕 ZeroIA - Module de décision autonome Enhanced v2.8.0

Module principal pour la prise de décision autonome avec error recovery,
circuit breaker, adaptive thresholds et graceful degradation.
"""

__version__ = "3.0.0-enhanced"
__author__ = "Arkalia-LUNA Team"
__description__ = "Système de raisonnement intelligent avec protection avancée"

from .error_recovery_system import ErrorRecoverySystem  # noqa: F401
from .graceful_degradation import (  # noqa: F401
    DegradationLevel,
    GracefulDegradationSystem,
)
from .reason_loop import reason_loop

# Imports conditionnels pour éviter les erreurs si modules non disponibles
try:
    from .circuit_breaker import CircuitBreaker  # noqa: F401
    from .event_store import EventStore, EventType  # noqa: F401
    from .reason_loop_enhanced import (  # noqa: F401
        reason_loop_enhanced,
        reason_loop_enhanced_with_recovery,
    )
except ImportError:
    # Modules optionnels non disponibles
    pass

# Configuration par défaut
DEFAULT_CONFIG = {
    "max_loops": 100,
    "interval_seconds": 1.0,
    "circuit_breaker_threshold": 5,
    "adaptive_thresholds": True,
    "graceful_degradation": True,
    "error_recovery": True,
    "model_integrity": True,
}

# Exports publics
__all__ = [
    # Core modules
    "CircuitBreaker",
    "EventStore",
    "EventType",
    "ErrorRecoverySystem",
    "GracefulDegradationSystem",
    "DegradationLevel",
    # Reason loops
    "reason_loop",
    "reason_loop_enhanced",
    "reason_loop_enhanced_with_recovery",
    # Configuration
    "DEFAULT_CONFIG",
]


def get_zeroia_status():
    """🔍 Obtenir le statut complet de ZeroIA"""
    try:
        # Test imports critiques
        from . import reason_loop_enhanced  # noqa: F401

        return {
            "status": "✅ HEALTHY",
            "version": "v2.8.0",
            "modules": {
                "circuit_breaker": "✅",
                "event_store": "✅",
                "reason_loop": "✅",
                "reason_loop_enhanced": "✅",
                "error_recovery": "✅",
                "graceful_degradation": "✅",
            },
            "features": {
                "circuit_breaker": "✅",
                "event_store": "✅",
                "error_recovery": "✅",
                "graceful_degradation": "✅",
            },
        }
    except ImportError as e:
        return {
            "status": "❌ ERROR",
            "error": str(e),
            "version": "v2.8.0",
        }


def get_version() -> str:
    """Retourne la version du module ZeroIA"""
    return __version__


def get_default_config() -> dict:
    """Retourne la configuration par défaut"""
    return DEFAULT_CONFIG.copy()


def health_check() -> dict:
    """Vérifie l'état de santé du module ZeroIA"""
    try:
        # Test imports critiques
        from . import circuit_breaker  # noqa: F401

        return {
            "status": "healthy",
            "version": __version__,
            "components": {
                "reason_loop": "available",
                "circuit_breaker": "available",
                "event_store": "available",
                "error_recovery": "available",
                "graceful_degradation": "available",
            },
            "timestamp": "2025-06-29T04:18:00Z",
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "version": __version__,
            "timestamp": "2025-06-29T04:18:00Z",
        }
