#!/usr/bin/env python3
"""
🌕 TaskIA Logger Service
📝 Service de logging selon le principe SRP
🔧 Version: 2.0.0
👤 Author: Athalia
📅 Created: 2025-01-27
"""

import logging
from typing import Optional


class LoggerService:
    """
    Service de logging centralisé.
    
    Principe SRP : Responsabilité unique = gérer les logs
    Principe DIP : Fournit des loggers injectables
    """
    
    def __init__(self, module_name: str = "taskia"):
        """
        Initialise le service de logging.
        
        Args:
            module_name: Nom du module pour le logger
        """
        self._module_name = module_name
        self._logger = logging.getLogger(f"arkalia.{module_name}")
        self._setup_logger()
    
    def _setup_logger(self) -> None:
        """Configure le logger avec les paramètres par défaut."""
        if not self._logger.handlers:
            self._logger.setLevel(logging.INFO)
            
            # Handler console
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # Formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(formatter)
            
            self._logger.addHandler(console_handler)
    
    def get_logger(self) -> logging.Logger:
        """
        Retourne le logger configuré.
        
        Returns:
            Logger configuré
        """
        return self._logger
    
    def set_level(self, level: int) -> None:
        """
        Définit le niveau de logging.
        
        Args:
            level: Niveau de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self._logger.setLevel(level)
    
    def log_operation(self, operation: str, details: Optional[str] = None) -> None:
        """
        Log une opération avec des détails optionnels.
        
        Args:
            operation: Nom de l'opération
            details: Détails optionnels
        """
        message = f"🌕 {operation}"
        if details:
            message += f" - {details}"
        
        self._logger.info(message)
    
    def log_error(self, error: str, context: Optional[str] = None) -> None:
        """
        Log une erreur avec un contexte optionnel.
        
        Args:
            error: Message d'erreur
            context: Contexte optionnel
        """
        message = f"❌ {error}"
        if context:
            message += f" - Contexte: {context}"
        
        self._logger.error(message) 