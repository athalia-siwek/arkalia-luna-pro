#!/usr/bin/env python3
# 🧪 tests/unit/zeroia/test_healthcheck_enhanced_fixed.py
"""Tests unitaires corrigés pour zeroia/healthcheck_enhanced.py"""

import json
import sys
from pathlib import Path
from unittest.mock import Mock, mock_open, patch

import pytest
import toml

from modules.zeroia.healthcheck_enhanced import (
    check_enhanced_health,
    check_zeroia_health,
    load_healthcheck_config,
)


class TestLoadHealthcheckConfig:
    """Tests pour load_healthcheck_config()"""

    def test_load_healthcheck_config_success(self):
        """Test chargement réussi de la configuration."""
        config_data = {"enabled": True, "interval": 45, "timeout": 10}

        with patch("builtins.open", mock_open(read_data=toml.dumps(config_data))):
            result = load_healthcheck_config()

        assert result == config_data
        assert result["enabled"] is True
        assert result["interval"] == 45

    def test_load_healthcheck_config_file_not_found(self):
        """Test gestion du fichier de configuration manquant."""
        with patch("builtins.open", side_effect=FileNotFoundError):
            result = load_healthcheck_config()

        assert result == {"enabled": True, "interval": 30}
        assert result["enabled"] is True
        assert result["interval"] == 30

    def test_load_healthcheck_config_invalid_toml(self):
        """Test gestion d'un fichier TOML invalide."""
        with patch("builtins.open", mock_open(read_data="invalid toml content")):
            result = load_healthcheck_config()

        assert result == {"enabled": False, "interval": 60}
        assert result["enabled"] is False
        assert result["interval"] == 60

    def test_load_healthcheck_config_permission_error(self):
        """Test gestion d'erreur de permission."""
        with patch("builtins.open", side_effect=PermissionError):
            result = load_healthcheck_config()

        assert result == {"enabled": False, "interval": 60}
        assert result["enabled"] is False


