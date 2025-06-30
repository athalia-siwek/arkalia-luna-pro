"""🧪 Tests étendus pour le module adaptive_thresholds de ZeroIA"""

import tempfile
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest
import toml

from modules.zeroia.adaptive_thresholds import (
    adjust_threshold,
    adjust_thresholds_based_on_history,
    analyze_decision_patterns,
    count_recent_action,
    load_adaptive_thresholds_config,
    load_decision_log,
    save_adaptive_thresholds_config,
    should_lower_cpu_threshold,
)


class TestAdaptiveThresholdsEnhanced:
    """Tests étendus pour les seuils adaptatifs"""

    def test_load_decision_log_success(self):
        """Test du chargement réussi du log de décisions"""
        mock_data = {"decisions": [{"output": "monitor"}, {"output": "reduce_load"}]}
        with patch("builtins.open", mock_open(read_data=toml.dumps(mock_data))):
            result = load_decision_log("test_path.toml")
            assert result == mock_data

    def test_load_decision_log_file_not_found(self):
        """Test du chargement avec fichier introuvable"""
        with patch("builtins.open", side_effect=FileNotFoundError):
            result = load_decision_log("nonexistent.toml")
            assert result is None

    def test_load_decision_log_invalid_toml(self):
        """Test du chargement avec TOML invalide"""
        with patch("builtins.open", mock_open(read_data="invalid toml content")):
            result = load_decision_log("invalid.toml")
            assert result is None

    def test_analyze_decision_patterns(self):
        """Test de l'analyse des patterns de décisions"""
        log_data = {"decisions": [{"output": "monitor"}]}
        result = analyze_decision_patterns(log_data)
        assert result == {"patterns": log_data}

    def test_adjust_thresholds_based_on_history(self):
        """Test de l'ajustement des seuils basé sur l'historique"""
        history = {"decisions": [{"output": "monitor"}]}
        # Cette fonction ne fait rien pour l'instant, on vérifie qu'elle ne lève pas d'erreur
        adjust_thresholds_based_on_history(history)

    def test_count_recent_action_with_valid_data(self):
        """Test du comptage d'actions récentes avec données valides"""
        mock_data = {
            "decisions": [
                {"output": "monitor"},
                {"output": "reduce_load"},
                {"output": "monitor"},
            ]
        }
        with patch("modules.zeroia.adaptive_thresholds.load_decision_log", return_value=mock_data):
            count = count_recent_action("monitor", window=3)
            assert count == 2

    def test_count_recent_action_no_decisions(self):
        """Test du comptage avec pas de décisions"""
        mock_data = {"other_data": "value"}
        with patch("modules.zeroia.adaptive_thresholds.load_decision_log", return_value=mock_data):
            count = count_recent_action("monitor")
            assert count == 0

    def test_count_recent_action_none_data(self):
        """Test du comptage avec données None"""
        with patch("modules.zeroia.adaptive_thresholds.load_decision_log", return_value=None):
            count = count_recent_action("monitor")
            assert count == 0

    def test_should_lower_cpu_threshold_true(self):
        """Test de should_lower_cpu_threshold retournant True"""
        mock_data = {
            "decisions": [{"output": "monitor"}] * 8  # 8 décisions monitor
        }
        with patch("modules.zeroia.adaptive_thresholds.load_decision_log", return_value=mock_data):
            result = should_lower_cpu_threshold()
            assert result is True

    def test_should_lower_cpu_threshold_false(self):
        """Test de should_lower_cpu_threshold retournant False"""
        mock_data = {
            "decisions": [{"output": "reduce_load"}] * 5  # 5 décisions reduce_load
        }
        with patch("modules.zeroia.adaptive_thresholds.load_decision_log", return_value=mock_data):
            result = should_lower_cpu_threshold()
            assert result is False

    def test_load_adaptive_thresholds_config_success(self):
        """Test du chargement réussi de la configuration"""
        mock_config = {"cpu_threshold": 80.0, "ram_threshold": 70.0}
        with patch("builtins.open", mock_open(read_data=toml.dumps(mock_config))):
            result = load_adaptive_thresholds_config()
            assert result == mock_config

    def test_load_adaptive_thresholds_config_file_not_found(self):
        """Test du chargement avec fichier introuvable"""
        with patch("builtins.open", side_effect=FileNotFoundError):
            result = load_adaptive_thresholds_config()
            assert result is None

    def test_load_adaptive_thresholds_config_invalid_data(self):
        """Test du chargement avec données invalides"""
        with patch("builtins.open", mock_open(read_data="invalid toml")):
            result = load_adaptive_thresholds_config()
            assert result is None

    def test_load_adaptive_thresholds_config_not_dict(self):
        """Test du chargement avec données non-dictionnaire"""
        with patch("builtins.open", mock_open(read_data="[1, 2, 3]")):
            result = load_adaptive_thresholds_config()
            assert result is None

    def test_adjust_threshold_increase(self):
        """Test de l'ajustement de seuil avec augmentation"""
        result = adjust_threshold(100.0, "increase")
        assert abs(result - 110.0) < 0.01  # Utiliser une comparaison approximative

    def test_adjust_threshold_decrease(self):
        """Test de l'ajustement de seuil avec diminution"""
        result = adjust_threshold(100.0, "decrease")
        assert result == 90.0

    def test_adjust_threshold_stable(self):
        """Test de l'ajustement de seuil stable"""
        result = adjust_threshold(100.0, "stable")
        assert result == 100.0

    def test_adjust_threshold_other_feedback(self):
        """Test de l'ajustement de seuil avec feedback inconnu"""
        result = adjust_threshold(100.0, "unknown")
        assert result == 100.0

    def test_save_adaptive_thresholds_config_success(self):
        """Test de la sauvegarde réussie de la configuration"""
        config = {"cpu_threshold": 80.0}
        with patch("builtins.open", mock_open()) as mock_file:
            save_adaptive_thresholds_config(config)
            mock_file.assert_called_once()

    def test_save_adaptive_thresholds_config_error(self):
        """Test de la sauvegarde avec erreur"""
        config = {"cpu_threshold": 80.0}
        with patch("builtins.open", side_effect=PermissionError):
            # Ne doit pas lever d'exception
            save_adaptive_thresholds_config(config)

    def test_count_recent_action_empty_decisions(self):
        """Test du comptage avec décisions vides"""
        mock_data = {"decisions": []}
        with patch("modules.zeroia.adaptive_thresholds.load_decision_log", return_value=mock_data):
            count = count_recent_action("monitor")
            assert count == 0

    def test_count_recent_action_missing_output_key(self):
        """Test du comptage avec clé output manquante"""
        mock_data = {
            "decisions": [
                {"other_key": "monitor"},
                {"output": "monitor"},
            ]
        }
        with patch("modules.zeroia.adaptive_thresholds.load_decision_log", return_value=mock_data):
            count = count_recent_action("monitor", window=2)
            assert count == 1 