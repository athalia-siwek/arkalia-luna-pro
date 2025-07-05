"""Tests pour taskia/core.py"""

from unittest.mock import patch

import pytest

from modules.taskia.core import taskia_main


def test_taskia_main() -> None:
    """Test de la fonction principale taskia_main"""
    context = {
        "module": "test_module",
        "action": "test_action",
        "status": "success",
        "details": {"param1": "value1", "param2": 42},
    }

    with patch("modules.taskia.core.format_summary") as mock_format:
        mock_format.return_value = "Test summary"
        result = taskia_main(context)

        # Vérifier que format_summary a été appelé avec le bon contexte
        mock_format.assert_called_once_with(context)

        # Vérifier que le résultat est correct
        assert result == "Test summary"
