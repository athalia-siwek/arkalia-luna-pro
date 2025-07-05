#!/usr/bin/env python3
"""
🔄 Demo ZeroIA Enhanced + Error Recovery Integration v2.7.0
Démontre l'intégration complète du système Error Recovery
dans la boucle de raisonnement ZeroIA Enhanced.
"""

# import logging
# import sys
from pathlib import Path

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
    print(f"⚠️ Import Error Recovery: {e}")
    ENHANCED_AVAILABLE = False

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def demo_integration():
    """Demo principal d'intégration Error Recovery"""
    print("🔄 DEMO: ZeroIA Enhanced + Error Recovery Integration v2.7.0")
    print("=" * 70)

    if not ENHANCED_AVAILABLE:
        print("❌ Modules Enhanced non disponibles")
        return

    # Test 1: Initialisation
    print("\n🔧 === TEST 1: Initialisation des composants ===")
    try:
        cb, es, error_recovery, graceful_degradation = initialize_components_with_recovery()
        print("✅ Circuit Breaker: initialisé")
        print("✅ Event Store: initialisé")
        print(f"🔄 Error Recovery: {'✅' if error_recovery else '❌'}")
        print(f"📉 Graceful Degradation: {'✅' if graceful_degradation else '❌'}")
    except Exception as e:
        raise RuntimeError(f"Erreur demo zeroia with error recovery: {e}") from e
        return

    # Test 2: Status des systèmes
    print("\n📊 === TEST 2: Status des systèmes ===")
    try:
        circuit_status = get_circuit_status()
        print(f"🔄 Circuit Breaker: {circuit_status.get('state', 'unknown')}")

        error_status = get_error_recovery_status()
        print(f"🔄 Error Recovery: {error_status.get('status', 'unknown')}")
    except Exception as e:
        raise RuntimeError(f"Erreur demo zeroia with error recovery: {e}") from e

    # Test 3: Boucle avec contexte normal
    print("\n🧪 === TEST 3: Boucle normale ===")
    try:
        decision, score = reason_loop_enhanced_with_recovery()
        print(f"✅ Décision: {decision} (confiance: {score:.2f})")
    except Exception as e:
        raise RuntimeError(f"Erreur demo zeroia with error recovery: {e}") from e

    print("\n🎉 Demo terminé - Error Recovery intégré avec succès !")
    print("💡 ZeroIA Enhanced peut maintenant récupérer automatiquement des erreurs")


if __name__ == "__main__":
    demo_integration()
