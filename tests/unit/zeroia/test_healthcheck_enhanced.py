#!/usr/bin/env python3
# 🧪 tests/unit/zeroia/test_healthcheck_enhanced.py
"""Tests unitaires pour healthcheck_enhanced.py"""

import json
import os
import runpy
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
    """Tests pour load_healthcheck_config"""

    def test_load_healthcheck_config_success(self, tmp_path):
        """Test chargement config réussi."""
        config_data = {"enabled": True, "interval": 30}
        with patch("builtins.open", mock_open(read_data=toml.dumps(config_data))):
            result = load_healthcheck_config()

        assert result == config_data

    def test_load_healthcheck_config_file_not_found(self):
        """Test chargement config avec fichier manquant."""
        with patch("builtins.open", side_effect=FileNotFoundError):
            result = load_healthcheck_config()

        assert result == {"enabled": True, "interval": 30}

    def test_load_healthcheck_config_invalid_toml(self):
        """Test chargement config avec TOML invalide."""
        with patch("builtins.open", mock_open(read_data="invalid toml")):
            result = load_healthcheck_config()

        assert result == {"enabled": False, "interval": 60}

    def test_load_healthcheck_config_permission_error(self):
        """Test chargement config avec erreur de permission."""
        with patch("builtins.open", side_effect=PermissionError):
            result = load_healthcheck_config()

        assert result == {"enabled": False, "interval": 60}


class TestCheckZeroiaHealth:
    """Tests pour check_zeroia_health"""

    def test_check_zeroia_health_active(self, tmp_path):
        """Test healthcheck ZeroIA actif."""
        state_data = {"status": "active"}
        state_file = tmp_path / "state" / "zeroia_state.toml"
        state_file.parent.mkdir(parents=True, exist_ok=True)
        state_file.write_text(toml.dumps(state_data))
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = check_zeroia_health()
            assert result is True
        finally:
            os.chdir(old_cwd)

    def test_check_zeroia_health_inactive(self, tmp_path):
        """Test healthcheck ZeroIA inactif."""
        state_data = {"status": "inactive"}
        state_file = tmp_path / "zeroia_state.toml"
        state_file.write_text(toml.dumps(state_data))

        with patch("pathlib.Path", return_value=state_file):
            result = check_zeroia_health()

        assert result is False

    def test_check_zeroia_health_missing_status(self, tmp_path):
        """Test healthcheck ZeroIA sans statut."""
        state_data = {"other_field": "value"}
        state_file = tmp_path / "zeroia_state.toml"
        state_file.write_text(toml.dumps(state_data))

        with patch("pathlib.Path", return_value=state_file):
            result = check_zeroia_health()

        assert result is False

    def test_check_zeroia_health_file_not_found(self):
        """Test healthcheck ZeroIA avec fichier manquant."""
        with patch("pathlib.Path.exists", return_value=False):
            result = check_zeroia_health()

        assert result is False

    def test_check_zeroia_health_invalid_toml(self, tmp_path):
        """Test healthcheck ZeroIA avec TOML invalide."""
        state_file = tmp_path / "zeroia_state.toml"
        state_file.write_text("invalid toml")

        with patch("pathlib.Path", return_value=state_file):
            result = check_zeroia_health()

        assert result is False

    def test_check_zeroia_health_permission_error(self, tmp_path):
        """Test healthcheck ZeroIA avec erreur de permission."""
        state_file = tmp_path / "zeroia_state.toml"
        state_file.touch()

        with patch("builtins.open", side_effect=PermissionError):
            with patch("pathlib.Path", return_value=state_file):
                result = check_zeroia_health()

        assert result is False


