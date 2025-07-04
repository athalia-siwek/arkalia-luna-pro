#!/usr/bin/env python3
"""
🌕 TaskIA Formatter Factory
📝 Factory pour les formateurs selon les principes OCP et DIP
🔧 Version: 2.0.0
👤 Author: Athalia
📅 Created: 2025-01-27
"""

from typing import Dict, Type
from interfaces import IFormatter
from formatters import (
    SummaryFormatter,
    JsonFormatter,
    MarkdownFormatter,
    HtmlFormatter
)


class FormatterFactory:
    """
    Factory pour créer des formateurs.
    
    Principe OCP : Extension sans modification
    Principe DIP : Dépend des interfaces
    """
    
    def __init__(self):
        """Initialise la factory avec les formateurs disponibles."""
        self._formatters: Dict[str, Type[IFormatter]] = {
            "summary": SummaryFormatter,
            "json": JsonFormatter,
            "markdown": MarkdownFormatter,
            "html": HtmlFormatter
        }
    
    def create_formatter(self, format_type: str, **kwargs) -> IFormatter:
        """
        Crée un formateur selon le type demandé.
        
        Args:
            format_type: Type de formateur ('summary', 'json', 'markdown', 'html')
            **kwargs: Paramètres spécifiques au formateur
            
        Returns:
            Instance du formateur
            
        Raises:
            ValueError: Si le type de formateur n'est pas supporté
        """
        if format_type not in self._formatters:
            available = ", ".join(self._formatters.keys())
            raise ValueError(f"Type de formateur '{format_type}' non supporté. Disponibles: {available}")
        
        formatter_class = self._formatters[format_type]
        return formatter_class(**kwargs)
    
    def get_available_formatters(self) -> list[str]:
        """
        Retourne la liste des formateurs disponibles.
        
        Returns:
            Liste des types de formateurs disponibles
        """
        return list(self._formatters.keys())
    
    def register_formatter(self, format_type: str, formatter_class: Type[IFormatter]) -> None:
        """
        Enregistre un nouveau formateur.
        
        Args:
            format_type: Type du formateur
            formatter_class: Classe du formateur
        """
        if not issubclass(formatter_class, IFormatter):
            raise ValueError("La classe doit implémenter IFormatter")
        
        self._formatters[format_type] = formatter_class
    
    def has_formatter(self, format_type: str) -> bool:
        """
        Vérifie si un formateur est disponible.
        
        Args:
            format_type: Type de formateur
            
        Returns:
            True si le formateur est disponible
        """
        return format_type in self._formatters 