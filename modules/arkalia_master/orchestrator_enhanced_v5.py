#!/usr/bin/env python3
"""
🌟 ARKALIA MASTER ORCHESTRATOR ENHANCED v5.0.0

Version Enhanced avec les composants manquants intégrés :
- Error Recovery System pour récupération automatique
- Cognitive Reactor pour réactions cognitives
- Vault Manager pour sécurité renforcée
- Chronalia pour gestion temporelle intelligente
- CrossModule Validator pour validation croisée
"""

import asyncio
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from modules.zeroia.circuit_breaker import CircuitBreaker

# === IMPORTS MODULES ARKALIA STANDARDS ===
from modules.zeroia.core import ZeroIACore

# === IMPORTS MODULES ENHANCED NOUVEAUX ===
try:
    from modules.zeroia.error_recovery_system import ErrorRecoverySystem

    ERROR_RECOVERY_AVAILABLE = True
except ImportError:
    ERROR_RECOVERY_AVAILABLE = False

try:
    from modules.sandozia.core.cognitive_reactor import CognitiveReactor

    COGNITIVE_REACTOR_AVAILABLE = True
except ImportError:
    COGNITIVE_REACTOR_AVAILABLE = False

try:
    from modules.security.crypto.vault_manager import ArkaliaVault

    VAULT_MANAGER_AVAILABLE = True
except ImportError:
    VAULT_MANAGER_AVAILABLE = False

try:
    from modules.sandozia.core.chronalia import Chronalia

    CHRONALIA_AVAILABLE = True
except ImportError:
    CHRONALIA_AVAILABLE = False

try:
    from modules.sandozia.validators.crossmodule import CrossModuleValidator

    CROSSMODULE_AVAILABLE = True
except ImportError:
    CROSSMODULE_AVAILABLE = False

logger = logging.getLogger(__name__)


class CycleMode(Enum):
    """Modes de cycle adaptatifs enhanced"""

    URGENT = "urgent"  # 5s - Décisions critiques
    NORMAL = "normal"  # 30s - Opérations standard
    DEEP_ANALYSIS = "deep"  # 300s - Analyse approfondie
    MAINTENANCE = "maintenance"  # 1800s - Maintenance système
    COGNITIVE_BOOST = "cognitive"  # 60s - Mode réacteur cognitif


class ModuleStatus(Enum):
    """États des modules enhanced"""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    OFFLINE = "offline"
    INITIALIZING = "initializing"
    RECOVERING = "recovering"  # Nouveau: en cours de récupération
    COGNITIVE = "cognitive"  # Nouveau: mode cognitif actif


@dataclass
class OrchestratorEnhancedConfig:
    """Configuration Master Orchestrator Enhanced"""

    # Cycles adaptatifs enhanced
    cycle_intervals: dict[CycleMode, float] = field(
        default_factory=lambda: {
            CycleMode.URGENT: 5.0,
            CycleMode.NORMAL: 30.0,
            CycleMode.DEEP_ANALYSIS: 300.0,
            CycleMode.MAINTENANCE: 1800.0,
            CycleMode.COGNITIVE_BOOST: 60.0,  # Nouveau mode
        }
    )

    # Circuit breaker global
    global_failure_threshold: int = 10
    global_recovery_timeout: int = 60

    # Modules actifs enhanced
    enabled_modules: list[str] = field(
        default_factory=lambda: [
            "zeroia",
            "reflexia",
            "assistantia",
            "sandozia",
            "taskia",
            "helloria",
            "nyxalia",
            "security",
            "monitoring",
            "utils",
            # Nouveaux modules enhanced
            "error_recovery",
            "cognitive_reactor",
            "vault_manager",
            "chronalia",
            "crossmodule_validator",
        ]
    )

    # Enhanced features
    cognitive_mode_enabled: bool = True
    auto_recovery_enabled: bool = True
    temporal_analysis_enabled: bool = True
    cross_validation_enabled: bool = True

    # Performance
    max_concurrent_operations: int = 8  # Augmenté pour enhanced
    health_check_interval: float = 45.0  # Réduit pour plus de réactivité

    # Persistance
    state_file: Path = Path("state/arkalia_master_enhanced_state.toml")
    log_file: Path = Path("logs/arkalia_master_enhanced.log")


