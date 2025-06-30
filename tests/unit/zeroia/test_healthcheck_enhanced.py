"""🧪 Tests étendus pour le module healthcheck_enhanced de ZeroIA"""

import json
import tempfile
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest
import toml

from modules.zeroia.healthcheck_enhanced import (
    check_enhanced_health,
    check_zeroia_health,
    load_healthcheck_config,
)


class TestHealthcheckEnhanced:
    """Tests étendus pour le healthcheck amélioré"""

    def setup_method(self):
        """Configuration avant chaque test"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = Path(self.temp_dir) / "healthcheck.toml"
        self.state_file = Path(self.temp_dir) / "zeroia_state.toml"
        self.dashboard_file = Path(self.temp_dir) / "zeroia_dashboard.json"
        self.events_dir = Path(self.temp_dir) / "events"

    def test_load_healthcheck_config_success(self):
        """Test du chargement réussi de la configuration"""
        mock_config = {"enabled": True, "interval": 30, "timeout": 10}
        with patch("builtins.open", mock_open(read_data=toml.dumps(mock_config))):
            result = load_healthcheck_config()
            assert result == mock_config

    def test_load_healthcheck_config_file_not_found(self):
        """Test du chargement avec fichier introuvable"""
        with patch("builtins.open", side_effect=FileNotFoundError):
            result = load_healthcheck_config()
            assert result == {"enabled": True, "interval": 30}

    def test_load_healthcheck_config_invalid_data(self):
        """Test du chargement avec données invalides"""
        with patch("builtins.open", side_effect=Exception("Invalid data")):
            result = load_healthcheck_config()
            assert result == {"enabled": False, "interval": 60}

    def test_check_zeroia_health_active(self):
        """Test de la vérification de santé avec état actif"""
        mock_state = {"status": "active", "last_update": "2025-01-01"}
        with patch("pathlib.Path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=toml.dumps(mock_state))):
                result = check_zeroia_health()
                assert result is True

    def test_check_zeroia_health_inactive(self):
        """Test de la vérification de santé avec état inactif"""
        mock_state = {"status": "inactive", "last_update": "2025-01-01"}
        with patch("pathlib.Path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=toml.dumps(mock_state))):
                result = check_zeroia_health()
                assert result is False

    def test_check_zeroia_health_file_not_found(self):
        """Test de la vérification de santé avec fichier introuvable"""
        with patch("pathlib.Path.exists", return_value=False):
            result = check_zeroia_health()
            assert result is False

    def test_check_zeroia_health_invalid_data(self):
        """Test de la vérification de santé avec données invalides"""
        with patch("pathlib.Path.exists", return_value=True):
            with patch("builtins.open", side_effect=Exception("Invalid data")):
                result = check_zeroia_health()
                assert result is False

    def test_check_zeroia_health_missing_status(self):
        """Test de la vérification de santé avec statut manquant"""
        mock_state = {"last_update": "2025-01-01"}  # Pas de status
        with patch("pathlib.Path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=toml.dumps(mock_state))):
                result = check_zeroia_health()
                assert result is False

    def test_check_enhanced_health_event_store_not_found(self):
        """Test de la vérification de santé améliorée sans Event Store"""
        with patch("pathlib.Path.exists", return_value=False):
            with patch("builtins.print") as mock_print:
                result = check_enhanced_health()
                assert result is False
                mock_print.assert_called_with("❌ Event Store non trouvé")

    def test_check_enhanced_health_no_recent_files(self):
        """Test de la vérification de santé améliorée sans fichiers récents"""
        # Mock events_dir existe mais pas de fichiers récents
        with patch("pathlib.Path.exists", side_effect=lambda: True):
            with patch("pathlib.Path.glob", return_value=[]):
                with patch("builtins.print") as mock_print:
                    result = check_enhanced_health()
                    assert result is False
                    mock_print.assert_called_with("❌ Aucun événement récent")

    def test_check_enhanced_health_with_dashboard_active(self):
        """Test de la vérification de santé améliorée avec dashboard actif"""
        mock_dashboard = {"status": "active", "last_decision": "monitor"}

        # Mock events_dir existe avec fichiers récents
        mock_files = [Path("event1.cache"), Path("event2.cache")]

        with patch("pathlib.Path.exists", side_effect=lambda: True):
            with patch("pathlib.Path.glob", return_value=mock_files):
                with patch("builtins.open", mock_open(read_data=json.dumps(mock_dashboard))):
                    with patch("builtins.print") as mock_print:
                        result = check_enhanced_health()
                        assert result is True
                        mock_print.assert_called_with("✅ ZeroIA Enhanced OK")

    def test_check_enhanced_health_with_dashboard_inactive(self):
        """Test de la vérification de santé améliorée avec dashboard inactif"""
        mock_dashboard = {"status": "inactive", "last_decision": "halt"}

        # Mock events_dir existe avec fichiers récents
        mock_files = [Path("event1.cache"), Path("event2.cache")]

        with patch("pathlib.Path.exists", side_effect=lambda: True):
            with patch("pathlib.Path.glob", return_value=mock_files):
                with patch("builtins.open", mock_open(read_data=json.dumps(mock_dashboard))):
                    with patch("builtins.print") as mock_print:
                        result = check_enhanced_health()
                        assert result is True  # Retourne True car Event Store est actif
                        # Vérifie que le message Event Store actif est affiché
                        mock_print.assert_called_with("✅ ZeroIA Enhanced - Event Store actif")

    def test_check_enhanced_health_dashboard_not_found(self):
        """Test de la vérification de santé améliorée sans dashboard"""
        # Mock events_dir existe avec fichiers récents, mais pas de dashboard
        mock_files = [Path("event1.cache"), Path("event2.cache")]

        def mock_exists(path):
            path_str = str(path)
            if "dashboard" in path_str:
                return False
            if "events" in path_str:
                return True
            return True

        with patch("pathlib.Path.exists", side_effect=mock_exists):
            with patch("pathlib.Path.glob", return_value=mock_files):
                with patch("builtins.print") as mock_print:
                    result = check_enhanced_health()
                    assert result is True
                    mock_print.assert_called_with("✅ ZeroIA Enhanced - Event Store actif")

    def test_check_enhanced_health_dashboard_invalid_json(self):
        """Test de la vérification de santé améliorée avec JSON invalide"""
        # Mock events_dir existe avec fichiers récents
        mock_files = [Path("event1.cache"), Path("event2.cache")]

        def mock_exists(path):
            return True

        with patch("pathlib.Path.exists", side_effect=mock_exists):
            with patch("pathlib.Path.glob", return_value=mock_files):
                with patch("builtins.open", side_effect=Exception("Invalid JSON")):
                    with patch("builtins.print") as mock_print:
                        result = check_enhanced_health()
                        assert result is True  # Retourne True car Event Store est actif
                        mock_print.assert_called_with("✅ ZeroIA Enhanced - Event Store actif")

    def test_check_enhanced_health_exception_handling(self):
        """Test de la gestion d'exception dans check_enhanced_health"""
        with patch("pathlib.Path.exists", side_effect=Exception("Test exception")):
            with patch("builtins.print") as mock_print:
                result = check_enhanced_health()
                assert result is False
                mock_print.assert_called_with("❌ Erreur healthcheck: Test exception")

    def test_check_enhanced_health_with_recent_files(self):
        """Test de la vérification de santé améliorée avec fichiers récents"""
        # Mock events_dir existe avec fichiers récents
        mock_files = [Path("event1.cache"), Path("event2.cache")]

        with patch("pathlib.Path.exists", side_effect=lambda: True):
            with patch("pathlib.Path.glob", return_value=mock_files):
                with patch("builtins.print") as mock_print:
                    result = check_enhanced_health()
                    assert result is True
                    # Vérifie que le message Event Store actif est affiché
                    mock_print.assert_called_with("✅ ZeroIA Enhanced - Event Store actif")

    def test_check_enhanced_health_dashboard_missing_status(self):
        """Test de la vérification de santé améliorée avec dashboard sans statut"""
        mock_dashboard = {"last_decision": "monitor"}  # Pas de status

        # Mock events_dir existe avec fichiers récents
        mock_files = [Path("event1.cache"), Path("event2.cache")]

        with patch("pathlib.Path.exists", side_effect=lambda: True):
            with patch("pathlib.Path.glob", return_value=mock_files):
                with patch("builtins.open", mock_open(read_data=json.dumps(mock_dashboard))):
                    with patch("builtins.print") as mock_print:
                        result = check_enhanced_health()
                        assert result is True  # Retourne True car Event Store est actif
                        mock_print.assert_called_with("✅ ZeroIA Enhanced - Event Store actif")

    def test_check_enhanced_health_file_permission_error(self):
        """Test de la vérification de santé améliorée avec erreur de permission"""
        with patch("pathlib.Path.exists", side_effect=PermissionError("Permission denied")):
            with patch("builtins.print") as mock_print:
                result = check_enhanced_health()
                assert result is False
                mock_print.assert_called_with("❌ Erreur healthcheck: Permission denied")
