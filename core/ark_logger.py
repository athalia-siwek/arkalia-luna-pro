"""
Logger principal pour Arkalia-LUNA
"""

import logging
import sys
from pathlib import Path
from typing import Optional


# Configuration du logger principal
def setup_logger(
    name: str = "arkalia", level: int = logging.INFO, log_file: Path | None = None
) -> logging.Logger:
    """Configure et retourne le logger principal Arkalia."""

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Éviter les handlers dupliqués
    if logger.handlers:
        return logger

    # Format personnalisé
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handler console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler fichier si spécifié
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# Logger principal global
ark_logger = setup_logger("arkalia")


# Loggers spécialisés
def get_module_logger(module_name: str) -> logging.Logger:
    """Retourne un logger spécialisé pour un module."""
    return logging.getLogger(f"arkalia.{module_name}")


def get_performance_logger() -> logging.Logger:
    """Retourne un logger pour les métriques de performance."""
    return logging.getLogger("arkalia.performance")


def get_security_logger() -> logging.Logger:
    """Retourne un logger pour les événements de sécurité."""
    return logging.getLogger("arkalia.security")


# Fonctions utilitaires
def log_function_call(func_name: str, module: str = "core"):
    """Décorateur pour logger les appels de fonction."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = get_module_logger(module)
            logger.debug(f"🧪 {func_name} déclaré")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def log_error(error: Exception, context: str = "", module: str = "core"):
    """Log une erreur avec contexte."""
    logger = get_module_logger(module)
    logger.error(f"❌ Erreur dans {context}: {error}")


def log_success(message: str, module: str = "core"):
    """Log un succès."""
    logger = get_module_logger(module)
    logger.info(f"✅ {message}")


def log_warning(message: str, module: str = "core"):
    """Log un avertissement."""
    logger = get_module_logger(module)
    logger.warning(f"⚠️ {message}")


def log_info(message: str, module: str = "core"):
    """Log une information."""
    logger = get_module_logger(module)
    logger.info(f"ℹ️ {message}")


# Export des fonctions principales
__all__ = [
    "ark_logger",
    "setup_logger",
    "get_module_logger",
    "get_performance_logger",
    "get_security_logger",
    "log_function_call",
    "log_error",
    "log_success",
    "log_warning",
    "log_info",
]