class TestCheckEnhancedHealth:
    """Tests pour check_enhanced_health"""

    def test_check_enhanced_health_success_with_dashboard(self, tmp_path):
        """Test healthcheck enhanced réussi avec dashboard."""
        cache_dir = tmp_path / "cache"
        events_dir = cache_dir / "zeroia_events" / "events"
        events_dir.mkdir(parents=True)
        (events_dir / "event1.cache").touch()
        state_dir = tmp_path / "state"
        state_dir.mkdir()
        dashboard_file = state_dir / "zeroia_dashboard.json"
        dashboard_data = {"status": "active", "last_decision": "2025-01-27"}
        dashboard_file.write_text(json.dumps(dashboard_data))
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with patch("builtins.print") as mock_print:
                result = check_enhanced_health()
            assert result is True
            mock_print.assert_called_with("✅ ZeroIA Enhanced OK")
        finally:
            os.chdir(old_cwd)

    def test_check_enhanced_health_success_without_dashboard(self, tmp_path):
        """Test healthcheck enhanced réussi sans dashboard mais avec Event Store."""
        cache_dir = tmp_path / "cache"
        events_dir = cache_dir / "zeroia_events" / "events"
        events_dir.mkdir(parents=True)
        (events_dir / "event1.cache").touch()
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with patch("builtins.print") as mock_print:
                result = check_enhanced_health()
            assert result is True
            mock_print.assert_called_with("✅ ZeroIA Enhanced - Event Store actif")
        finally:
            os.chdir(old_cwd)

    def test_check_enhanced_health_events_dir_missing(self, tmp_path):
        """Test healthcheck enhanced avec répertoire events manquant."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with patch("builtins.print") as mock_print:
                result = check_enhanced_health()
            assert result is False
            mock_print.assert_any_call("❌ Event Store non trouvé")
        finally:
            os.chdir(old_cwd)

    def test_check_enhanced_health_no_recent_files(self, tmp_path):
        """Test healthcheck enhanced sans fichiers récents."""
        cache_dir = tmp_path / "cache"
        events_dir = cache_dir / "zeroia_events" / "events"
        events_dir.mkdir(parents=True)
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with patch("builtins.print") as mock_print:
                result = check_enhanced_health()
            assert result is False
            mock_print.assert_any_call("❌ Aucun événement récent")
        finally:
            os.chdir(old_cwd)

    def test_check_enhanced_health_dashboard_error(self, tmp_path):
        """Test healthcheck enhanced avec erreur de lecture dashboard."""
        cache_dir = tmp_path / "cache"
        events_dir = cache_dir / "zeroia_events" / "events"
        events_dir.mkdir(parents=True)
        (events_dir / "event1.cache").touch()
        state_dir = tmp_path / "state"
        state_dir.mkdir()
        dashboard_file = state_dir / "zeroia_dashboard.json"
        dashboard_file.write_text("invalid json {")
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with patch("builtins.print") as mock_print:
                result = check_enhanced_health()
            assert result is True
            mock_print.assert_called_with("✅ ZeroIA Enhanced - Event Store actif")
        finally:
            os.chdir(old_cwd)

    def test_check_enhanced_health_dashboard_inactive(self, tmp_path):
        """Test healthcheck enhanced avec dashboard inactif."""
        cache_dir = tmp_path / "cache"
        events_dir = cache_dir / "zeroia_events" / "events"
        events_dir.mkdir(parents=True)
        (events_dir / "event1.cache").touch()
        state_dir = tmp_path / "state"
        state_dir.mkdir()
        dashboard_file = state_dir / "zeroia_dashboard.json"
        dashboard_data = {"status": "inactive", "last_decision": "2025-01-27"}
        dashboard_file.write_text(json.dumps(dashboard_data))
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with patch("builtins.print") as mock_print:
                result = check_enhanced_health()
            assert result is True
            mock_print.assert_called_with("✅ ZeroIA Enhanced - Event Store actif")
        finally:
            os.chdir(old_cwd)

    def test_check_enhanced_health_exception_handling(self, tmp_path):
        """Test healthcheck enhanced avec gestion d'exception."""
        cache_dir = tmp_path / "cache"
        events_dir = cache_dir / "zeroia_events" / "events"
        events_dir.mkdir(parents=True)
        events_dir.chmod(0o000)
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with patch("builtins.print") as mock_print:
                result = check_enhanced_health()
            assert result is False
            # Le test passe si l'un des messages d'erreur attendus est présent
            error_msgs = ["Erreur healthcheck", "Aucun événement récent", "Event Store non trouvé"]
            found = any(
                any(msg in str(args) for msg in error_msgs) for args, _ in mock_print.call_args_list
            )
            assert (
                found
            ), f"Aucun message d'erreur attendu trouvé dans les prints: {[args for args, _ in mock_print.call_args_list]}"
        finally:
            events_dir.chmod(0o755)
            os.chdir(old_cwd)