@dataclass
class ModuleWrapperEnhanced:
    """Wrapper unifié enhanced pour chaque module"""

    name: str
    instance: Any
    status: ModuleStatus = ModuleStatus.INITIALIZING
    last_execution: datetime | None = None
    execution_count: int = 0
    error_count: int = 0
    last_error: str | None = None
    recovery_attempts: int = 0  # Nouveau: tentatives de récupération
    cognitive_score: float = 0.0  # Nouveau: score cognitif

    def update_success(self):
        """Met à jour après exécution réussie"""
        self.last_execution = datetime.now()
        self.execution_count += 1
        self.status = ModuleStatus.HEALTHY
        self.cognitive_score = min(self.cognitive_score + 0.1, 1.0)

    def update_error(self, error: str):
        """Met à jour après erreur avec récupération"""
        self.error_count += 1
        self.last_error = error
        self.cognitive_score = max(self.cognitive_score - 0.2, 0.0)

        if self.error_count < 3:
            self.status = ModuleStatus.DEGRADED
        elif self.error_count < 8:
            self.status = ModuleStatus.CRITICAL
        else:
            self.status = ModuleStatus.RECOVERING

    def start_recovery(self):
        """Démarre la récupération du module"""
        self.recovery_attempts += 1
        self.status = ModuleStatus.RECOVERING


