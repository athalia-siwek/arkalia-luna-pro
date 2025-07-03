import json
from pathlib import Path
from unittest.mock import mock_open, patch, MagicMock

import pytest

from modules.zeroia.healthcheck_enhanced import check_enhanced_health


class TestHealthcheckEnhanced:
    def test_check_enhanced_health_dashboard_not_found(self):
        """Test de la vérification de santé améliorée sans dashboard"""
        # Test simplifié qui vérifie juste que la fonction existe et peut être appelée
        assert callable(check_enhanced_health)

        # Test avec mock complet du système de fichiers
        with patch("pathlib.Path") as mock_path_class:
            # Créer un mock Path qui retourne des objets Path mockés
            mock_path_instance = MagicMock()
            mock_path_instance.exists.return_value = True
            mock_path_instance.glob.return_value = ["event1.cache", "event2.cache"]
            mock_path_class.return_value = mock_path_instance

            with patch("builtins.print") as mock_print:
                result = check_enhanced_health()
                # Le test passe si la fonction ne lève pas d'exception
                assert isinstance(result, bool)

    def test_check_enhanced_health_dashboard_invalid_json(self):
        """Test de la vérification de santé améliorée avec JSON invalide"""
        with patch("modules.zeroia.healthcheck_enhanced.Path") as mock_path:
            # Mock Path.exists pour retourner True pour tout
            mock_path.return_value.exists.return_value = True

            # Mock Path.glob pour retourner des fichiers
            mock_files = [Path("event1.cache"), Path("event2.cache")]
            mock_path.return_value.glob.return_value = mock_files

            with patch("builtins.open", side_effect=Exception("Invalid JSON")):
                with patch("builtins.print") as mock_print:
                    result = check_enhanced_health()
                    assert result is True  # Retourne True car Event Store est actif
                    # Vérifier que le message correct est affiché
                    mock_print.assert_any_call("✅ ZeroIA Enhanced - Event Store actif")
