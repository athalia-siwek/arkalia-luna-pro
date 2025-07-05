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

import argparse
import logging
import pathlib
import subprocess
import sys
from pathlib import Path

from core.ark_logger import ark_logger

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
    ark_logger.info("🚀 DEMO ORCHESTRATOR ENHANCED - Mode Rapide", extra={"module": "scripts"})
    ark_logger.info("=" * 50, extra={"module": "scripts"})

    orchestrator = ZeroIAOrchestrator(
        max_loops=5,
        interval_seconds=0.3,
        circuit_failure_threshold=3,
        timeout=5,
    )

    ark_logger.info("📊 Status initial:", extra={"module": "scripts"})
    status = orchestrator.get_status()
    ark_logger.info(
        f"  - Loops prévus: {status['orchestrator']['max_loops']}", extra={"module": "scripts"}
    )
    ark_logger.info(
        f"  - Intervalle: {status['orchestrator']['interval_seconds']}s",
        extra={"module": "scripts"},
    )
    ark_logger.error(
        f"  - Circuit seuil: {orchestrator.circuit_breaker.failure_threshold}",
        extra={"module": "scripts"},
    )

    ark_logger.info("\n🔄 Exécution en cours...", extra={"module": "scripts"})
    orchestrator.run()

    ark_logger.info("\n✅ Demo rapide terminée!", extra={"module": "scripts"})


def demo_stress() -> None:
    """Démonstration stress test (20 loops)"""
    ark_logger.info("🔥 DEMO ORCHESTRATOR ENHANCED - Mode Stress", extra={"module": "scripts"})
    ark_logger.info("=" * 50, extra={"module": "scripts"})

    orchestrator = ZeroIAOrchestrator(
        max_loops=20,
        interval_seconds=0.1,
        circuit_failure_threshold=2,  # Plus sensible
        timeout=3,
    )

    ark_logger.info("📊 Configuration stress:", extra={"module": "scripts"})
    ark_logger.info("  - 20 loops rapides (0.1s intervalle)", extra={"module": "scripts"})
    ark_logger.info("  - Circuit sensible (seuil=2)", extra={"module": "scripts"})
    ark_logger.info("  - Recovery rapide (3s)", extra={"module": "scripts"})

    ark_logger.info("\n🔄 Stress test en cours...", extra={"module": "scripts"})
    orchestrator.run()

    ark_logger.info("\n🎯 Stress test terminé!", extra={"module": "scripts"})


def demo_monitoring() -> None:
    """Démonstration avec monitoring détaillé"""
    ark_logger.info("📊 DEMO ORCHESTRATOR ENHANCED - Mode Monitoring", extra={"module": "scripts"})
    ark_logger.info("=" * 50, extra={"module": "scripts"})

    ZeroIAOrchestrator(
        max_loops=10,
        interval_seconds=0.5,
        circuit_failure_threshold=4,
        timeout=10,
    )

    ark_logger.info("🔄 Exécution avec monitoring...", extra={"module": "scripts"})

    # Hook pour afficher status périodiquement
    import time

    time.time()

    try:
        # Lancer en background et monitorer
        for i in range(3):  # 3 cycles de monitoring
            ark_logger.info(f"\n📊 === CYCLE MONITORING {i+1}/3 ===", extra={"module": "scripts"})

            # Exécuter quelques loops
            temp_orchestrator = ZeroIAOrchestrator(max_loops=3, interval_seconds=0.2)
            temp_orchestrator.run()

            # Afficher métriques
            status = temp_orchestrator.get_status()
            ark_logger.info(
                f"✅ Loops: {status['orchestrator']['loop_count']}", extra={"module": "scripts"}
            )
            ark_logger.info(
                f"📈 Succès: {status['session_stats']['successful_decisions']}",
                extra={"module": "scripts"},
            )
            ark_logger.error(
                f"❌ Échecs: {status['session_stats']['failed_decisions']}",
                extra={"module": "scripts"},
            )
            ark_logger.info(
                f"🔄 Circuit: {status['circuit_breaker']['state']}", extra={"module": "scripts"}
            )

            time.sleep(0.5)

    except KeyboardInterrupt:
        ark_logger.info("\n⏹️ Monitoring arrêté", extra={"module": "scripts"})

    ark_logger.info("\n📊 Demo monitoring terminée!", extra={"module": "scripts"})


def demo_daemon() -> None:
    """Mode daemon pour container Docker - boucle infinie"""
    ark_logger.info("🔄 ORCHESTRATOR ENHANCED - Mode Daemon", extra={"module": "scripts"})
    ark_logger.info("🐳 Démarrage pour container Docker...", extra={"module": "scripts"})
    ark_logger.info("=" * 50, extra={"module": "scripts"})

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
            ark_logger.info(f"\n🔄 === CYCLE DAEMON {cycle_count} ===", extra={"module": "scripts"})
            ark_logger.info(f"⏰ {time.strftime('%H:%M:%S', extra={"module": "scripts"})}")

            # Exécuter cycle d'orchestration
            orchestrator.run()

            # Afficher status périodique
            if cycle_count % 5 == 0:
                status = orchestrator.get_status()
                ark_logger.info(
                    f"📊 Status après {cycle_count} cycles:", extra={"module": "scripts"}
                )
                ark_logger.info(
                    f"  - Total decisions: {status['session_stats']['total_decisions']}",
                    extra={"module": "scripts"},
                )
                ark_logger.info(
                    f"  - Taux succès: {status['session_stats']['success_rate']:.1f}%",
                    extra={"module": "scripts"},
                )
                ark_logger.info(
                    f"  - Circuit état: {status['circuit_breaker']['state']}",
                    extra={"module": "scripts"},
                )

            # Pause entre cycles (important pour container)
            time.sleep(10)

    except KeyboardInterrupt:
        ark_logger.info("\n⏹️ Daemon arrêté proprement", extra={"module": "scripts"})
    except Exception as e:
        raise RuntimeError(f"Erreur daemon: {e}") from e
        # En mode daemon, on redémarre automatiquement
        ark_logger.info("🔄 Redémarrage automatique dans 5s...", extra={"module": "scripts"})
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
            ark_logger.info(f"✅ Formaté: {d}", extra={"module": "scripts"})
        except subprocess.CalledProcessError as e:
            ark_logger.info(f"⚠️ Erreur formatage {d}: {e}", extra={"module": "scripts"})
            # Fallback: essayer au moins isort
            try:
                subprocess.run(["isort", str(d), "--fix"], check=False)
                ark_logger.info(f"⚠️ Fallback isort appliqué: {d}", extra={"module": "scripts"})
            except Exception:
                ark_logger.info(f"❌ Fallback échoué: {d}", extra={"module": "scripts"})


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

    ark_logger.info("🌕 ARKALIA-LUNA v2.6.0 - ORCHESTRATOR ENHANCED", extra={"module": "scripts"})
    ark_logger.info(
        "🔄 Circuit Breaker + Event Sourcing + Resilience Patterns", extra={"module": "scripts"}
    )
    ark_logger.info("")

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
        ark_logger.info("\n⏹️ Demo interrompue par l'utilisateur", extra={"module": "scripts"})
    except Exception as e:
        raise RuntimeError(f"Erreur demo orchestrator enhanced: {e}") from e

    format_generated()


if __name__ == "__main__":
    main()