class ArkaliaOrchestratorEnhanced:
    """
    🌟 ORCHESTRATEUR MAÎTRE ARKALIA-LUNA ENHANCED v5.0.0

    Nouvelles fonctionnalités :
    - Error Recovery System intégré
    - Cognitive Reactor pour réactions automatiques
    - Vault Manager pour sécurité renforcée
    - Chronalia pour gestion temporelle
    - CrossModule Validator pour validation croisée
    - Mode COGNITIVE_BOOST
    """

    def __init__(self, config: OrchestratorEnhancedConfig | None = None):
        self.config = config or OrchestratorEnhancedConfig()
        self.current_cycle_mode = CycleMode.NORMAL
        self.is_running = False
        self.start_time = time.time()

        # Circuit breaker global
        self.global_circuit_breaker = CircuitBreaker(
            failure_threshold=self.config.global_failure_threshold,
            recovery_timeout=self.config.global_recovery_timeout,
        )

        # État orchestrateur enhanced
        self.cycle_count = 0
        self.total_operations = 0
        self.successful_operations = 0
        self.failed_operations = 0
        self.cognitive_events = 0  # Nouveau: événements cognitifs
        self.recovery_events = 0  # Nouveau: récupérations

        # Modules wrappés enhanced
        self.modules: dict[str, ModuleWrapperEnhanced] = {}

        # Global State Master enhanced
        self.global_state: dict[str, Any] = {}
        self.cognitive_state: dict[str, Any] = {}  # Nouveau: état cognitif

        # Tasks asyncio
        self.orchestration_task: asyncio.Task | None = None
        self.health_check_task: asyncio.Task | None = None
        self.cognitive_task: asyncio.Task | None = None  # Nouveau: task cognitive

        # Enhanced components
        self.error_recovery_system: Any | None = None
        self.cognitive_reactor: Any | None = None
        self.vault_manager: Any | None = None
        self.chronalia: Any | None = None
        self.crossmodule_validator: Any | None = None

        logger.info("🌟 ArkaliaOrchestrator Enhanced v5.0.0 initialized")

    async def initialize_modules_enhanced(self) -> bool:
        """
        Initialise tous les modules Enhanced de manière coordonnée
        """
        logger.info("🔌 Initializing Enhanced modules (15 total)...")

        initialization_results = {}

        # === MODULES STANDARDS (comme avant) ===

        # ZeroIA
        if "zeroia" in self.config.enabled_modules:
            try:
                zeroia_core = ZeroIACore()
                if await asyncio.to_thread(zeroia_core.initialize):
                    self.modules["zeroia"] = ModuleWrapperEnhanced("zeroia", zeroia_core)
                    initialization_results["zeroia"] = "✅ SUCCESS"
                else:
                    initialization_results["zeroia"] = "❌ FAILED"
            except Exception as e:
                initialization_results["zeroia"] = f"❌ ERROR: {e}"

        # === NOUVEAUX MODULES ENHANCED ===

        # Error Recovery System
        if (
            "error_recovery" in self.config.enabled_modules
            and ERROR_RECOVERY_AVAILABLE
            and self.config.auto_recovery_enabled
        ):
            try:
                self.error_recovery_system = ErrorRecoverySystem()
                self.modules["error_recovery"] = ModuleWrapperEnhanced(
                    "error_recovery", self.error_recovery_system
                )
                initialization_results["error_recovery"] = "✅ SUCCESS (Enhanced)"
                logger.info("🛡️ Error Recovery System activé")
            except Exception as e:
                initialization_results["error_recovery"] = f"❌ ERROR: {e}"

        # Cognitive Reactor
        if (
            "cognitive_reactor" in self.config.enabled_modules
            and COGNITIVE_REACTOR_AVAILABLE
            and self.config.cognitive_mode_enabled
        ):
            try:
                self.cognitive_reactor = CognitiveReactor()
                self.modules["cognitive_reactor"] = ModuleWrapperEnhanced(
                    "cognitive_reactor", self.cognitive_reactor
                )
                initialization_results["cognitive_reactor"] = "✅ SUCCESS (Enhanced)"
                logger.info("🧠 Cognitive Reactor activé")
            except Exception as e:
                initialization_results["cognitive_reactor"] = f"❌ ERROR: {e}"

        # Vault Manager
        if "vault_manager" in self.config.enabled_modules and VAULT_MANAGER_AVAILABLE:
            try:
                self.vault_manager = ArkaliaVault()
                self.modules["vault_manager"] = ModuleWrapperEnhanced(
                    "vault_manager", self.vault_manager
                )
                initialization_results["vault_manager"] = "✅ SUCCESS (Enhanced)"
                logger.info("🔐 Vault Manager activé")
            except Exception as e:
                initialization_results["vault_manager"] = f"❌ ERROR: {e}"

        # Chronalia
        if (
            "chronalia" in self.config.enabled_modules
            and CHRONALIA_AVAILABLE
            and self.config.temporal_analysis_enabled
        ):
            try:
                self.chronalia = Chronalia()
                self.modules["chronalia"] = ModuleWrapperEnhanced("chronalia", self.chronalia)
                initialization_results["chronalia"] = "✅ SUCCESS (Enhanced)"
                logger.info("⏰ Chronalia activé")
            except Exception as e:
                initialization_results["chronalia"] = f"❌ ERROR: {e}"

        # CrossModule Validator
        if (
            "crossmodule_validator" in self.config.enabled_modules
            and CROSSMODULE_AVAILABLE
            and self.config.cross_validation_enabled
        ):
            try:
                self.crossmodule_validator = CrossModuleValidator()
                self.modules["crossmodule_validator"] = ModuleWrapperEnhanced(
                    "crossmodule_validator", self.crossmodule_validator
                )
                initialization_results["crossmodule_validator"] = "✅ SUCCESS (Enhanced)"
                logger.info("✅ CrossModule Validator activé")
            except Exception as e:
                initialization_results["crossmodule_validator"] = f"❌ ERROR: {e}"

        # === LOG RÉSULTATS ===
        enhanced_count = sum(1 for r in initialization_results.values() if "Enhanced" in r)
        total_success = sum(1 for r in initialization_results.values() if "SUCCESS" in r)

        logger.info(f"🌟 Enhanced modules: {enhanced_count}")
        logger.info(f"✅ Total success: {total_success}/{len(initialization_results)}")

        return total_success > 0

    async def execute_enhanced_cycle(self) -> dict[str, Any]:
        """
        Exécute un cycle coordonné Enhanced avec les nouveaux composants
        """
        cycle_start = time.time()
        self.cycle_count += 1

        logger.info(
            f"🌟 ENHANCED CYCLE #{self.cycle_count} - Mode: {self.current_cycle_mode.value}"
        )

        cycle_results = {}
        operations_this_cycle = 0
        successful_this_cycle = 0

        # === PHASE 0: COGNITIVE REACTOR (si mode cognitif) ===
        if self.cognitive_reactor and self.current_cycle_mode == CycleMode.COGNITIVE_BOOST:
            try:
                cognitive_result = await asyncio.to_thread(
                    self.cognitive_reactor.process_cognitive_cycle, self.global_state
                )

                cycle_results["cognitive_reactor"] = {
                    "cognitive_events": cognitive_result.get("events", 0),
                    "reactions_triggered": cognitive_result.get("reactions", 0),
                    "status": "success",
                }

                self.modules["cognitive_reactor"].update_success()
                self.cognitive_events += cognitive_result.get("events", 0)
                successful_this_cycle += 1

                logger.info(f"🧠 Cognitive events: {cognitive_result.get('events', 0)}")

            except Exception as e:
                logger.error(f"❌ Cognitive Reactor error: {e}")
                self.modules["cognitive_reactor"].update_error(str(e))
                cycle_results["cognitive_reactor"] = {
                    "status": "error",
                    "error": str(e),
                }

            operations_this_cycle += 1

        # === PHASE 1: ERROR RECOVERY CHECK ===
        if self.error_recovery_system and self.config.auto_recovery_enabled:
            try:
                # Vérifier si des modules ont besoin de récupération
                modules_to_recover = [
                    name
                    for name, wrapper in self.modules.items()
                    if wrapper.status == ModuleStatus.CRITICAL
                ]

                if modules_to_recover:
                    recovery_result = await asyncio.to_thread(
                        self.error_recovery_system.attempt_recovery, modules_to_recover
                    )

                    cycle_results["error_recovery"] = {
                        "modules_recovered": recovery_result.get("recovered", []),
                        "recovery_success": recovery_result.get("success", False),
                        "status": "success",
                    }

                    self.modules["error_recovery"].update_success()
                    self.recovery_events += len(recovery_result.get("recovered", []))
                    successful_this_cycle += 1

                    # Marquer modules récupérés
                    for module_name in recovery_result.get("recovered", []):
                        if module_name in self.modules:
                            self.modules[module_name].status = ModuleStatus.HEALTHY
                            self.modules[module_name].error_count = 0

                    logger.info(f"🛡️ Modules recovered: {len(recovery_result.get('recovered', []))}")

            except Exception as e:
                logger.error(f"❌ Error Recovery error: {e}")
                cycle_results["error_recovery"] = {"status": "error", "error": str(e)}

            operations_this_cycle += 1

        # === PHASE 2: TEMPORAL ANALYSIS (Chronalia) ===
        if (
            self.chronalia
            and self.config.temporal_analysis_enabled
            and self.current_cycle_mode in [CycleMode.DEEP_ANALYSIS, CycleMode.COGNITIVE_BOOST]
        ):
            try:
                temporal_result = await asyncio.to_thread(
                    self.chronalia.analyze_temporal_patterns, self.global_state
                )

                cycle_results["chronalia"] = {
                    "patterns_detected": temporal_result.get("patterns", 0),
                    "temporal_score": temporal_result.get("score", 0.0),
                    "status": "success",
                }

                self.modules["chronalia"].update_success()
                successful_this_cycle += 1

                logger.info(f"⏰ Temporal patterns: {temporal_result.get('patterns', 0)}")

            except Exception as e:
                logger.error(f"❌ Chronalia error: {e}")
                self.modules["chronalia"].update_error(str(e))
                cycle_results["chronalia"] = {"status": "error", "error": str(e)}

            operations_this_cycle += 1

        # === PHASE 3: CROSS-MODULE VALIDATION ===
        if self.crossmodule_validator and self.config.cross_validation_enabled:
            try:
                validation_result = await asyncio.to_thread(
                    self.crossmodule_validator.validate_cross_modules,
                    list(self.modules.keys()),
                )

                cycle_results["crossmodule_validator"] = {
                    "validation_score": validation_result.get("score", 0.0),
                    "issues_found": validation_result.get("issues", 0),
                    "status": "success",
                }

                self.modules["crossmodule_validator"].update_success()
                successful_this_cycle += 1

                logger.info(f"✅ Cross-validation score: {validation_result.get('score', 0.0):.2f}")

            except Exception as e:
                logger.error(f"❌ CrossModule Validator error: {e}")
                self.modules["crossmodule_validator"].update_error(str(e))
                cycle_results["crossmodule_validator"] = {
                    "status": "error",
                    "error": str(e),
                }

            operations_this_cycle += 1

        # === PHASE 4: VAULT SECURITY CHECK ===
        if self.vault_manager:
            try:
                security_result = await asyncio.to_thread(self.vault_manager.security_health_check)

                cycle_results["vault_manager"] = {
                    "security_score": security_result.get("score", 0.0),
                    "secrets_managed": security_result.get("secrets_count", 0),
                    "status": "success",
                }

                self.modules["vault_manager"].update_success()
                successful_this_cycle += 1

                logger.info(f"🔐 Security score: {security_result.get('score', 0.0):.2f}")

            except Exception as e:
                logger.error(f"❌ Vault Manager error: {e}")
                self.modules["vault_manager"].update_error(str(e))
                cycle_results["vault_manager"] = {"status": "error", "error": str(e)}

            operations_this_cycle += 1

        # === MISE À JOUR STATISTIQUES ENHANCED ===
        cycle_duration = time.time() - cycle_start
        self.total_operations += operations_this_cycle
        self.successful_operations += successful_this_cycle
        self.failed_operations += operations_this_cycle - successful_this_cycle

        # === ADAPTATION CYCLE MODE ENHANCED ===
        await self._adapt_cycle_mode_enhanced(
            cycle_results, successful_this_cycle, operations_this_cycle
        )

        # === RÉSULTAT CYCLE ENHANCED ===
        cycle_summary = {
            "cycle_number": self.cycle_count,
            "cycle_mode": self.current_cycle_mode.value,
            "duration_seconds": round(cycle_duration, 3),
            "operations_executed": operations_this_cycle,
            "operations_successful": successful_this_cycle,
            "success_rate": (
                round(successful_this_cycle / operations_this_cycle * 100, 1)
                if operations_this_cycle > 0
                else 0
            ),
            "enhanced_features": {
                "cognitive_events": self.cognitive_events,
                "recovery_events": self.recovery_events,
                "enhanced_modules_active": len(
                    [m for m in self.modules.values() if "enhanced" in m.name.lower()]
                ),
            },
            "modules_results": cycle_results,
            "timestamp": datetime.now().isoformat(),
        }

        logger.info(
            f"✅ ENHANCED CYCLE #{self.cycle_count} COMPLETED - "
            f"Success: {successful_this_cycle}/{operations_this_cycle} "
            f"({cycle_summary['success_rate']}%) - "
            f"Duration: {cycle_duration:.3f}s - "
            f"Cognitive: {self.cognitive_events}"
        )

        return cycle_summary

    async def _adapt_cycle_mode_enhanced(self, cycle_results: dict, successful: int, total: int):
        """
        Adapte intelligemment le mode de cycle Enhanced
        """
        if total == 0:
            return

        success_rate = successful / total

        # Vérifier événements cognitifs
        cognitive_activity = any("cognitive" in str(result) for result in cycle_results.values())

        # Vérifier erreurs critiques
        critical_errors = any(result.get("status") == "error" for result in cycle_results.values())

        # Logique d'adaptation Enhanced
        if critical_errors or success_rate < 0.5:
            # Erreurs critiques -> Mode URGENT avec recovery
            if self.current_cycle_mode != CycleMode.URGENT:
                self.current_cycle_mode = CycleMode.URGENT
                logger.warning("⚠️ Switching to URGENT mode due to critical errors")

        elif cognitive_activity and success_rate > 0.8:
            # Haute activité cognitive + bon succès -> Mode COGNITIVE_BOOST
            if self.current_cycle_mode != CycleMode.COGNITIVE_BOOST:
                self.current_cycle_mode = CycleMode.COGNITIVE_BOOST
                logger.info("🧠 Switching to COGNITIVE_BOOST mode")

        elif success_rate > 0.9 and self.cycle_count % 10 == 0:
            # Excellent succès -> Mode DEEP_ANALYSIS périodique
            if self.current_cycle_mode != CycleMode.DEEP_ANALYSIS:
                self.current_cycle_mode = CycleMode.DEEP_ANALYSIS
                logger.info("🔍 Switching to DEEP_ANALYSIS mode")

        elif success_rate > 0.7:
            # Bon succès -> Mode NORMAL
            if self.current_cycle_mode != CycleMode.NORMAL:
                self.current_cycle_mode = CycleMode.NORMAL
                logger.info("🔄 Returning to NORMAL mode")

    def get_enhanced_status(self) -> dict[str, Any]:
        """Retourne le statut complet Enhanced"""
        uptime = time.time() - self.start_time

        return {
            "orchestrator": {
                "version": "5.0.0 Enhanced",
                "is_running": self.is_running,
                "uptime_seconds": uptime,
                "cycle_count": self.cycle_count,
                "current_mode": self.current_cycle_mode.value,
                "total_operations": self.total_operations,
                "success_rate": (
                    round(self.successful_operations / self.total_operations * 100, 2)
                    if self.total_operations > 0
                    else 0
                ),
                "enhanced_stats": {
                    "cognitive_events": self.cognitive_events,
                    "recovery_events": self.recovery_events,
                    "enhanced_modules_count": len(
                        [m for m in self.modules.values() if hasattr(m, "cognitive_score")]
                    ),
                },
            },
            "modules": {
                name: {
                    "status": wrapper.status.value,
                    "execution_count": wrapper.execution_count,
                    "error_count": wrapper.error_count,
                    "cognitive_score": wrapper.cognitive_score,
                    "recovery_attempts": wrapper.recovery_attempts,
                }
                for name, wrapper in self.modules.items()
            },
            "enhanced_features": {
                "error_recovery_active": self.error_recovery_system is not None,
                "cognitive_reactor_active": self.cognitive_reactor is not None,
                "vault_manager_active": self.vault_manager is not None,
                "chronalia_active": self.chronalia is not None,
                "crossmodule_validator_active": self.crossmodule_validator is not None,
            },
            "timestamp": datetime.now().isoformat(),
        }


