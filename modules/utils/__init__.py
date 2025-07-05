#!/usr/bin/env python3
"""
🛠️ Utils Module - Module utilitaire consolidé SOLID
Regroupe tous les utilitaires du système Arkalia-LUNA

Architecture SOLID :
- error_recovery/ : Récupération d'erreurs unifiée
- validators/ : Validation croisée et autres validateurs
- helpers/ : Utilitaires généraux (IO, cache, etc.)
- taskia/ : Gestion de tâches (déjà SOLID)

Principes SOLID appliqués :
- SRP : Chaque sous-module a une responsabilité unique
- OCP : Extensible via interfaces et factories
- LSP : Interfaces polymorphiques
- ISP : Interfaces spécialisées
- DIP : Injection de dépendances
"""

from .error_recovery import ErrorRecoverySystem, ErrorSeverity, RecoveryStrategy
from .helpers import atomic_write, locked_read, save_json_safe, save_toml_safe
from .validators import CrossModuleValidator, ValidationResult

__version__ = "1.0.0"
__author__ = "Arkalia-LUNA Team"

__all__ = [
    # Error Recovery
    "ErrorRecoverySystem",
    "RecoveryStrategy",
    "ErrorSeverity",
    # Validators
    "CrossModuleValidator",
    "ValidationResult",
    # Helpers
    "atomic_write",
    "locked_read",
    "save_toml_safe",
    "save_json_safe",
]
