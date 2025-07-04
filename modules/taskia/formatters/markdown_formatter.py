#!/usr/bin/env python3
"""
🌕 TaskIA Markdown Formatter
📝 Formateur Markdown selon le principe OCP
🔧 Version: 2.0.0
👤 Author: Athalia
📅 Created: 2025-01-27
"""

from typing import Dict, Any
from modules.taskia.interfaces.formatter_interface import IFormatter


class MarkdownFormatter(IFormatter):
    """
    Formateur Markdown pour documentation.
    
    Principe OCP : Extension du comportement sans modification
    Principe LSP : Implémente l'interface IFormatter
    """
    
    def __init__(self, title: str = "Données TaskIA"):
        """
        Initialise le formateur Markdown.
        
        Args:
            title: Titre du document Markdown
        """
        self._title = title
    
    def format(self, data: Dict[str, Any]) -> str:
        """
        Formate les données en Markdown.
        
        Args:
            data: Données à formater
            
        Returns:
            Données formatées en Markdown
        """
        if not data:
            return f"# {self._title}\n\n*Aucune donnée disponible*"
        
        markdown_lines = [f"# {self._title}\n"]
        
        for key, value in data.items():
            # Titre de section
            markdown_lines.append(f"## {key.title()}")
            
            # Contenu selon le type
            if isinstance(value, dict):
                markdown_lines.append(self._format_dict(value))
            elif isinstance(value, list):
                markdown_lines.append(self._format_list(value))
            else:
                markdown_lines.append(f"{value}\n")
        
        return "\n".join(markdown_lines)
    
    def _format_dict(self, data: Dict[str, Any]) -> str:
        """Formate un dictionnaire en Markdown."""
        lines = []
        for k, v in data.items():
            lines.append(f"- **{k}**: {v}")
        return "\n".join(lines) + "\n"
    
    def _format_list(self, data: list) -> str:
        """Formate une liste en Markdown."""
        lines = []
        for item in data:
            lines.append(f"- {item}")
        return "\n".join(lines) + "\n"
    
    def get_format_type(self) -> str:
        """
        Retourne le type de formatage supporté.
        
        Returns:
            Type de formatage
        """
        return "markdown" 