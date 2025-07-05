#!/usr/bin/env python3
"""
💥 Error Recovery System - Système de récupération d'erreurs consolidé SOLID
Fusion des systèmes error_recovery et zeroia/error_recovery_system

Principes SOLID appliqués :
- SRP : Récupération d'erreurs uniquement
- OCP : Stratégies de récupération extensibles
- LSP : Interfaces polymorphiques pour les stratégies
- ISP : Interfaces spécialisées par type d'erreur
- DIP : Injection de dépendances via factories
"""

from .core import (
    CognitiveOverloadError,
    DecisionIntegrityError,
    ErrorContext,
    ErrorRecoverySystem,
    ErrorSeverity,
    ErrorType,
    RecoveryMetrics,
    RecoveryStrategy,
    SystemRebootRequired,
    ZeroIAError,
)

__all__ = [
    "ErrorRecoverySystem",
    "RecoveryStrategy",
    "ErrorSeverity",
    "ErrorType",
    "RecoveryMetrics",
    "ErrorContext",
    "ZeroIAError",
    "CognitiveOverloadError",
    "DecisionIntegrityError",
    "SystemRebootRequired",
]
