#!/usr/bin/env python3

"""
🧠 modules/zeroia/__init__.py
ZeroIA Module - Système de raisonnement intelligent Arkalia-LUNA v3.0

Module principal de raisonnement et prise de décision automatisée.
Intègre Circuit Breaker, Event Sourcing, Error Recovery et Graceful Degradation.
"""

__version__ = "3.0.0-enhanced"
__author__ = "Arkalia-LUNA Team"
__description__ = "Système de raisonnement intelligent avec protection avancée"

# Imports principaux
from .reason_loop_enhanced import (
    reason_loop_enhanced_with_recovery,
    initialize_components_with_recovery,
    get_circuit_status,
    get_event_analytics,
    get_error_recovery_status,
    get_degradation_status,
)

from .orchestrator_enhanced import (
    ZeroIAOrchestrator,
    orchestrate_zeroia_enhanced,
)

from .circuit_breaker import (
    CircuitBreaker,
    CognitiveOverloadError,
    DecisionIntegrityError,
)

from .event_store import (
    EventStore,
    EventType,
)

from .error_recovery_system import (
    ErrorRecoverySystem,
    create_error_recovery_system,
)

from .graceful_degradation import (
    GracefulDegradationSystem,
    DegradationLevel,
    create_graceful_degradation_system,
)

from .confidence_score import (
    ConfidenceScorer,
)

from .model_integrity import (
    ModelIntegrityMonitor,
    validate_decision_integrity,
)

from .core import (
    ZeroIACore,
    get_zeroia_core,
    quick_decision,
)

# Exports publics
__all__ = [
    # Fonctions principales
    "reason_loop_enhanced_with_recovery",
    "initialize_components_with_recovery",
    "orchestrate_zeroia_enhanced",
    
    # Classes principales
    "ZeroIACore",
    "ZeroIAOrchestrator",
    "CircuitBreaker",
    "EventStore",
    "ErrorRecoverySystem", 
    "GracefulDegradationSystem",
    "ConfidenceScorer",
    "ModelIntegrityMonitor",
    
    # Enums et types
    "EventType",
    "DegradationLevel",
    
    # Exceptions
    "CognitiveOverloadError", 
    "DecisionIntegrityError",
    
    # Utilitaires
    "get_circuit_status",
    "get_event_analytics",
    "get_error_recovery_status",
    "get_degradation_status",
    "validate_decision_integrity",
    "get_zeroia_core",
    "quick_decision",
    
    # Métadonnées
    "__version__",
    "__author__",
    "__description__",
]

# Configuration par défaut
DEFAULT_CONFIG = {
    "circuit_breaker": {
        "failure_threshold": 5,
        "recovery_timeout": 60,
    },
    "event_store": {
        "max_events": 10000,
        "retention_days": 30,
    },
    "error_recovery": {
        "max_retries": 3,
        "backoff_factor": 2.0,
    },
    "graceful_degradation": {
        "enable_degradation": True,
        "degradation_threshold": 0.3,
    },
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
        from . import reason_loop_enhanced
        from . import circuit_breaker
        from . import event_store
        
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
