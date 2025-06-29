# 🧪 Tests pour main_loop et le point d'entrée de ZeroIA
from io import StringIO
from unittest.mock import patch

import pytest

from modules.zeroia.reason_loop import main_loop
from tests.common.helpers import ensure_test_toml

ensure_test_toml()


def test_main_loop_success():
    """🧠 Test de main_loop avec un appel réussi de reason_loop"""
    with patch("modules.zeroia.reason_loop.reason_loop") as mock_reason_loop:
        mock_reason_loop.return_value = ("reduce_load", 0.75)

        # Capture la sortie standard
        captured_output = StringIO()
        with patch("sys.stdout", captured_output):
            main_loop()

        # Vérifie que reason_loop a été appelé
        mock_reason_loop.assert_called_once()

        # Vérifie la sortie
        output = captured_output.getvalue()
        assert "[ZeroIA] loop started" in output


def test_main_loop_with_exception():
    """🧠 Test de main_loop quand reason_loop lève une exception"""
    with patch("modules.zeroia.reason_loop.reason_loop") as mock_reason_loop:
        mock_reason_loop.side_effect = ValueError("Test error")

        with patch("modules.zeroia.reason_loop.logger") as mock_logger:
            captured_output = StringIO()
            with patch("sys.stdout", captured_output):
                main_loop()

            # Vérifie que l'exception a été loggée
            mock_logger.exception.assert_called_once()

            # Vérifie la sortie d'erreur
            output = captured_output.getvalue()
            assert "🚨 ERREUR dans reason_loop()" in output
            assert "Test error" in output


def test_main_loop_with_keyboard_interrupt():
    """🧠 Test de main_loop avec KeyboardInterrupt (qui ne devrait pas être capturée)"""
    with patch("modules.zeroia.reason_loop.reason_loop") as mock_reason_loop:
        mock_reason_loop.side_effect = KeyboardInterrupt()

        # KeyboardInterrupt ne devrait pas être capturée par main_loop
        with pytest.raises(KeyboardInterrupt):
            main_loop()


def test_main_loop_with_system_exit():
    """🧠 Test de main_loop avec SystemExit (qui ne devrait pas être capturée)"""
    with patch("modules.zeroia.reason_loop.reason_loop") as mock_reason_loop:
        mock_reason_loop.side_effect = SystemExit(1)

        # SystemExit ne devrait pas être capturée par main_loop
        with pytest.raises(SystemExit):
            main_loop()


def test_main_loop_output_formatting():
    """🧠 Test du formatage de sortie de main_loop"""
    with patch("modules.zeroia.reason_loop.reason_loop") as mock_reason_loop:
        mock_reason_loop.return_value = ("monitor", 0.6)

        captured_output = StringIO()
        with patch("sys.stdout", captured_output):
            main_loop()

        output = captured_output.getvalue()
        assert "[ZeroIA] loop started" in output
        # Vérifie que flush=True est utilisé (pas de test direct possible)


def test_main_loop_multiple_calls():
    """🧠 Test d'appels multiples à main_loop"""
    with patch("modules.zeroia.reason_loop.reason_loop") as mock_reason_loop:
        mock_reason_loop.return_value = ("normal", 0.4)

        # Appelle main_loop plusieurs fois
        for i in range(3):
            main_loop()

        # Vérifie que reason_loop a été appelé 3 fois
        assert mock_reason_loop.call_count == 3


def test_main_loop_with_different_exceptions():
    """🧠 Test de main_loop avec différents types d'exceptions"""
    exceptions_to_test = [
        ValueError("Value error"),
        RuntimeError("Runtime error"),
        FileNotFoundError("File not found"),
        PermissionError("Permission denied"),
        ConnectionError("Connection failed"),
    ]

    for exception in exceptions_to_test:
        with patch("modules.zeroia.reason_loop.reason_loop") as mock_reason_loop:
            mock_reason_loop.side_effect = exception

            with patch("modules.zeroia.reason_loop.logger") as mock_logger:
                captured_output = StringIO()
                with patch("sys.stdout", captured_output):
                    main_loop()

                # Vérifie que l'exception a été loggée
                mock_logger.exception.assert_called_once_with(exception)

                # Vérifie le message d'erreur
                output = captured_output.getvalue()
                assert "🚨 ERREUR dans reason_loop()" in output
                assert str(exception) in output


def test_main_loop_logger_configuration():
    """🧠 Test que main_loop utilise le bon logger"""
    with patch("modules.zeroia.reason_loop.reason_loop") as mock_reason_loop:
        mock_reason_loop.side_effect = Exception("Test exception")

        with patch("modules.zeroia.reason_loop.logger") as mock_logger:
            main_loop()

            # Vérifie que logger.exception a été appelé avec l'exception
            mock_logger.exception.assert_called_once()
            args, _ = mock_logger.exception.call_args
            assert isinstance(args[0], Exception)
            assert str(args[0]) == "Test exception"


def test_main_loop_stdout_flushing():
    """🧠 Test que main_loop utilise flush=True pour l'affichage immédiat"""
    with patch("modules.zeroia.reason_loop.reason_loop") as mock_reason_loop:
        mock_reason_loop.return_value = ("reduce_load", 0.75)

        # Mock print pour vérifier les appels avec flush=True
        with patch("builtins.print") as mock_print:
            main_loop()

            # Vérifie que print a été appelé avec flush=True
            mock_print.assert_called_with("[ZeroIA] loop started", flush=True)


def test_main_loop_reason_loop_call():
    """🧠 Test que main_loop appelle reason_loop sans arguments"""
    with patch("modules.zeroia.reason_loop.reason_loop") as mock_reason_loop:
        mock_reason_loop.return_value = ("normal", 0.4)

        main_loop()

        # Vérifie que reason_loop est appelé sans arguments
        mock_reason_loop.assert_called_once_with()


def test_main_loop_exception_handling_preserves_original_exception():
    """🧠 Test que le handling d'exception préserve l'exception orig."""
    original_exception = ValueError("Original error message")

    with patch("modules.zeroia.reason_loop.reason_loop") as mock_reason_loop:
        mock_reason_loop.side_effect = original_exception

        with patch("modules.zeroia.reason_loop.logger") as mock_logger:
            main_loop()

            # Vérifie que l'exception originale est passée au logger
            mock_logger.exception.assert_called_once_with(original_exception)
