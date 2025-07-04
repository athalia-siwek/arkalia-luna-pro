#!/usr/bin/env python3
"""
🌕 TaskIA Task Processor Service
📝 Service de traitement des tâches selon le principe SRP
🔧 Version: 2.0.0
👤 Author: Athalia
📅 Created: 2025-01-27
"""

import logging
from typing import Dict, Any
from modules.taskia.interfaces.task_processor_interface import ITaskProcessor
from modules.taskia.interfaces.formatter_interface import IFormatter


class TaskProcessor(ITaskProcessor):
    """
    Service de traitement des tâches.
    
    Principe SRP : Responsabilité unique = traiter les tâches
    Principe DIP : Dépend des interfaces, pas des implémentations
    """
    
    def __init__(self, formatter: IFormatter, logger: logging.Logger | None = None):
        """
        Initialise le processeur de tâches.
        
        Args:
            formatter: Formateur injecté (DIP)
            logger: Logger injecté (DIP)
        """
        self._formatter = formatter
        self._logger = logger or logging.getLogger(__name__)
    
    def process(self, context: Dict[str, Any]) -> str:
        """
        Traite le contexte et génère un résultat formaté.
        
        Args:
            context: Contexte à traiter
            
        Returns:
            Résultat formaté
        """
        self._logger.info(f"Traitement du contexte avec {self._formatter.get_format_type()}")
        
        if not self.validate_context(context):
            raise ValueError("Contexte invalide")
        
        return self._formatter.format(context)
    
    def validate_context(self, context: Dict[str, Any]) -> bool:
        """
        Valide le contexte d'entrée.
        
        Args:
            context: Contexte à valider
            
        Returns:
            True si le contexte est valide
        """
        if not isinstance(context, dict):
            self._logger.error("Le contexte doit être un dictionnaire")
            return False
        
        if not context:
            self._logger.warning("Contexte vide")
            return False
        
        return True 