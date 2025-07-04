#!/usr/bin/env python3
"""
🌕 TaskIA Service Factory
📝 Factory pour les services selon le principe DIP
🔧 Version: 2.0.0
👤 Author: Athalia
📅 Created: 2025-01-27
"""

import logging
from typing import Optional

from modules.taskia.factories.formatter_factory import FormatterFactory
from modules.taskia.interfaces.formatter_interface import IFormatter
from modules.taskia.interfaces.health_check_interface import IHealthChecker
from modules.taskia.interfaces.task_processor_interface import ITaskProcessor
from modules.taskia.services.health_checker import HealthChecker
from modules.taskia.services.logger_service import LoggerService
from modules.taskia.services.task_processor import TaskProcessor


class ServiceFactory:
    """
    Factory pour créer des services avec injection de dépendances.

    Principe DIP : Dépend des interfaces, pas des implémentations
    Principe SRP : Responsabilité unique = créer des services
    """

    def __init__(self, formatter_factory: FormatterFactory | None = None):
        """
        Initialise la factory de services.

        Args:
            formatter_factory: Factory de formateurs (injection)
        """
        self._formatter_factory = formatter_factory or FormatterFactory()
        self._logger_service = LoggerService()

    def create_task_processor(
        self, format_type: str = "summary", **formatter_kwargs
    ) -> ITaskProcessor:
        """
        Crée un processeur de tâches avec injection de dépendances.

        Args:
            format_type: Type de formateur à utiliser
            **formatter_kwargs: Paramètres du formateur

        Returns:
            Processeur de tâches configuré
        """
        formatter = self._formatter_factory.create_formatter(format_type, **formatter_kwargs)
        logger = self._logger_service.get_logger()

        return TaskProcessor(formatter=formatter, logger=logger)

    def create_health_checker(self, module_name: str = "taskia") -> IHealthChecker:
        """
        Crée un vérificateur de santé.

        Args:
            module_name: Nom du module à vérifier

        Returns:
            Vérificateur de santé
        """
        logger = self._logger_service.get_logger()
        return HealthChecker(module_name=module_name, logger=logger)

    def create_logger_service(self, module_name: str = "taskia") -> LoggerService:
        """
        Crée un service de logging.

        Args:
            module_name: Nom du module pour le logger

        Returns:
            Service de logging
        """
        return LoggerService(module_name=module_name)

    def get_formatter_factory(self) -> FormatterFactory:
        """
        Retourne la factory de formateurs.

        Returns:
            Factory de formateurs
        """
        return self._formatter_factory

    def get_logger_service(self) -> LoggerService:
        """
        Retourne le service de logging.

        Returns:
            Service de logging
        """
        return self._logger_service
