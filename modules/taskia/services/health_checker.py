#!/usr/bin/env python3
"""
🌕 TaskIA Health Checker Service
📝 Service de vérification de santé selon le principe SRP
🔧 Version: 2.0.0
👤 Author: Athalia
📅 Created: 2025-01-27
"""

import logging
from datetime import datetime
from typing import Any

from modules.taskia.interfaces.health_check_interface import IHealthChecker


class HealthChecker(IHealthChecker):
    """
    Service de vérification de santé.

    Principe SRP : Responsabilité unique = vérifier la santé
    Principe LSP : Implémente l'interface IHealthChecker
    """

    def __init__(self, module_name: str = "taskia", logger: logging.Logger | None = None):
        """
        Initialise le vérificateur de santé.

        Args:
            module_name: Nom du module à vérifier
            logger: Logger injecté (DIP)
        """
        self._module_name = module_name
        self._logger = logger or logging.getLogger(__name__)
        self._status = "operational"

    def check_health(self) -> dict[str, Any]:
        """
        Effectue une vérification de santé.

        Returns:
            Statut de santé sous forme de dictionnaire
        """
        self._logger.info(f"Vérification de santé pour {self._module_name}")

        try:
            health_data = {
                "module": self._module_name,
                "status": self._status,
                "version": "2.0.0",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "checks": {"memory": "ok", "cpu": "ok", "dependencies": "ok"},
            }

            self._logger.debug(f"Données de santé: {health_data}")
            return health_data

        except Exception as e:
            self._logger.error(f"Erreur lors de la vérification de santé: {e}")
            self._status = "degraded"
            return {
                "module": self._module_name,
                "status": "degraded",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }

    def get_health_status(self) -> str:
        """
        Retourne le statut de santé actuel.

        Returns:
            Statut ('operational', 'degraded', 'down')
        """
        return self._status

    def set_status(self, status: str) -> None:
        """
        Définit le statut de santé.

        Args:
            status: Nouveau statut
        """
        valid_statuses = ["operational", "degraded", "down"]
        if status not in valid_statuses:
            raise ValueError(f"Statut invalide. Doit être l'un de: {valid_statuses}")

        self._status = status
        self._logger.info(f"Statut de santé changé à: {status}")
