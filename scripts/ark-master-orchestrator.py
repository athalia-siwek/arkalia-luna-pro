#!/usr/bin/env python3
"""
🌕 ARKALIA MASTER ORCHESTRATOR LAUNCHER v4.0.0

Script de lancement du Master Orchestrator
Coordonne l'écosystème complet Arkalia-LUNA
"""

import asyncio
import logging
import sys
from pathlib import Path

# Ajouter le path des modules
sys.path.append(str(Path(__file__).parent.parent / "modules"))

from modules.arkalia_master.orchestrator_ultimate import (
    ArkaliaOrchestrator,
    OrchestratorConfig,
    CycleMode,
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
        ]
    )

def print_banner():
    """Affiche le banner de démarrage"""
    print("=" * 80)
    print("🌕 ARKALIA MASTER ORCHESTRATOR v4.0.0 - ULTIMATE EDITION")
    print("=" * 80)
    print("🧠 Modules IA Coordonnés    : 10 modules (ZeroIA, ReflexIA, etc.)")
    print("🔄 Cycles Adaptatifs        : 5s urgent → 30s normal → 300s deep")
    print("🛡️ Protection Globale        : Circuit breaker + Error recovery")
    print("🌐 État Global Unifié       : Synchronisation inter-modules")
    print("📊 Monitoring Intégré       : Métriques temps réel")
    print("🐳 Container Ready          : Mode daemon optimisé")
    print("=" * 80)

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
        """
    )
    
    parser.add_argument(
        "--mode", 
        choices=["daemon", "test", "status"], 
        default="daemon",
        help="Mode d'exécution (défaut: daemon)"
    )
    parser.add_argument(
        "--cycles", 
        type=int, 
        help="Nombre de cycles en mode test"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="Logs détaillés (DEBUG)"
    )
    parser.add_argument(
        "--config", 
        type=str, 
        help="Fichier de configuration personnalisé"
    )
    parser.add_argument(
        "--enable-modules",
        nargs="+",
        help="Modules à activer (par défaut: tous)"
    )
    
    args = parser.parse_args()
    
    # Configuration logging
    setup_logging(args.verbose)
    
    # Banner
    print_banner()
    
    # Configuration
    config = OrchestratorConfig()
    
    if args.config:
        print(f"📁 Chargement config personnalisée: {args.config}")
        # TODO: Implémenter chargement config
        
    if args.enable_modules:
        config.enabled_modules = args.enable_modules
        print(f"🔧 Modules activés: {', '.join(args.enable_modules)}")
    
    print(f"⚙️ Mode: {args.mode.upper()}")
    print(f"🔧 Modules actifs: {len(config.enabled_modules)}/10")
    print()
    
    try:
        if args.mode == "daemon":
            print("🚀 Démarrage mode DAEMON (production)...")
            print("   Ctrl+C pour arrêter")
            print()
            await orchestrate_full_ecosystem(config)
            
        elif args.mode == "test":
            cycles = args.cycles or 5
            print(f"🧪 Mode TEST - {cycles} cycles")
            print()
            await orchestrate_full_ecosystem(config, max_cycles=cycles)
            
        elif args.mode == "status":
            print("📊 AFFICHAGE STATUT")
            print()
            orchestrator = ArkaliaOrchestrator(config)
            status = orchestrator.get_status()
            
            print("🌕 ARKALIA ORCHESTRATOR STATUS")
            print("=" * 50)
            print(f"Version        : {status['orchestrator']['version']}")
            print(f"Running        : {status['orchestrator']['is_running']}")
            print(f"Uptime         : {status['orchestrator']['uptime_seconds']:.1f}s")
            print(f"Cycles         : {status['orchestrator']['cycle_count']}")
            print(f"Current Mode   : {status['orchestrator']['current_mode'].upper()}")
            print(f"Success Rate   : {status['orchestrator']['success_rate']}%")
            print()
            
            print("📋 MODULES STATUS:")
            print("-" * 30)
            for module_name, module_info in status['modules'].items():
                status_icon = {
                    'healthy': '✅',
                    'degraded': '⚠️',
                    'critical': '❌',
                    'offline': '🔴',
                    'initializing': '🔄'
                }.get(module_info['status'], '❓')
                
                print(f"{status_icon} {module_name:12} : {module_info['status'].upper()}")
                if module_info['execution_count'] > 0:
                    print(f"   Executions  : {module_info['execution_count']}")
                    print(f"   Errors      : {module_info['error_count']}")
            
    except KeyboardInterrupt:
        print("\n⏹️ Arrêté par l'utilisateur")
        print("✅ Orchestration terminée proprement")
        
    except Exception as e:
        print(f"\n💥 ERREUR: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 