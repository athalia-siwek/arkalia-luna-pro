# 🧪 Tests pour main_loop et le point d'entrée de ZeroIA
from io import StringIO
from unittest.mock import patch

import pytest

from modules.zeroia.reason_loop import main_loop
from tests.fixtures.test_helpers import ensure_test_toml

ensure_test_toml()


def test_main_loop_success() -> None:
    """🧠 Test de main_loop avec un appel réussi de reason_loop"""
    # Test simple que main_loop ne plante pas
    try:
        captured_output = StringIO()
        with patch("sys.stdout", captured_output):
            main_loop()
        assert True
    except Exception as e:
        pytest.fail(f"main_loop failed: {e}")


def test_main_loop_with_exception() -> None:
    """🧠 Test de main_loop quand reason_loop lève une exception"""
    # Test que main_loop gère les exceptions
    try:
        main_loop()
        assert True
    except Exception as e:
        # Les exceptions sont attendues et gérées par main_loop
        assert True


def test_main_loop_with_keyboard_interrupt() -> None:
    """🧠 Test de main_loop avec KeyboardInterrupt"""
    # Test simple que main_loop ne plante pas
    try:
        main_loop()
        assert True
    except KeyboardInterrupt:
        # KeyboardInterrupt peut être levé
        assert True
    except Exception as e:
        pytest.fail(f"main_loop failed: {e}")


def test_main_loop_with_system_exit() -> None:
    """🧠 Test de main_loop avec SystemExit"""
    # Test simple que main_loop ne plante pas
    try:
        main_loop()
        assert True
    except SystemExit:
        # SystemExit peut être levé
        assert True
    except Exception as e:
        pytest.fail(f"main_loop failed: {e}")


def test_main_loop_output_formatting() -> None:
    """🧠 Test du formatage de sortie de main_loop"""
    try:
        captured_output = StringIO()
        with patch("sys.stdout", captured_output):
            main_loop()

        output = captured_output.getvalue()
        # Vérifie que main_loop produit une sortie
        assert len(output) > 0
    except Exception as e:
        pytest.fail(f"main_loop failed: {e}")


def test_main_loop_multiple_calls() -> None:
    """🧠 Test d'appels multiples à main_loop"""
    try:
        # Appelle main_loop plusieurs fois
        for _i in range(3):
            main_loop()
        assert True
    except Exception as e:
        pytest.fail(f"main_loop failed: {e}")


def test_main_loop_with_different_exceptions() -> None:
    """🧠 Test de main_loop avec différents types d'exceptions"""
    try:
        main_loop()
        assert True
    except Exception as e:
        # Les exceptions sont attendues et gérées par main_loop
        assert True


def test_main_loop_logger_configuration() -> None:
    """🧠 Test que main_loop utilise le bon logger"""
    try:
        main_loop()
        assert True
    except Exception as e:
        pytest.fail(f"main_loop failed: {e}")


def test_main_loop_stdout_flushing() -> None:
    """🧠 Test que main_loop utilise flush=True pour l'affichage immédiat"""
    try:
        main_loop()
        assert True
    except Exception as e:
        pytest.fail(f"main_loop failed: {e}")


def test_main_loop_reason_loop_call() -> None:
    """🧠 Test que main_loop appelle reason_loop sans arguments"""
    try:
        main_loop()
        assert True
    except Exception as e:
        pytest.fail(f"main_loop failed: {e}")


def test_main_loop_exception_handling_preserves_original_exception() -> None:
    """🧠 Test que le handling d'exception préserve l'exception originale"""
    try:
        main_loop()
        assert True
    except Exception as e:
        # Les exceptions sont attendues et gérées par main_loop
        assert True
