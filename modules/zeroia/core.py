#!/usr/bin/env python3

"""
🧠 modules/zeroia/core.py
ZeroIA Core - Point d'entrée principal du système de raisonnement

Module core simplifié qui délègue aux composants enhanced spécialisés.
"""

import logging
import os
import time
from pathlib import Path
from typing import Dict, Optional, Tuple

from .reason_loop_enhanced import (
    get_circuit_status,
    get_error_recovery_status,
    initialize_components_with_recovery,
    reason_loop_enhanced_with_recovery,
)

logger = logging.getLogger(__name__)


class ZeroIACore:
    """
    Classe principale ZeroIA - Interface simplifiée pour le système complet
    """

    def __init__(self):
        """Initialise le core ZeroIA"""
        self.initialized = False
        self.components = None

    def initialize(self) -> bool:
        """
        Initialise tous les composants ZeroIA

        Returns:
            bool: True si succès, False sinon
        """
        try:
            # Add startup delay to ensure dependencies are ready
            startup_delay = int(os.getenv("ZEROIA_STARTUP_DELAY", "15"))
            logger.info(f"⏳ Waiting {startup_delay}s for system stabilization...")
            time.sleep(startup_delay)

            # Initialize with recovery mechanism
            retry_count = 0
            max_retries = int(os.getenv("ZEROIA_MAX_RETRIES", "5"))

            while retry_count < max_retries:
                try:
                    logger.info(f"🔄 Initialization attempt {retry_count + 1}/{max_retries}")
                    self.components = initialize_components_with_recovery()
                    self.initialized = True
                    logger.info("🚀 ZeroIA Core initialisé avec succès")
                    return True
                except Exception as e:
                    retry_count += 1
                    if retry_count >= max_retries:
                        logger.error(f"❌ Échec initialisation après {max_retries} tentatives: {e}")
                        return False
                    logger.warning(f"⚠️ Tentative {retry_count} échouée: {e}")
                    time.sleep(min(5 * retry_count, 30))  # Exponential backoff

            return False
        except Exception as e:
            logger.error(f"❌ Erreur critique initialisation ZeroIA Core: {e}")
            return False

    def run_decision_cycle(self, context_path: Path | None = None) -> tuple[str, float]:
        """
        Exécute un cycle de décision complet

        Args:
            context_path: Chemin vers le contexte (optionnel)

        Returns:
            Tuple[str, float]: (décision, score_confiance)
        """
        if not self.initialized:
            logger.warning("⚠️ ZeroIA Core non initialisé")
            return "error", 0.0

        try:
            return reason_loop_enhanced_with_recovery(context_path=context_path)
        except Exception as e:
            logger.error(f"❌ Erreur cycle de décision: {e}")
            return "error", 0.0

    def get_status(self) -> dict:
        """
        Retourne l'état complet du système ZeroIA

        Returns:
            Dict: État détaillé du système
        """
        if not self.initialized:
            return {
                "status": "not_initialized",
                "initialized": False,
                "error": "ZeroIA Core non initialisé",
            }

        try:
            circuit_status = get_circuit_status()
            recovery_status = get_error_recovery_status()

            return {
                "status": "operational",
                "initialized": True,
                "circuit_breaker": circuit_status,
                "error_recovery": recovery_status,
                "version": "3.0.0-enhanced",
            }
        except Exception as e:
            return {"status": "error", "initialized": self.initialized, "error": str(e)}


# Instance globale (singleton pattern simple)
_zeroia_core_instance: ZeroIACore | None = None


def get_zeroia_core() -> ZeroIACore:
    """
    Retourne l'instance singleton de ZeroIA Core

    Returns:
        ZeroIACore: Instance du core
    """
    global _zeroia_core_instance

    if _zeroia_core_instance is None:
        _zeroia_core_instance = ZeroIACore()

    return _zeroia_core_instance


def quick_decision(context_path: Path | None = None) -> tuple[str, float]:
    """
    Interface rapide pour une décision ZeroIA

    Args:
        context_path: Chemin vers le contexte (optionnel)

    Returns:
        Tuple[str, float]: (décision, score_confiance)
    """
    core = get_zeroia_core()

    if not core.initialized:
        core.initialize()

    return core.run_decision_cycle(context_path)


def health_check() -> dict:
    """
    Vérifie l'état de santé du core ZeroIA

    Returns:
        Dict: État de santé détaillé
    """
    try:
        core = get_zeroia_core()
        return core.get_status()
    except Exception as e:
        return {"status": "critical_error", "error": str(e), "initialized": False}


if __name__ == "__main__":
    # Test rapide du core
    print("🧠 ZeroIA Core - Test de démarrage")

    core = get_zeroia_core()

    if core.initialize():
        print("✅ Initialisation réussie")

        decision, confidence = core.run_decision_cycle()
        print(f"🎯 Décision: {decision} (confiance: {confidence:.2f})")

        status = core.get_status()
        print(f"📊 État: {status['status']}")
    else:
        print("❌ Échec initialisation")