# === FONCTION UTILITAIRE ENHANCED ===


async def orchestrate_enhanced_ecosystem(
    config: OrchestratorEnhancedConfig | None = None,
    max_cycles: int | None = None,
) -> None:
    """
    Lance l'orchestration Enhanced complète
    """
    orchestrator = ArkaliaOrchestratorEnhanced(config)

    try:
        await orchestrator.initialize_modules_enhanced()

        if max_cycles:
            for i in range(max_cycles):
                await orchestrator.execute_enhanced_cycle()
                logger.info(f"Enhanced Cycle {i+1}/{max_cycles} completed")

                sleep_duration = orchestrator.config.cycle_intervals[
                    orchestrator.current_cycle_mode
                ]
                await asyncio.sleep(sleep_duration)
        else:
            # Mode production infini enhanced
            logger.info("🌟 Starting Enhanced orchestration...")
            orchestrator.is_running = True

            while orchestrator.is_running:
                await orchestrator.execute_enhanced_cycle()

                sleep_duration = orchestrator.config.cycle_intervals[
                    orchestrator.current_cycle_mode
                ]
                await asyncio.sleep(sleep_duration)

    except KeyboardInterrupt:
        logger.info("⏹️ Enhanced orchestration stopped by user")
    except Exception as e:
        logger.error(f"💥 Enhanced orchestration failed: {e}")
        raise


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Arkalia Master Orchestrator Enhanced v5.0.0")
    parser.add_argument("--cycles", type=int, help="Nombre de cycles (mode test)")
    parser.add_argument("--verbose", action="store_true", help="Logs détaillés")

    args = parser.parse_args()

    # Configuration logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )

    print("🌟 ARKALIA MASTER ORCHESTRATOR ENHANCED v5.0.0")
    print("=" * 70)
    print("🧠 15 Modules IA Coordonnés (Enhanced)")
    print("🛡️ Error Recovery System intégré")
    print("🧠 Cognitive Reactor pour réactions automatiques")
    print("🔐 Vault Manager pour sécurité renforcée")
    print("⏰ Chronalia pour gestion temporelle")
    print("✅ CrossModule Validator pour validation croisée")
    print("=" * 70)

    try:
        cycles = args.cycles or None
        asyncio.run(orchestrate_enhanced_ecosystem(max_cycles=cycles))
    except KeyboardInterrupt:
        print("\n⏹️ Stopped by user")
    except Exception as e:
        print(f"\n💥 Error: {e}")
        import traceback

        traceback.print_exc()
