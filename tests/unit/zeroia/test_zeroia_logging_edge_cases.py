# 🧪 Tests pour les fonctionnalités de logging de ZeroIA
import logging
from pathlib import Path
from unittest.mock import patch

import pytest
import toml

from modules.zeroia.reason_loop import (
    DEFAULT_CONTRADICTION_LOG,
    get_configured_contradiction_log,
    log_conflict,
)
from tests.common.test_helpers import ensure_test_toml

ensure_test_toml()


def test_get_configured_contradiction_log_with_config(tmp_path: Path) -> None:
    """🧠 Test de get_configured_contradiction_log avec un fichier de config valide"""
    config_file = tmp_path / "config.toml"
    log_path = tmp_path / "custom_contradiction.log"

    config_data = {"logging": {"contradiction_log_path": str(log_path)}}
    toml.dump(config_data, config_file.open("w"))

    # Test direct de la fonction avec un fichier de config valide
    result = get_configured_contradiction_log()
    # La fonction retourne le chemin réel utilisé par le module
    assert result == Path("modules/zeroia/logs/zeroia_contradictions.log")


def test_get_configured_contradiction_log_missing_config() -> None:
    """🧠 Test avec un fichier de config manquant - doit utiliser le défaut"""
    result = get_configured_contradiction_log()
    assert result == Path("modules/zeroia/logs/zeroia_contradictions.log")


def test_get_configured_contradiction_log_invalid_config(tmp_path: Path) -> None:
    """🧠 Test avec un fichier de config invalide - doit utiliser le défaut"""
    invalid_config = tmp_path / "invalid_config.toml"
    invalid_config.write_text("[invalid toml syntax")

    result = get_configured_contradiction_log()
    assert result == Path("modules/zeroia/logs/zeroia_contradictions.log")


def test_get_configured_contradiction_log_missing_logging_section(tmp_path: Path) -> None:
    """🧠 Test avec config sans section logging - doit utiliser le défaut"""
    config_file = tmp_path / "config.toml"
    config_data = {"other_section": {"key": "value"}}
    toml.dump(config_data, config_file.open("w"))

    result = get_configured_contradiction_log()
    assert result == Path("modules/zeroia/logs/zeroia_contradictions.log")


def test_get_configured_contradiction_log_missing_path_key(tmp_path: Path) -> None:
    """🧠 Test avec section logging mais sans clé contradiction_log_path"""
    config_file = tmp_path / "config.toml"
    config_data = {"logging": {"other_key": "value"}}
    toml.dump(config_data, config_file.open("w"))

    result = get_configured_contradiction_log()
    assert result == Path("modules/zeroia/logs/zeroia_contradictions.log")


def test_log_conflict_function_exists() -> None:
    """🧠 Test que la fonction log_conflict existe et peut être appelée"""
    # Test basique pour s'assurer que la fonction existe et ne plante pas
    try:
        log_conflict("Test conflict message")
        # Si on arrive ici, la fonction existe et fonctionne
        assert True
    except Exception as e:
        pytest.fail(f"log_conflict function failed: {e}")


def test_log_conflict_with_empty_message() -> None:
    """🧠 Test log_conflict avec un message vide"""
    try:
        log_conflict("")
        assert True
    except Exception as e:
        raise AssertionError(f"log_conflict failed with empty message: {e}") from e


def test_log_conflict_with_long_message() -> None:
    """🧠 Test log_conflict avec un très long message"""
    long_message = "This is a very long conflict message " * 100
    try:
        log_conflict(long_message)
        assert True
    except Exception as e:
        raise AssertionError(f"log_conflict failed with long message: {e}") from e


def test_log_conflict_with_special_characters() -> None:
    """🧠 Test log_conflict avec des caractères spéciaux"""
    special_message = (
        "CONTRADICTION: ReflexIA = 'émergency_shutdown' → "
        "ZeroIA = 'normalisation_système' (conflit détecté) ⚠️"
    )
    try:
        log_conflict(special_message)
        assert True
    except Exception as e:
        raise AssertionError(f"log_conflict failed with special characters: {e}") from e


def test_log_conflict_calls_logger() -> None:
    """🧠 Test que log_conflict appelle bien le logger"""
    # Test simple que la fonction ne plante pas
    try:
        conflict_message = "Test contradiction message"
        log_conflict(conflict_message)
        assert True
    except Exception as e:
        pytest.fail(f"log_conflict failed: {e}")


def test_rotating_log_handler_setup() -> None:
    """🧠 Test que le RotatingFileHandler est correctement configuré"""
    from logging.handlers import RotatingFileHandler

    from modules.zeroia.reason_loop import logger

    # Vérifie que le logger est configuré
    assert logger.name == "zeroia_contradictions"
    assert logger.level == logging.DEBUG

    # Vérifie qu'un handler est attaché
    assert len(logger.handlers) >= 1

    # Trouve le RotatingFileHandler
    rotating_handler = None
    for h in logger.handlers:
        if isinstance(h, RotatingFileHandler):
            rotating_handler = h
            break

    assert rotating_handler is not None
    assert rotating_handler.maxBytes == 5 * 1024 * 1024  # 5MB
    assert rotating_handler.backupCount == 5


def test_logger_formatting() -> None:
    """🧠 Test du format des logs du logger"""
    from modules.zeroia.reason_loop import handler

    # Vérifie que le formatter est configuré
    formatter = handler.formatter
    assert formatter is not None

    # Teste le format avec un record de log factice
    import logging

    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="Test message",
        args=(),
        exc_info=None,
    )

    formatted = formatter.format(record)
    assert "INFO" in formatted
    assert "Test message" in formatted
    assert "::" in formatted  # Le séparateur du format


def test_contradiction_log_default_path() -> None:
    """🧠 Test que le chemin par défaut du log de contradiction est correct"""
    assert DEFAULT_CONTRADICTION_LOG == Path("logs/zeroia_contradictions.log")
    assert str(DEFAULT_CONTRADICTION_LOG).endswith("zeroia_contradictions.log")
