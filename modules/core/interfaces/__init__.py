"""
🔗 Interfaces SOLID pour le Core
🎯 Définition des contrats entre composants
"""

from .health_interface import IHealthCheck
from .module_interface import IModule
from .orchestrator_interface import IOrchestrator

__all__ = ["IModule", "IOrchestrator", "IHealthCheck"]
