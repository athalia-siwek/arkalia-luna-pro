# 🧪 Tests complets pour modules/zeroia/healthcheck_zeroia.py
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import toml

from modules.zeroia.healthcheck_zeroia import check_zeroia_health, get_state_path
from tests.unit.test_helpers import ensure_test_toml

ensure_test_toml()


def test_get_state_path_default():
    """🧠 Test get_state_path sans variable d'environnement"""
    with patch.dict(os.environ, {}, clear=True):
        # Supprime ZEROIA_STATE_PATH si elle existe
        if "ZEROIA_STATE_PATH" in os.environ:
            del os.environ["ZEROIA_STATE_PATH"]

        path = get_state_path()
        assert str(path) == "modules/zeroia/state/zeroia_state.toml"
        assert isinstance(path, Path)


def test_get_state_path_with_env_var():
    """🧠 Test get_state_path avec variable d'environnement personnalisée"""
    custom_path = "/custom/path/zeroia_state.toml"
    with patch.dict(os.environ, {"ZEROIA_STATE_PATH": custom_path}):
        path = get_state_path()
        assert str(path) == custom_path
        assert isinstance(path, Path)


def test_check_zeroia_health_file_missing_verbose():
    """🧠 Test check_zeroia_health avec fichier manquant (mode verbose)"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        missing_file = Path(tmp_dir) / "missing.toml"

        with patch(
            "modules.zeroia.healthcheck_zeroia.get_state_path",
            return_value=missing_file,
        ):
            result = check_zeroia_health(verbose=True)
            assert result is False


def test_check_zeroia_health_file_missing_silent():
    """🧠 Test check_zeroia_health avec fichier manquant (mode silencieux)"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        missing_file = Path(tmp_dir) / "missing.toml"

        with patch(
            "modules.zeroia.healthcheck_zeroia.get_state_path",
            return_value=missing_file,
        ):
            result = check_zeroia_health(verbose=False)
            assert result is False


def test_check_zeroia_health_active_with_decision():
    """🧠 Test check_zeroia_health avec état actif et décision"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        state_file = Path(tmp_dir) / "zeroia_state.toml"

        test_data = {"active": True, "decision": {"last_decision": "reduce_load"}}

        toml.dump(test_data, state_file.open("w"))

        with patch(
            "modules.zeroia.healthcheck_zeroia.get_state_path", return_value=state_file
        ):
            result = check_zeroia_health(verbose=True)
            assert result is True


def test_check_zeroia_health_inactive():
    """🧠 Test check_zeroia_health avec état inactif"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        state_file = Path(tmp_dir) / "zeroia_state.toml"

        test_data = {"active": False, "decision": {"last_decision": "reduce_load"}}

        toml.dump(test_data, state_file.open("w"))

        with patch(
            "modules.zeroia.healthcheck_zeroia.get_state_path", return_value=state_file
        ):
            result = check_zeroia_health(verbose=True)
            assert result is False


def test_check_zeroia_health_active_no_decision():
    """🧠 Test check_zeroia_health avec état actif mais sans décision"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        state_file = Path(tmp_dir) / "zeroia_state.toml"

        test_data = {"active": True, "decision": {}}  # Pas de last_decision

        toml.dump(test_data, state_file.open("w"))

        with patch(
            "modules.zeroia.healthcheck_zeroia.get_state_path", return_value=state_file
        ):
            result = check_zeroia_health(verbose=True)
            assert result is False


def test_check_zeroia_health_missing_decision_section():
    """🧠 Test check_zeroia_health sans section decision"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        state_file = Path(tmp_dir) / "zeroia_state.toml"

        test_data = {
            "active": True
            # Pas de section decision
        }

        toml.dump(test_data, state_file.open("w"))

        with patch(
            "modules.zeroia.healthcheck_zeroia.get_state_path", return_value=state_file
        ):
            result = check_zeroia_health(verbose=True)
            assert result is False


