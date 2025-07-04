#!/usr/bin/env python3
"""
🌕 TaskIA Core Refactored
📝 Core refactorisé selon les principes SOLID
🔧 Version: 2.0.0
👤 Author: Athalia
📅 Created: 2025-01-27
"""

from typing import Dict, Any
from interfaces import ITaskProcessor
from factories import ServiceFactory


class TaskIACore:
    """
    Core refactorisé de TaskIA.
    
    Principe DIP : Dépend des interfaces, pas des implémentations
    Principe SRP : Responsabilité unique = orchestrer les services
    Principe OCP : Extensible sans modification
    """
    
    def __init__(self, service_factory: ServiceFactory | None = None):
        """
        Initialise le core avec injection de dépendances.
        
        Args:
            service_factory: Factory de services (injection DIP)
        """
        self._service_factory = service_factory or ServiceFactory()
        self._task_processor: ITaskProcessor | None = None
        self._health_checker = None
        self._logger_service = self._service_factory.get_logger_service()
        self._logger = self._logger_service.get_logger()
        
        # Initialisation par défaut
        self._initialize_default_services()
    
    def _initialize_default_services(self) -> None:
        """Initialise les services par défaut."""
        self._task_processor = self._service_factory.create_task_processor("summary")
        self._health_checker = self._service_factory.create_health_checker("taskia")
        self._logger.info("🌕 Services TaskIA initialisés")
    
    def process_task(self, context: Dict[str, Any], format_type: str = "summary", **formatter_kwargs) -> str:
        """
        Traite une tâche avec le formatage spécifié.
        
        Args:
            context: Contexte à traiter
            format_type: Type de formatage ('summary', 'json', 'markdown', 'html')
            **formatter_kwargs: Paramètres du formateur
            
        Returns:
            Résultat formaté
        """
        self._logger.info(f"Traitement de tâche avec formatage {format_type}")
        
        # Création dynamique du processeur avec le bon formateur
        processor = self._service_factory.create_task_processor(format_type, **formatter_kwargs)
        
        try:
            result = processor.process(context)
            self._logger.info("Tâche traitée avec succès")
            return result
        except Exception as e:
            self._logger.error(f"Erreur lors du traitement: {e}")
            raise
    
    def check_health(self) -> Dict[str, Any]:
        """
        Vérifie la santé du module.
        
        Returns:
            Statut de santé
        """
        if self._health_checker:
            return self._health_checker.check_health()
        return {"error": "Health checker not initialized"}
    
    def get_available_formatters(self) -> list[str]:
        """
        Retourne les formateurs disponibles.
        
        Returns:
            Liste des formateurs disponibles
        """
        return self._service_factory.get_formatter_factory().get_available_formatters()
    
    def set_health_status(self, status: str) -> None:
        """
        Définit le statut de santé.
        
        Args:
            status: Nouveau statut
        """
        if self._health_checker and hasattr(self._health_checker, 'set_status'):
            self._health_checker.set_status(status)
        else:
            self._logger.warning("Health checker does not support set_status")
    
    def get_logger(self):
        """
        Retourne le logger du service.
        
        Returns:
            Logger configuré
        """
        return self._logger


# Fonction de compatibilité avec l'ancien code
def taskia_main(context: Dict[str, Any]) -> str:
    """
    Fonction de compatibilité avec l'ancien code.
    
    Args:
        context: Contexte à traiter
        
    Returns:
        Résultat formaté
    """
    core = TaskIACore()
    return core.process_task(context)


# Fonction de compatibilité avec l'ancien code
def format_summary(context: Dict[str, Any]) -> str:
    """
    Fonction de compatibilité avec l'ancien code.
    
    Args:
        context: Contexte à formater
        
    Returns:
        Résumé formaté
    """
    return taskia_main(context) 