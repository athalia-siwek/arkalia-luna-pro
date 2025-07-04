#!/usr/bin/env python3
"""
🌕 TaskIA Task Processor Interface
📝 Interface pour le traitement des tâches selon le principe ISP
🔧 Version: 2.0.0
👤 Author: Athalia
📅 Created: 2025-01-27
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class ITaskProcessor(ABC):
    """
    Interface pour le traitement des tâches.
    
    Principe ISP : Interface spécifique pour le traitement
    Principe LSP : Permet la substitution de processeurs
    """
    
    @abstractmethod
    def process(self, context: Dict[str, Any]) -> str:
        """
        Traite le contexte et génère un résultat formaté.
        
        Args:
            context: Contexte à traiter
            
        Returns:
            Résultat formaté
        """
        pass
    
    @abstractmethod
    def validate_context(self, context: Dict[str, Any]) -> bool:
        """
        Valide le contexte d'entrée.
        
        Args:
            context: Contexte à valider
            
        Returns:
            True si le contexte est valide
        """
        pass 