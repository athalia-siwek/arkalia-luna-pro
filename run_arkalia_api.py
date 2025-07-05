#!/usr/bin/env python3
"""
🚀 Script de démarrage robuste pour l'API Arkalia-LUNA
Gestion d'erreurs et healthcheck intégré
"""

import logging
import os
import sys
import time
from pathlib import Path

# Configuration logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def check_dependencies():
    """Vérification des dépendances critiques"""
    try:
        import fastapi
        import uvicorn

        logger.info("✅ FastAPI et Uvicorn disponibles")
        return True
    except ImportError as e:
        logger.error(f"❌ Dépendance manquante: {e}")
        return False


def check_modules():
    """Vérification des modules critiques"""
    critical_modules = [
        "helloria/core.py",
        "modules/reflexia/core.py",
        "modules/zeroia/core.py",
        "modules/assistantia/core.py",
    ]

    missing_modules = []
    for module in critical_modules:
        if not Path(module).exists():
            missing_modules.append(module)

    if missing_modules:
        logger.warning(f"⚠️ Modules manquants: {missing_modules}")
        return False

    logger.info("✅ Tous les modules critiques présents")
    return True


def create_directories():
    """Création des répertoires nécessaires"""
    directories = ["logs", "state", "cache", "modules/zeroia/state", "modules/assistantia/logs"]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

    logger.info("✅ Répertoires créés")


def start_api():
    """Démarrage de l'API avec gestion d'erreurs"""
    try:
        # Vérifications préalables
        if not check_dependencies():
            logger.error("❌ Dépendances manquantes")
            sys.exit(1)

        if not check_modules():
            logger.warning("⚠️ Certains modules manquants, démarrage en mode dégradé")

        create_directories()

        # Import de l'application
        from helloria.core import app

        logger.info("🚀 Démarrage de l'API Arkalia-LUNA...")

        # Configuration uvicorn
        import uvicorn

        uvicorn.run(
            app,
            host="127.0.0.1",  # nosec B104 - Interface locale pour développement
            port=8000,
            workers=1,
            access_log=True,
            log_level="info",
            reload=False,
        )

    except Exception as e:
        logger.error(f"❌ Erreur de démarrage: {e}")
        sys.exit(1)


if __name__ == "__main__":
    start_api()
