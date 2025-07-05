#!/usr/bin/env python3
"""
🌕 Arkalia-LUNA - Logger Centralisé
📝 Logger structuré conforme cahier des charges v4.0
🔧 Version: 2.8.0
👤 Author: Athalia
📅 Created: 2025-06-27
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


# Configuration du logger centralisé Arkalia
class ArkaliaLogger:
    """Logger centralisé Arkalia conforme cahier des charges v4.0"""

    def __init__(self, module_name: str = "arkalia"):
        self.module_name = module_name
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Configure le logger selon les standards Arkalia"""
        logger = logging.getLogger(f"ark_logger.{self.module_name}")

        # Éviter la duplication des handlers
        if logger.handlers:
            return logger

        logger.setLevel(logging.INFO)

        # Format structuré conforme cahier des charges
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - [%(arkalia_module)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Handler console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Handler fichier avec rotation
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        file_handler = logging.handlers.RotatingFileHandler(
            log_dir / f"{self.module_name}.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger

    def info(self, message: str, extra: dict[str, Any] | None = None) -> None:
        """Log info avec contexte structuré"""
        if extra is None:
            extra = {}
        extra["arkalia_module"] = self.module_name
        extra["timestamp"] = datetime.now().isoformat()
        self.logger.info(message, extra=extra)

    def error(self, message: str, extra: dict[str, Any] | None = None) -> None:
        """Log error avec contexte structuré"""
        if extra is None:
            extra = {}
        extra["arkalia_module"] = self.module_name
        extra["timestamp"] = datetime.now().isoformat()
        self.logger.error(message, extra=extra)

    def warning(self, message: str, extra: dict[str, Any] | None = None) -> None:
        """Log warning avec contexte structuré"""
        if extra is None:
            extra = {}
        extra["arkalia_module"] = self.module_name
        extra["timestamp"] = datetime.now().isoformat()
        self.logger.warning(message, extra=extra)

    def debug(self, message: str, extra: dict[str, Any] | None = None) -> None:
        """Log debug avec contexte structuré"""
        if extra is None:
            extra = {}
        extra["arkalia_module"] = self.module_name
        extra["timestamp"] = datetime.now().isoformat()
        self.logger.debug(message, extra=extra)

    def critical(self, message: str, extra: dict[str, Any] | None = None) -> None:
        """Log critical avec contexte structuré"""
        if extra is None:
            extra = {}
        extra["arkalia_module"] = self.module_name
        extra["timestamp"] = datetime.now().isoformat()
        self.logger.critical(message, extra=extra)

# Instance globale du logger Arkalia
ark_logger = ArkaliaLogger("core")

def get_ark_logger(module_name: str) -> ArkaliaLogger:
    """Factory pour obtenir un logger Arkalia pour un module spécifique"""
    return ArkaliaLogger(module_name)

# Fonction de compatibilité pour migration
def setup_ark_logger(module_name: str) -> ArkaliaLogger:
    """Setup le logger Arkalia pour un module (compatibilité)"""
    return get_ark_logger(module_name)
