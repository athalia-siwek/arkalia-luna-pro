#!/usr/bin/env python3
"""
🌕 ARKALIA MASTER ORCHESTRATOR LAUNCHER v4.0.0

Script de lancement du Master Orchestrator
Coordonne l'écosystème complet Arkalia-LUNA
"""

from core.ark_logger import ark_logger
import asyncio
import logging
import sys
from pathlib import Path

# Ajouter le path des modules
sys.path.append(str(Path(__file__).parent.parent / "modules"))

from modules.arkalia_master.orchestrator_ultimate import (
    ArkaliaOrchestrator,
    OrchestratorConfig,
    orchestrate_full_ecosystem,
)


def setup_logging(verbose: bool = False):
    """Configure le logging"""
    log_level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("logs/arkalia_master.log", mode="a"),
        ],
    )


def print_banner():
    """Affiche le banner de démarrage"""
    ark_logger.info("=" * 80, extra={"module": "scripts"})
    ark_logger.info("🌕 ARKALIA MASTER ORCHESTRATOR v4.0.0 - ULTIMATE EDITION", extra={"module": "scripts"})
    ark_logger.info("=" * 80, extra={"module": "scripts"})
    ark_logger.info("🧠 Modules IA Coordonnés    : 10 modules (ZeroIA, ReflexIA, etc.)", extra={"module": "scripts"})
    ark_logger.info("🔄 Cycles Adaptatifs        : 5s urgent → 30s normal → 300s deep", extra={"module": "scripts"})
    ark_logger.error("🛡️ Protection Globale        : Circuit breaker + Error recovery", extra={"module": "scripts"})
    ark_logger.info("🌐 État Global Unifié       : Synchronisation inter-modules", extra={"module": "scripts"})
    ark_logger.info("📊 Monitoring Intégré       : Métriques temps réel", extra={"module": "scripts"})
    ark_logger.info("🐳 Container Ready          : Mode daemon optimisé", extra={"module": "scripts"})
    ark_logger.info("=" * 80, extra={"module": "scripts"})


async def main():
    """Point d'entrée principal"""
    import argparse

    parser = argparse.ArgumentParser(
        description="🌕 Arkalia Master Orchestrator v4.0.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation :
  python ark-master-orchestrator.py --mode daemon              # Production
  python ark-master-orchestrator.py --mode test --cycles 10    # Test 10 cycles
  python ark-master-orchestrator.py --mode status              # Statut uniquement
  python ark-master-orchestrator.py --verbose                  # Logs détaillés
        """,
    )

    parser.add_argument(
        "--mode",
        choices=["daemon", "test", "status"],
        default="daemon",
        help="Mode d'exécution (défaut: daemon)",
    )
    parser.add_argument("--cycles", type=int, help="Nombre de cycles en mode test")
    parser.add_argument("--verbose", action="store_true", help="Logs détaillés (DEBUG)")
    parser.add_argument("--config", type=str, help="Fichier de configuration personnalisé")
    parser.add_argument("--enable-modules", nargs="+", help="Modules à activer (par défaut: tous)")

    args = parser.parse_args()

    # Configuration logging
    setup_logging(args.verbose)

    # Banner
    print_banner()

    # Configuration
    config = OrchestratorConfig()

    if args.config:
        ark_logger.info(f"📁 Chargement config personnalisée: {args.config}", extra={"module": "scripts"})
        # TODO: Implémenter chargement config

    if args.enable_modules:
        config.enabled_modules = args.enable_modules
        ark_logger.info(f"🔧 Modules activés: {', '.join(args.enable_modules, extra={"module": "scripts"})}")

    ark_logger.info(f"⚙️ Mode: {args.mode.upper(, extra={"module": "scripts"})}")
    ark_logger.info(f"🔧 Modules actifs: {len(config.enabled_modules, extra={"module": "scripts"})}/10")
    ark_logger.info("")

    try:
        if args.mode == "daemon":
            ark_logger.info("🚀 Démarrage mode DAEMON (production)...", extra={"module": "scripts"})
            ark_logger.info("   Ctrl+C pour arrêter", extra={"module": "scripts"})
            ark_logger.info("")
            await orchestrate_full_ecosystem(config)

        elif args.mode == "test":
            cycles = args.cycles or 5
            ark_logger.info(f"🧪 Mode TEST - {cycles} cycles", extra={"module": "scripts"})
            ark_logger.info("")
            await orchestrate_full_ecosystem(config, max_cycles=cycles)

        elif args.mode == "status":
            ark_logger.info("📊 AFFICHAGE STATUT", extra={"module": "scripts"})
            ark_logger.info("")
            orchestrator = ArkaliaOrchestrator(config)
            status = orchestrator.get_status()

            ark_logger.info("🌕 ARKALIA ORCHESTRATOR STATUS", extra={"module": "scripts"})
            ark_logger.info("=" * 50, extra={"module": "scripts"})
            ark_logger.info(f"Version        : {status['orchestrator']['version']}", extra={"module": "scripts"})
            ark_logger.info(f"Running        : {status['orchestrator']['is_running']}", extra={"module": "scripts"})
            ark_logger.info(f"Uptime         : {status['orchestrator']['uptime_seconds']:.1f}s", extra={"module": "scripts"})
            ark_logger.info(f"Cycles         : {status['orchestrator']['cycle_count']}", extra={"module": "scripts"})
            ark_logger.info(f"Current Mode   : {status['orchestrator']['current_mode'].upper(, extra={"module": "scripts"})}")
            ark_logger.info(f"Success Rate   : {status['orchestrator']['success_rate']}%", extra={"module": "scripts"})
            ark_logger.info("")

            ark_logger.info("📋 MODULES STATUS:", extra={"module": "scripts"})
            ark_logger.info("-" * 30, extra={"module": "scripts"})
            for module_name, module_info in status["modules"].items():
                status_icon = {
                    "healthy": "✅",
                    "degraded": "⚠️",
                    "critical": "❌",
                    "offline": "🔴",
                    "initializing": "🔄",
                }.get(module_info["status"], "❓")

                ark_logger.info(f"{status_icon} {module_name:12} : {module_info['status'].upper(, extra={"module": "scripts"})}")
                if module_info["execution_count"] > 0:
                    ark_logger.info(f"   Executions  : {module_info['execution_count']}", extra={"module": "scripts"})
                    ark_logger.error(f"   Errors      : {module_info['error_count']}", extra={"module": "scripts"})

    except KeyboardInterrupt:
        ark_logger.info("\n⏹️ Arrêté par l'utilisateur", extra={"module": "scripts"})
        ark_logger.info("✅ Orchestration terminée proprement", extra={"module": "scripts"})

    except Exception as e:
        raise RuntimeError(f"Erreur orchestrator: {e}") from e


if __name__ == "__main__":
    asyncio.run(main())