class TestHealthcheckEnhancedIntegration:
    """Tests d'intégration pour healthcheck_enhanced"""

    def test_full_healthcheck_workflow(self, tmp_path):
        """Test workflow complet de healthcheck."""
        cache_dir = tmp_path / "cache"
        events_dir = cache_dir / "zeroia_events" / "events"
        events_dir.mkdir(parents=True)
        (events_dir / "event1.cache").touch()
        state_dir = tmp_path / "state"
        state_dir.mkdir()
        dashboard_file = state_dir / "zeroia_dashboard.json"
        dashboard_data = {"status": "active", "last_decision": "2025-01-27"}
        dashboard_file.write_text(json.dumps(dashboard_data))
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with patch("builtins.print") as mock_print:
                result = check_enhanced_health()
            assert result is True
            mock_print.assert_called_with("✅ ZeroIA Enhanced OK")
        finally:
            os.chdir(old_cwd)

    def test_healthcheck_with_real_file_structure(self, tmp_path):
        """Test healthcheck avec structure de fichiers réelle."""
        cache_dir = tmp_path / "cache"
        events_dir = cache_dir / "zeroia_events" / "events"
        events_dir.mkdir(parents=True)
        state_dir = tmp_path / "state"
        state_dir.mkdir()
        (events_dir / "event_20250127_120000.cache").touch()
        (events_dir / "event_20250127_120030.cache").touch()
        dashboard_file = state_dir / "zeroia_dashboard.json"
        dashboard_data = {
            "status": "active",
            "last_decision": "2025-01-27T12:00:30",
            "cpu_usage": 45.2,
            "memory_usage": 67.8,
        }
        dashboard_file.write_text(json.dumps(dashboard_data))
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with patch("builtins.print") as mock_print:
                result = check_enhanced_health()
            assert result is True
            mock_print.assert_called_with("✅ ZeroIA Enhanced OK")
        finally:
            os.chdir(old_cwd)


class TestHealthcheckEnhancedRobustness:
    """Tests de robustesse pour healthcheck_enhanced"""

    def test_healthcheck_with_malformed_json(self, tmp_path):
        """Test healthcheck avec JSON malformé dans dashboard."""
        cache_dir = tmp_path / "cache"
        events_dir = cache_dir / "zeroia_events" / "events"
        events_dir.mkdir(parents=True)
        (events_dir / "event1.cache").touch()
        state_dir = tmp_path / "state"
        state_dir.mkdir()
        dashboard_file = state_dir / "zeroia_dashboard.json"
        dashboard_file.write_text("invalid json {")
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with patch("builtins.print") as mock_print:
                result = check_enhanced_health()
            assert result is True
            mock_print.assert_called_with("✅ ZeroIA Enhanced - Event Store actif")
        finally:
            os.chdir(old_cwd)

    def test_healthcheck_with_empty_events_directory(self, tmp_path):
        """Test healthcheck avec répertoire events vide."""
        cache_dir = tmp_path / "cache"
        events_dir = cache_dir / "zeroia_events" / "events"
        events_dir.mkdir(parents=True)
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with patch("builtins.print") as mock_print:
                result = check_enhanced_health()
            assert result is False
            mock_print.assert_any_call("❌ Aucun événement récent")
        finally:
            os.chdir(old_cwd)

    def test_healthcheck_with_unicode_paths(self, tmp_path):
        """Test healthcheck avec chemins Unicode."""
        cache_dir = tmp_path / "cache"
        events_dir = cache_dir / "zeroia_events" / "events"
        events_dir.mkdir(parents=True)
        (events_dir / "événement_2025.cache").touch()
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with patch("builtins.print") as mock_print:
                result = check_enhanced_health()
            assert result is True
            mock_print.assert_called_with("✅ ZeroIA Enhanced - Event Store actif")
        finally:
            os.chdir(old_cwd)


class TestHealthcheckEnhancedMain:
    """Tests pour la fonction main"""

    def test_main_success(self, tmp_path):
        """Test main avec succès."""
        # Créer la structure attendue pour un succès
        cache_dir = tmp_path / "cache"
        events_dir = cache_dir / "zeroia_events" / "events"
        events_dir.mkdir(parents=True)
        (events_dir / "event1.cache").touch()
        state_dir = tmp_path / "state"
        state_dir.mkdir()
        dashboard_file = state_dir / "zeroia_dashboard.json"
        dashboard_data = {"status": "active", "last_decision": "2025-01-27"}
        dashboard_file.write_text(json.dumps(dashboard_data))
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with patch("sys.exit") as mock_exit:
                runpy.run_module("modules.zeroia.healthcheck_enhanced", run_name="__main__")
            mock_exit.assert_called_with(0)
        finally:
            os.chdir(old_cwd)

    def test_main_failure(self, tmp_path):
        """Test main avec échec."""
        # Créer la structure attendue pour un échec (pas de fichiers events)
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            with patch("sys.exit") as mock_exit:
                runpy.run_module("modules.zeroia.healthcheck_enhanced", run_name="__main__")
            mock_exit.assert_called_with(1)
        finally:
            os.chdir(old_cwd)