class TestCheckZeroiaHealth:
    """Tests pour check_zeroia_health()"""

    def test_check_zeroia_health_active(self):
        """Test healthcheck avec état actif."""
        state_data = {"status": "active", "last_update": "2025-01-27"}

        with patch("pathlib.Path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=toml.dumps(state_data))):
                result = check_zeroia_health()

        assert result is True

    def test_check_zeroia_health_inactive(self):
        """Test healthcheck avec état inactif."""
        state_data = {"status": "inactive", "last_update": "2025-01-27"}

        with patch("pathlib.Path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=toml.dumps(state_data))):
                result = check_zeroia_health()

        assert result is False

    def test_check_zeroia_health_missing_status(self):
        """Test healthcheck avec statut manquant."""
        state_data = {"last_update": "2025-01-27"}

        with patch("pathlib.Path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=toml.dumps(state_data))):
                result = check_zeroia_health()

        assert result is False

    def test_check_zeroia_health_file_not_found(self):
        """Test healthcheck avec fichier d'état manquant."""
        with patch("pathlib.Path.exists", return_value=False):
            result = check_zeroia_health()

        assert result is False

    def test_check_zeroia_health_invalid_toml(self):
        """Test healthcheck avec TOML invalide."""
        with patch("pathlib.Path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data="invalid toml")):
                result = check_zeroia_health()

        assert result is False

    def test_check_zeroia_health_permission_error(self):
        """Test healthcheck avec erreur de permission."""
        with patch("pathlib.Path.exists", return_value=True):
            with patch("builtins.open", side_effect=PermissionError):
                result = check_zeroia_health()

        assert result is False


class TestCheckEnhancedHealth:
    """Tests pour check_enhanced_health()"""

    def test_check_enhanced_health_success_with_dashboard(self):
        """Test healthcheck enhanced avec dashboard actif."""
        # Mock pour events_dir
        mock_events_dir = Mock()
        mock_events_dir.exists.return_value = True
        mock_events_dir.glob.return_value = [Mock()]  # Fichiers récents

        # Mock pour dashboard_file
        mock_dashboard_file = Mock()
        mock_dashboard_file.exists.return_value = True

        # Mock Path constructor
        def mock_path_constructor(path_str):
            if str(path_str) == "cache/zeroia_events/events":
                return mock_events_dir
            elif str(path_str) == "state/zeroia_dashboard.json":
                return mock_dashboard_file
            else:
                return Mock()

        dashboard_data = {"status": "active", "last_decision": "2025-01-27"}

        with patch("modules.zeroia.healthcheck_enhanced.Path", side_effect=mock_path_constructor):
            with patch("builtins.open", mock_open(read_data=json.dumps(dashboard_data))):
                with patch("builtins.print") as mock_print:
                    result = check_enhanced_health()

        assert result is True
        mock_print.assert_called_with("✅ ZeroIA Enhanced OK")

    def test_check_enhanced_health_success_without_dashboard(self):
        """Test healthcheck enhanced sans dashboard."""
        # Mock pour events_dir
        mock_events_dir = Mock()
        mock_events_dir.exists.return_value = True
        mock_events_dir.glob.return_value = [Mock()]  # Fichiers récents

        # Mock pour dashboard_file
        mock_dashboard_file = Mock()
        mock_dashboard_file.exists.return_value = False

        # Mock Path constructor
        def mock_path_constructor(path_str):
            if str(path_str) == "cache/zeroia_events/events":
                return mock_events_dir
            elif str(path_str) == "state/zeroia_dashboard.json":
                return mock_dashboard_file
            else:
                return Mock()

        with patch("modules.zeroia.healthcheck_enhanced.Path", side_effect=mock_path_constructor):
            with patch("builtins.print") as mock_print:
                result = check_enhanced_health()

        assert result is True
        mock_print.assert_called_with("✅ ZeroIA Enhanced - Event Store actif")

    def test_check_enhanced_health_events_dir_missing(self):
        """Test healthcheck enhanced avec répertoire events manquant."""
        # Mock Path pour events_dir
        mock_events_dir = Mock()
        mock_events_dir.exists.return_value = False

        # Mock Path constructor
        def mock_path_constructor(path_str):
            if "events" in path_str:
                return mock_events_dir
            else:
                return Mock()

        with patch("modules.zeroia.healthcheck_enhanced.Path", side_effect=mock_path_constructor):
            with patch("builtins.print") as mock_print:
                result = check_enhanced_health()

        assert result is False
        mock_print.assert_any_call("❌ Event Store non trouvé")

    def test_check_enhanced_health_no_recent_files(self):
        """Test healthcheck enhanced sans fichiers récents."""
        # Mock Path pour events_dir
        mock_events_dir = Mock()
        mock_events_dir.exists.return_value = True
        mock_events_dir.glob.return_value = []  # Pas de fichiers récents

        # Mock Path constructor
        def mock_path_constructor(path_str):
            if "events" in path_str:
                return mock_events_dir
            else:
                return Mock()

        with patch("modules.zeroia.healthcheck_enhanced.Path", side_effect=mock_path_constructor):
            with patch("builtins.print") as mock_print:
                result = check_enhanced_health()

        assert result is False
        mock_print.assert_any_call("❌ Aucun événement récent")

    def test_check_enhanced_health_dashboard_error(self):
        """Test healthcheck enhanced avec erreur de lecture dashboard."""
        # Mock Path pour events_dir
        mock_events_dir = Mock()
        mock_events_dir.exists.return_value = True
        mock_events_dir.glob.return_value = [Mock()]  # Fichiers récents

        # Mock Path pour dashboard_file
        mock_dashboard_file = Mock()
        mock_dashboard_file.exists.return_value = True

        # Mock Path constructor
        def mock_path_constructor(path_str):
            if "events" in path_str:
                return mock_events_dir
            elif "dashboard" in path_str:
                return mock_dashboard_file
            else:
                return Mock()

        with patch("modules.zeroia.healthcheck_enhanced.Path", side_effect=mock_path_constructor):
            with patch("builtins.open", side_effect=json.JSONDecodeError("", "", 0)):
                with patch("builtins.print") as mock_print:
                    result = check_enhanced_health()

        assert result is True
        mock_print.assert_called_with("✅ ZeroIA Enhanced - Event Store actif")

    def test_check_enhanced_health_dashboard_inactive(self):
        """Test healthcheck enhanced avec dashboard inactif."""
        # Mock Path pour events_dir
        mock_events_dir = Mock()
        mock_events_dir.exists.return_value = True
        mock_events_dir.glob.return_value = [Mock()]  # Fichiers récents

        # Mock Path pour dashboard_file
        mock_dashboard_file = Mock()
        mock_dashboard_file.exists.return_value = True

        # Mock Path constructor
        def mock_path_constructor(path_str):
            if "events" in path_str:
                return mock_events_dir
            elif "dashboard" in path_str:
                return mock_dashboard_file
            else:
                return Mock()

        dashboard_data = {"status": "inactive", "last_decision": "2025-01-27"}

        with patch("modules.zeroia.healthcheck_enhanced.Path", side_effect=mock_path_constructor):
            with patch("builtins.open", mock_open(read_data=json.dumps(dashboard_data))):
                with patch("builtins.print") as mock_print:
                    result = check_enhanced_health()

        assert result is True
        mock_print.assert_called_with("✅ ZeroIA Enhanced - Event Store actif")

    def test_check_enhanced_health_exception_handling(self):
        """Test healthcheck enhanced avec gestion d'exception."""
        # Mock Path constructor pour lever une exception
        with patch(
            "modules.zeroia.healthcheck_enhanced.Path", side_effect=Exception("Test exception")
        ):
            with patch("builtins.print") as mock_print:
                result = check_enhanced_health()

        assert result is False
        mock_print.assert_any_call("❌ Erreur healthcheck: Test exception")

    def test_debug_path_calls(self):
        """Test de debug pour comprendre les appels Path."""
        path_calls = []

        def mock_path_constructor(*args, **kwargs):
            path_calls.append((args, kwargs))
            print(f"DEBUG: Path called with args={args}, kwargs={kwargs}")
            mock_path = Mock()
            mock_path.exists.return_value = True
            mock_path.glob.return_value = [Mock()]
            return mock_path

        with patch("modules.zeroia.healthcheck_enhanced.Path", side_effect=mock_path_constructor):
            with patch("builtins.print"):
                try:
                    result = check_enhanced_health()
                    print(f"DEBUG: Result: {result}")
                except Exception as e:
                    print(f"DEBUG: Exception: {e}")

        print(f"DEBUG: Path calls: {path_calls}")
        # Ne pas faire d'assertion pour ce test de debug


class TestHealthcheckEnhancedIntegration:
    """Tests d'intégration pour healthcheck_enhanced"""

    def test_full_healthcheck_workflow(self):
        """Test workflow complet de healthcheck."""
        # Mock Path pour events_dir
        mock_events_dir = Mock()
        mock_events_dir.exists.return_value = True
        mock_events_dir.glob.return_value = [Mock()]  # Fichiers récents

        # Mock Path pour dashboard_file
        mock_dashboard_file = Mock()
        mock_dashboard_file.exists.return_value = True

        # Mock Path constructor
        def mock_path_constructor(path_str):
            if "events" in path_str:
                return mock_events_dir
            elif "dashboard" in path_str:
                return mock_dashboard_file
            else:
                return Mock()

        dashboard_data = {"status": "active", "last_decision": "2025-01-27"}

        with patch("modules.zeroia.healthcheck_enhanced.Path", side_effect=mock_path_constructor):
            with patch("builtins.open", mock_open(read_data=json.dumps(dashboard_data))):
                with patch("builtins.print") as mock_print:
                    result = check_enhanced_health()

        assert result is True
        mock_print.assert_called_with("✅ ZeroIA Enhanced OK")


class TestHealthcheckEnhancedRobustness:
    """Tests de robustesse pour healthcheck_enhanced"""

    def test_healthcheck_with_malformed_json(self):
        """Test healthcheck avec JSON malformé dans dashboard."""
        # Mock Path pour events_dir
        mock_events_dir = Mock()
        mock_events_dir.exists.return_value = True
        mock_events_dir.glob.return_value = [Mock()]  # Fichiers récents

        # Mock Path pour dashboard_file
        mock_dashboard_file = Mock()
        mock_dashboard_file.exists.return_value = True

        # Mock Path constructor
        def mock_path_constructor(path_str):
            if "events" in path_str:
                return mock_events_dir
            elif "dashboard" in path_str:
                return mock_dashboard_file
            else:
                return Mock()

        with patch("modules.zeroia.healthcheck_enhanced.Path", side_effect=mock_path_constructor):
            with patch("builtins.open", mock_open(read_data="invalid json {")):
                with patch("builtins.print") as mock_print:
                    result = check_enhanced_health()

        assert result is True
        mock_print.assert_called_with("✅ ZeroIA Enhanced - Event Store actif")

    def test_healthcheck_with_empty_events_directory(self):
        """Test healthcheck avec répertoire events vide."""
        # Mock Path pour events_dir
        mock_events_dir = Mock()
        mock_events_dir.exists.return_value = True
        mock_events_dir.glob.return_value = []  # Pas de fichiers récents

        # Mock Path constructor
        def mock_path_constructor(path_str):
            if "events" in path_str:
                return mock_events_dir
            else:
                return Mock()

        with patch("modules.zeroia.healthcheck_enhanced.Path", side_effect=mock_path_constructor):
            with patch("builtins.print") as mock_print:
                result = check_enhanced_health()

        assert result is False
        mock_print.assert_any_call("❌ Aucun événement récent")
