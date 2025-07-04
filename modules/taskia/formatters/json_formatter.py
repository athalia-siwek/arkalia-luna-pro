#!/usr/bin/env python3
"""
🌕 TaskIA JSON Formatter
📝 Formateur JSON selon le principe OCP
🔧 Version: 2.0.0
👤 Author: Athalia
📅 Created: 2025-01-27
"""

import json
from typing import Any

from modules.taskia.interfaces.formatter_interface import IFormatter


class JsonFormatter(IFormatter):
    """
    Formateur JSON pour API et intégration.

    Principe OCP : Extension du comportement sans modification
    Principe LSP : Implémente l'interface IFormatter
    """

    def __init__(self, indent: int = 2, ensure_ascii: bool = False):
        """
        Initialise le formateur JSON.

        Args:
            indent: Indentation JSON
            ensure_ascii: Encodage ASCII
        """
        self._indent = indent
        self._ensure_ascii = ensure_ascii

    def format(self, data: dict[str, Any]) -> str:
        """
        Formate les données en JSON.

        Args:
            data: Données à formater

        Returns:
            Données formatées en JSON
        """
        try:
            return json.dumps(
                data,
                indent=self._indent,
                ensure_ascii=self._ensure_ascii,
                default=str,  # Gestion des types non sérialisables
            )
        except Exception as e:
            return json.dumps(
                {"error": "Erreur de formatage JSON", "message": str(e), "data": str(data)}
            )

    def get_format_type(self) -> str:
        """
        Retourne le type de formatage supporté.

        Returns:
            Type de formatage
        """
        return "json"
