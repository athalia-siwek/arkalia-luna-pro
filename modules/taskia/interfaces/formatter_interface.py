#!/usr/bin/env python3
"""
🌕 TaskIA Formatter Interface
📝 Interface pour les formateurs selon le principe ISP
🔧 Version: 2.0.0
👤 Author: Athalia
📅 Created: 2025-01-27
"""

from abc import ABC, abstractmethod
from typing import Any


class IFormatter(ABC):
    """
    Interface pour les formateurs de données.

    Principe ISP : Interface spécifique pour le formatage
    Principe LSP : Permet la substitution de formateurs
    """

    @abstractmethod
    def format(self, data: dict[str, Any]) -> str:
        """
        Formate les données selon le type de formateur.

        Args:
            data: Données à formater

        Returns:
            Données formatées sous forme de chaîne
        """
        pass

    @abstractmethod
    def get_format_type(self) -> str:
        """
        Retourne le type de formatage supporté.

        Returns:
            Type de formatage (ex: 'summary', 'json', 'markdown')
        """
        pass
