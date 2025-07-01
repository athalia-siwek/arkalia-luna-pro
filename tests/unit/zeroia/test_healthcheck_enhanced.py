import json
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

from modules.zeroia.healthcheck_enhanced import check_enhanced_health


class TestHealthcheckEnhanced:
    def test_check_enhanced_health_dashboard_not_found(self):
        """Test de la vérification de santé améliorée sans dashboard"""
        mock_files = [Path("event1.cache"), Path("event2.cache")]

        def mock_exists(path):
            path_str = str(path)
            if "dashboard" in path_str:
                return False
            if "events" in path_str:
                return True
            return True

        with patch("pathlib.Path.exists", side_effect=mock_exists):
            with patch("pathlib.Path.glob", return_value=iter(mock_files)):
                with patch("builtins.print") as mock_print:
                    result = check_enhanced_health()
                    assert result is True
                    mock_print.assert_called_with("✅ ZeroIA Enhanced - Event Store actif")

    def test_check_enhanced_health_dashboard_invalid_json(self):
        """Test de la vérification de santé améliorée avec JSON invalide"""
        mock_files = [Path("event1.cache"), Path("event2.cache")]

        def mock_exists(path):
            return True

        with patch("pathlib.Path.exists", side_effect=mock_exists):
            with patch("pathlib.Path.glob", return_value=iter(mock_files)):
                with patch("builtins.open", side_effect=Exception("Invalid JSON")):
                    with patch("builtins.print") as mock_print:
                        result = check_enhanced_health()
                        assert result is True  # Retourne True car Event Store est actif
                        mock_print.assert_called_with("✅ ZeroIA Enhanced - Event Store actif")
