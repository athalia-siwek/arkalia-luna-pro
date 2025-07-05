#!/usr/bin/env python3
"""
🌕 TaskIA Summary Formatter
📝 Formateur de résumé selon le principe OCP
🔧 Version: 2.0.0
👤 Author: Athalia
📅 Created: 2025-01-27
"""

from typing import Any

from modules.taskia.interfaces.formatter_interface import IFormatter


class SummaryFormatter(IFormatter):
    """
    Formateur de résumé en format liste.

    Principe OCP : Extension du comportement sans modification
    Principe LSP : Implémente l'interface IFormatter
    """

    def format(self, data: dict[str, Any]) -> str:
        """
        Formate les données en résumé liste.

        Args:
            data: Données à formater

        Returns:
            Données formatées en liste
        """
        if not data:
            return "Aucune donnée à formater"

        formatted_lines = []
        for key, value in data.items():
            # Gestion des valeurs complexes
            if isinstance(value, dict | list):
                formatted_lines.append(f"- {key}: {str(value)}")
            else:
                formatted_lines.append(f"- {key}: {value}")

        return "\n".join(formatted_lines)

    def get_format_type(self) -> str:
        """
        Retourne le type de formatage supporté.

        Returns:
            Type de formatage
        """
        return "summary"
