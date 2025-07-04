#!/usr/bin/env python3
"""
🌕 TaskIA Health Check Interface
📝 Interface pour les vérifications de santé selon le principe ISP
🔧 Version: 2.0.0
👤 Author: Athalia
📅 Created: 2025-01-27
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class IHealthChecker(ABC):
    """
    Interface pour les vérifications de santé.
    
    Principe ISP : Interface spécifique pour la santé
    Principe LSP : Permet la substitution de vérificateurs
    """
    
    @abstractmethod
    def check_health(self) -> Dict[str, Any]:
        """
        Effectue une vérification de santé.
        
        Returns:
            Statut de santé sous forme de dictionnaire
        """
        pass
    
    @abstractmethod
    def get_health_status(self) -> str:
        """
        Retourne le statut de santé actuel.
        
        Returns:
            Statut ('operational', 'degraded', 'down')
        """
        pass
    
    @abstractmethod
    def set_status(self, status: str) -> None:
        """
        Définit le statut de santé.
        
        Args:
            status: Nouveau statut
        """
        pass 