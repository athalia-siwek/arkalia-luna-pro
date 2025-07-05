#!/usr/bin/env python3
"""
🔄 Demo ZeroIA Enhanced + Error Recovery Integration v2.7.0
Démontre l'intégration complète du système Error Recovery
dans la boucle de raisonnement ZeroIA Enhanced.
"""

import logging
import sys
from pathlib import Path

from core.ark_logger import ark_logger

# Ajout du chemin modules
sys.path.insert(0, str(Path(__file__).parent.parent / "modules"))

try:
    from zeroia.reason_loop_enhanced import (
        get_circuit_status,
        get_error_recovery_status,
        initialize_components_with_recovery,
        reason_loop_enhanced_with_recovery,
    )

    ENHANCED_AVAILABLE = True
except ImportError as e:
    ark_logger.error(f"⚠️ Import Error Recovery: {e}", extra={"module": "scripts"})
    ENHANCED_AVAILABLE = False

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def demo_integration():
    """Demo principal d'intégration Error Recovery"""
    ark_logger.error("🔄 DEMO: ZeroIA Enhanced + Error Recovery Integration v2.7.0", extra={"module": "scripts"})
    ark_logger.info("=" * 70, extra={"module": "scripts"})

    if not ENHANCED_AVAILABLE:
        ark_logger.info("❌ Modules Enhanced non disponibles", extra={"module": "scripts"})
        return

    # Test 1: Initialisation
    ark_logger.info("\n🔧 === TEST 1: Initialisation des composants ===", extra={"module": "scripts"})
    try:
        cb, es, error_recovery, graceful_degradation = initialize_components_with_recovery()
        ark_logger.info("✅ Circuit Breaker: initialisé", extra={"module": "scripts"})
        ark_logger.info("✅ Event Store: initialisé", extra={"module": "scripts"})
        ark_logger.error(f"🔄 Error Recovery: {'✅' if error_recovery else '❌'}", extra={"module": "scripts"})
        ark_logger.info(f"📉 Graceful Degradation: {'✅' if graceful_degradation else '❌'}", extra={"module": "scripts"})
    except Exception as e:
        raise RuntimeError(f"Erreur demo zeroia with error recovery: {e}") from e
        return

    # Test 2: Status des systèmes
    ark_logger.info("\n📊 === TEST 2: Status des systèmes ===", extra={"module": "scripts"})
    try:
        circuit_status = get_circuit_status()
        ark_logger.info(f"🔄 Circuit Breaker: {circuit_status.get('state', 'unknown', extra={"module": "scripts"})}")

        error_status = get_error_recovery_status()
        ark_logger.error(f"🔄 Error Recovery: {error_status.get('status', 'unknown', extra={"module": "scripts"})}")
    except Exception as e:
        raise RuntimeError(f"Erreur demo zeroia with error recovery: {e}") from e

    # Test 3: Boucle avec contexte normal
    ark_logger.info("\n🧪 === TEST 3: Boucle normale ===", extra={"module": "scripts"})
    try:
        decision, score = reason_loop_enhanced_with_recovery()
        ark_logger.info(f"✅ Décision: {decision} (confiance: {score:.2f}, extra={"module": "scripts"})")
    except Exception as e:
        raise RuntimeError(f"Erreur demo zeroia with error recovery: {e}") from e

    ark_logger.error("\n🎉 Demo terminé - Error Recovery intégré avec succès !", extra={"module": "scripts"})
    ark_logger.info("💡 ZeroIA Enhanced peut maintenant récupérer automatiquement des erreurs", extra={"module": "scripts"})


if __name__ == "__main__":
    demo_integration()
