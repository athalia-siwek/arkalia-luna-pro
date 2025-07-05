#!/usr/bin/env python3
# 🚀 scripts/demo_orchestrator_enhanced.py
"""
Démonstration de l'Orchestrator ZeroIA Enhanced v2.6.0

FEATURES:
- Circuit Breaker avec protection cascade failures
- Event Sourcing pour traçabilité complète
- Resilience patterns enterprise
- Monitoring et métriques temps réel
"""

# import argparse
# import logging
# import pathlib
# import subprocess
# import sys
from pathlib import Path

# Ajouter le path des modules
sys.path.append(str(Path(__file__).parent.parent / "modules"))

from modules.zeroia.orchestrator_enhanced import ZeroIAOrchestrator

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)


def demo_quick() -> None:
    """Démonstration rapide (5 loops)"""
    print("🚀 DEMO ORCHESTRATOR ENHANCED - Mode Rapide")
    print("=" * 50)

    orchestrator = ZeroIAOrchestrator(
        max_loops=5,
        interval_seconds=0.3,
        circuit_failure_threshold=3,
        timeout=5,
    )

    print("📊 Status initial:")
    status = orchestrator.get_status()
    print(f"  - Loops prévus: {status['orchestrator']['max_loops']}")
    print(f"  - Intervalle: {status['orchestrator']['interval_seconds']}s")
    print(f"  - Circuit seuil: {orchestrator.circuit_breaker.failure_threshold}")

    print("\n🔄 Exécution en cours...")
    orchestrator.run()

    print("\n✅ Demo rapide terminée!")


def demo_stress() -> None:
    """Démonstration stress test (20 loops)"""
    print("🔥 DEMO ORCHESTRATOR ENHANCED - Mode Stress")
    print("=" * 50)

    orchestrator = ZeroIAOrchestrator(
        max_loops=20,
        interval_seconds=0.1,
        circuit_failure_threshold=2,  # Plus sensible
        timeout=3,
    )

    print("📊 Configuration stress:")
    print("  - 20 loops rapides (0.1s intervalle)")
    print("  - Circuit sensible (seuil=2)")
    print("  - Recovery rapide (3s)")

    print("\n🔄 Stress test en cours...")
    orchestrator.run()

    print("\n🎯 Stress test terminé!")


def demo_monitoring() -> None:
    """Démonstration avec monitoring détaillé"""
    print("📊 DEMO ORCHESTRATOR ENHANCED - Mode Monitoring")
    print("=" * 50)

    ZeroIAOrchestrator(
        max_loops=10,
        interval_seconds=0.5,
        circuit_failure_threshold=4,
        timeout=10,
    )

    print("🔄 Exécution avec monitoring...")

    # Hook pour afficher status périodiquement
    import time

    time.time()

    try:
        # Lancer en background et monitorer
        for i in range(3):  # 3 cycles de monitoring
            print(f"\n📊 === CYCLE MONITORING {i+1}/3 ===")

            # Exécuter quelques loops
            temp_orchestrator = ZeroIAOrchestrator(max_loops=3, interval_seconds=0.2)
            temp_orchestrator.run()

            # Afficher métriques
            status = temp_orchestrator.get_status()
            print(f"✅ Loops: {status['orchestrator']['loop_count']}")
            print(f"📈 Succès: {status['session_stats']['successful_decisions']}")
            print(f"❌ Échecs: {status['session_stats']['failed_decisions']}")
            print(f"🔄 Circuit: {status['circuit_breaker']['state']}")

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n⏹️ Monitoring arrêté")

    print("\n📊 Demo monitoring terminée!")


def demo_daemon() -> None:
    """Mode daemon pour container Docker - boucle infinie"""
    print("🔄 ORCHESTRATOR ENHANCED - Mode Daemon")
    print("🐳 Démarrage pour container Docker...")
    print("=" * 50)

    import time

    # Configuration daemon adaptée container
    orchestrator = ZeroIAOrchestrator(
        max_loops=100,  # Nombreux loops par cycle
        interval_seconds=2.0,  # Plus lent pour container
        circuit_failure_threshold=5,
        timeout=30,
    )

    cycle_count = 0

    try:
        while True:  # Boucle infinie pour daemon
            cycle_count += 1
            print(f"\n🔄 === CYCLE DAEMON {cycle_count} ===")
            print(f"⏰ {time.strftime('%H:%M:%S')}")

            # Exécuter cycle d'orchestration
            orchestrator.run()

            # Afficher status périodique
            if cycle_count % 5 == 0:
                status = orchestrator.get_status()
                print(f"📊 Status après {cycle_count} cycles:")
                print(f"  - Total decisions: {status['session_stats']['total_decisions']}")
                print(f"  - Taux succès: {status['session_stats']['success_rate']:.1f}%")
                print(f"  - Circuit état: {status['circuit_breaker']['state']}")

            # Pause entre cycles (important pour container)
            time.sleep(10)

    except KeyboardInterrupt:
        print("\n⏹️ Daemon arrêté proprement")
    except Exception as e:
        raise RuntimeError(f"Erreur daemon: {e}") from e
        # En mode daemon, on redémarre automatiquement
        print("🔄 Redémarrage automatique dans 5s...")
        time.sleep(5)
        demo_daemon()  # Relance recursive


def format_generated():
    """Formate tous les dossiers generated avec isort + black."""
    for d in pathlib.Path(".").rglob("generated"):
        try:
            # Tri des imports avec isort (compatible black)
            subprocess.run(["isort", str(d), "--profile", "black"], check=True)
            # Formatage du code avec black
            subprocess.run(["black", str(d), "--quiet"], check=True)
            print(f"✅ Formaté: {d}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Erreur formatage {d}: {e}")
            # Fallback: essayer au moins isort
            try:
                subprocess.run(["isort", str(d), "--fix"], check=False)
                print(f"⚠️ Fallback isort appliqué: {d}")
            except Exception:
                print(f"❌ Fallback échoué: {d}")


def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(description="Demo Orchestrator ZeroIA Enhanced")
    parser.add_argument(
        "--mode",
        choices=["quick", "stress", "monitoring", "daemon"],
        default="quick",
        help="Mode de démonstration",
    )
    parser.add_argument("--logs", action="store_true", help="Activer logs détaillés")

    args = parser.parse_args()

    if args.logs:
        logging.getLogger().setLevel(logging.DEBUG)

    print("🌕 ARKALIA-LUNA v2.6.0 - ORCHESTRATOR ENHANCED")
    print("🔄 Circuit Breaker + Event Sourcing + Resilience Patterns")
    print()

    try:
        if args.mode == "quick":
            demo_quick()
        elif args.mode == "stress":
            demo_stress()
        elif args.mode == "monitoring":
            demo_monitoring()
        elif args.mode == "daemon":
            demo_daemon()

    except KeyboardInterrupt:
        print("\n⏹️ Demo interrompue par l'utilisateur")
    except Exception as e:
        raise RuntimeError(f"Erreur demo orchestrator enhanced: {e}") from e

    format_generated()


if __name__ == "__main__":
    main()