def test_check_zeroia_health_force_ok_enabled():
    """🧠 Test check_zeroia_health avec FORCE_ZEROIA_OK=1"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        state_file = Path(tmp_dir) / "zeroia_state.toml"

        # État inactif normalement
        test_data = {"active": False, "decision": {}}

        toml.dump(test_data, state_file.open("w"))

        with patch(
            "modules.zeroia.healthcheck_zeroia.get_state_path", return_value=state_file
        ):
            with patch.dict(os.environ, {"FORCE_ZEROIA_OK": "1"}):
                result = check_zeroia_health(verbose=True)
                assert result is True  # Forcé à True par la variable d'environnement


def test_check_zeroia_health_force_ok_disabled():
    """🧠 Test check_zeroia_health avec FORCE_ZEROIA_OK=0"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        state_file = Path(tmp_dir) / "zeroia_state.toml"

        test_data = {"active": False, "decision": {}}

        toml.dump(test_data, state_file.open("w"))

        with patch(
            "modules.zeroia.healthcheck_zeroia.get_state_path", return_value=state_file
        ):
            with patch.dict(os.environ, {"FORCE_ZEROIA_OK": "0"}):
                result = check_zeroia_health(verbose=True)
                assert result is False  # Pas forcé, suit la logique normale


def test_check_zeroia_health_toml_parse_error():
    """🧠 Test check_zeroia_health avec erreur de parsing TOML"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        state_file = Path(tmp_dir) / "zeroia_state.toml"

        # Écrit un TOML invalide
        state_file.write_text("[invalid toml syntax")

        with patch(
            "modules.zeroia.healthcheck_zeroia.get_state_path", return_value=state_file
        ):
            result = check_zeroia_health(verbose=True)
            assert result is False


def test_check_zeroia_health_permission_error():
    """🧠 Test check_zeroia_health avec erreur de permissions"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        state_file = Path(tmp_dir) / "zeroia_state.toml"

        test_data = {"active": True}
        toml.dump(test_data, state_file.open("w"))

        # Supprime les permissions de lecture
        state_file.chmod(0o000)

        try:
            with patch(
                "modules.zeroia.healthcheck_zeroia.get_state_path",
                return_value=state_file,
            ):
                result = check_zeroia_health(verbose=True)
                assert result is False
        finally:
            # Remet les permissions pour le nettoyage
            state_file.chmod(0o644)


def test_check_zeroia_health_empty_file():
    """🧠 Test check_zeroia_health avec fichier vide"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        state_file = Path(tmp_dir) / "zeroia_state.toml"

        # Crée un fichier vide
        state_file.touch()

        with patch(
            "modules.zeroia.healthcheck_zeroia.get_state_path", return_value=state_file
        ):
            result = check_zeroia_health(verbose=True)
            assert result is False


def test_check_zeroia_health_null_values():
    """🧠 Test check_zeroia_health avec des valeurs null"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        state_file = Path(tmp_dir) / "zeroia_state.toml"

        test_data = {"active": None, "decision": {"last_decision": None}}

        toml.dump(test_data, state_file.open("w"))

        with patch(
            "modules.zeroia.healthcheck_zeroia.get_state_path", return_value=state_file
        ):
            result = check_zeroia_health(verbose=True)
            assert result is False


def test_check_zeroia_health_empty_string_decision():
    """🧠 Test check_zeroia_health avec décision chaîne vide"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        state_file = Path(tmp_dir) / "zeroia_state.toml"

        test_data = {"active": True, "decision": {"last_decision": ""}}  # Chaîne vide

        toml.dump(test_data, state_file.open("w"))

        with patch(
            "modules.zeroia.healthcheck_zeroia.get_state_path", return_value=state_file
        ):
            result = check_zeroia_health(verbose=True)
            assert result is False  # Chaîne vide évaluée comme False


def test_check_zeroia_health_verbose_false_scenarios():
    """🧠 Test plusieurs scénarios avec verbose=False"""
    scenarios = [
        {
            "active": True,
            "decision": {"last_decision": "reduce_load"},
        },  # Should be True
        {
            "active": False,
            "decision": {"last_decision": "reduce_load"},
        },  # Should be False
        {"active": True, "decision": {}},  # Should be False
    ]

    expected_results = [True, False, False]

    for i, (test_data, expected) in enumerate(zip(scenarios, expected_results)):
        with tempfile.TemporaryDirectory() as tmp_dir:
            state_file = Path(tmp_dir) / f"zeroia_state_{i}.toml"
            toml.dump(test_data, state_file.open("w"))

            with patch(
                "modules.zeroia.healthcheck_zeroia.get_state_path",
                return_value=state_file,
            ):
                result = check_zeroia_health(verbose=False)
                assert (
                    result is expected
                ), f"Scenario {i} failed: expected {expected}, got {result}"
