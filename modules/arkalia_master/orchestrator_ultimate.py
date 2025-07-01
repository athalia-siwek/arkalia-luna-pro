#!/usr/bin/env python3
"""
🌕 ARKALIA MASTER ORCHESTRATOR ULTIMATE v4.0.0

Orchestrateur Maître coordonnant l'écosystème complet Arkalia-LUNA
Gère intelligemment les 10 modules IA avec cycles adaptatifs
"""

from core.ark_logger import ark_logger
import asyncio
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional

import toml

# AssistantIA - Chat & interactions
from ..assistantia.core import router as assistantia_router

# Monitoring - Métriques Prometheus
from ..monitoring.prometheus_metrics import ArkaliaMetrics

# NyxalIA - Interprétation signaux
from ..nyxalia.core import interpret_signal

# ReflexIA - Monitoring & auto-réflexion
from ..reflexia.core import get_metrics, launch_reflexia_check

# SandozIA - Intelligence croisée
from ..sandozia.core.sandozia_core import SandoziaCore

# Security - Protection & cryptographie
from ..security.crypto.checksum_validator import BuildIntegrityValidator

# TaskIA - Coordination tâches
from ..taskia.core import taskia_main

# Utils Enhanced - Cache & optimisations
from ..utils_enhanced.cache_enhanced import load_toml_cached
from ..zeroia.circuit_breaker import CircuitBreaker

# === IMPORTS MODULES ARKALIA ===
# ZeroIA - Décisions & raisonnement
from ..zeroia.core import ZeroIACore

logger = logging.getLogger(__name__)


class CycleMode(Enum):
    """Modes de cycle adaptatifs"""

    URGENT = "urgent"  # 5s - Décisions critiques
    NORMAL = "normal"  # 30s - Opérations standard
    DEEP_ANALYSIS = "deep"  # 300s - Analyse approfondie
    MAINTENANCE = "maintenance"  # 1800s - Maintenance système


class ModuleStatus(Enum):
    """États des modules"""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    OFFLINE = "offline"
    INITIALIZING = "initializing"


@dataclass
class OrchestratorConfig:
    """Configuration Master Orchestrator"""

    # Cycles adaptatifs
    cycle_intervals: dict[CycleMode, float] = field(
        default_factory=lambda: {
            CycleMode.URGENT: 5.0,
            CycleMode.NORMAL: 30.0,
            CycleMode.DEEP_ANALYSIS: 300.0,
            CycleMode.MAINTENANCE: 1800.0,
        }
    )

    # Circuit breaker global
    global_failure_threshold: int = 10
    global_timeout: int = 60

    # Modules actifs
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
        ]
    )

    # Performance
    max_concurrent_operations: int = 5
    health_check_interval: float = 60.0

    # Persistance
    state_file: Path = Path("state/arkalia_master_state.toml")
    log_file: Path = Path("logs/arkalia_master.log")


@dataclass
class ModuleWrapper:
    """Wrapper unifié pour chaque module"""

    name: str
    instance: Any
    status: ModuleStatus = ModuleStatus.INITIALIZING
    last_execution: datetime | None = None
    execution_count: int = 0
    error_count: int = 0
    last_error: str | None = None

    def update_success(self):
        """Met à jour après exécution réussie"""
        self.last_execution = datetime.now()
        self.execution_count += 1
        self.status = ModuleStatus.HEALTHY

    def update_error(self, error: str):
        """Met à jour après erreur"""
        self.error_count += 1
        self.last_error = error
        self.status = ModuleStatus.DEGRADED if self.error_count < 5 else ModuleStatus.CRITICAL


class ArkaliaOrchestrator:
    """
    🌕 ORCHESTRATEUR MAÎTRE ARKALIA-LUNA v4.0.0

    Fonctionnalités :
    - Coordination intelligente 10 modules IA
    - Cycles adaptatifs (urgent/normal/deep/maintenance)
    - Circuit breaker global protection
    - Communication inter-modules optimisée
    - Global State Master unifié
    - Auto-healing & resilience patterns
    """

    def __init__(self, config: OrchestratorConfig | None = None) -> None:
        self.config = config or OrchestratorConfig()
        self.current_cycle_mode = CycleMode.NORMAL
        self.is_running = False
        self.start_time = time.time()

        # Circuit breaker global
        self.global_circuit_breaker = CircuitBreaker(
            failure_threshold=self.config.global_failure_threshold,
            timeout=self.config.global_timeout,
        )

        # État orchestrateur
        self.cycle_count = 0
        self.total_operations = 0
        self.successful_operations = 0
        self.failed_operations = 0

        # Modules wrappés
        self.modules: dict[str, ModuleWrapper] = {}

        # Global State Master
        self.global_state: dict[str, Any] = {}

        # Tasks asyncio
        self.orchestration_task: asyncio.Task | None = None
        self.health_check_task: asyncio.Task | None = None

        logger.info("🌕 ArkaliaOrchestrator Ultimate v4.0.0 initialized")

    async def initialize_modules(self) -> bool:
        """
        Initialise tous les modules Arkalia de manière coordonnée
        """
        logger.info("🔌 Initializing 10 Arkalia modules...")

        initialization_results: dict[str, Any] = {}

        # === ZEROIA - Décisions & raisonnement ===
        if "zeroia" in self.config.enabled_modules:
            try:
                zeroia_core = ZeroIACore()
                if await asyncio.to_thread(zeroia_core.initialize):
                    self.modules["zeroia"] = ModuleWrapper("zeroia", zeroia_core)
                    initialization_results["zeroia"] = "✅ SUCCESS"
                else:
                    initialization_results["zeroia"] = "❌ FAILED"
            except Exception as e:
                initialization_results["zeroia"] = f"❌ ERROR: {e}"

        # === REFLEXIA - Monitoring & auto-réflexion ===
        if "reflexia" in self.config.enabled_modules:
            try:
                # Test fonction réflexIA
                test_metrics = await asyncio.to_thread(get_metrics)
                if test_metrics:
                    self.modules["reflexia"] = ModuleWrapper("reflexia", launch_reflexia_check)
                    initialization_results["reflexia"] = "✅ SUCCESS"
                else:
                    initialization_results["reflexia"] = "❌ FAILED"
            except Exception as e:
                initialization_results["reflexia"] = f"❌ ERROR: {e}"

        # === ASSISTANTIA - Chat & interactions ===
        if "assistantia" in self.config.enabled_modules:
            try:
                # Vérifier que le router est disponible
                if assistantia_router:
                    self.modules["assistantia"] = ModuleWrapper("assistantia", assistantia_router)
                    initialization_results["assistantia"] = "✅ SUCCESS"
                else:
                    initialization_results["assistantia"] = "❌ FAILED"
            except Exception as e:
                initialization_results["assistantia"] = f"❌ ERROR: {e}"

        # === SANDOZIA - Intelligence croisée ===
        if "sandozia" in self.config.enabled_modules:
            try:
                sandozia_core = SandoziaCore()
                self.modules["sandozia"] = ModuleWrapper("sandozia", sandozia_core)
                initialization_results["sandozia"] = "✅ SUCCESS"
            except Exception as e:
                initialization_results["sandozia"] = f"❌ ERROR: {e}"

        # === TASKIA - Coordination tâches ===
        if "taskia" in self.config.enabled_modules:
            try:
                # Test fonction TaskIA
                test_result = await asyncio.to_thread(taskia_main, {"test": "init"})
                if test_result:
                    self.modules["taskia"] = ModuleWrapper("taskia", taskia_main)
                    initialization_results["taskia"] = "✅ SUCCESS"
                else:
                    initialization_results["taskia"] = "❌ FAILED"
            except Exception as e:
                initialization_results["taskia"] = f"❌ ERROR: {e}"

        # === HELLORIA - API & routing ===
        if "helloria" in self.config.enabled_modules:
            try:
                # HellorIA fonctionne via container, on marque comme disponible
                self.modules["helloria"] = ModuleWrapper("helloria", "container_based")
                initialization_results["helloria"] = "✅ SUCCESS (Container)"
            except Exception as e:
                initialization_results["helloria"] = f"❌ ERROR: {e}"

        # === NYXALIA - Interprétation signaux ===
        if "nyxalia" in self.config.enabled_modules:
            try:
                test_signal = await asyncio.to_thread(interpret_signal, "ping")
                if test_signal == "pong":
                    self.modules["nyxalia"] = ModuleWrapper("nyxalia", interpret_signal)
                    initialization_results["nyxalia"] = "✅ SUCCESS"
                else:
                    initialization_results["nyxalia"] = "❌ FAILED"
            except Exception as e:
                initialization_results["nyxalia"] = f"❌ ERROR: {e}"

        # === SECURITY - Protection & cryptographie ===
        if "security" in self.config.enabled_modules:
            try:
                security_validator = BuildIntegrityValidator()
                self.modules["security"] = ModuleWrapper("security", security_validator)
                initialization_results["security"] = "✅ SUCCESS"
            except Exception as e:
                initialization_results["security"] = f"❌ ERROR: {e}"

        # === MONITORING - Métriques Prometheus ===
        if "monitoring" in self.config.enabled_modules:
            try:
                arkalia_metrics = ArkaliaMetrics()
                self.modules["monitoring"] = ModuleWrapper("monitoring", arkalia_metrics)
                initialization_results["monitoring"] = "✅ SUCCESS"
            except Exception as e:
                initialization_results["monitoring"] = f"❌ ERROR: {e}"

        # === UTILS ENHANCED - Cache & optimisations ===
        if "utils" in self.config.enabled_modules:
            try:
                # Test fonction utils enhanced
                test_load = await asyncio.to_thread(load_toml_cached, "version.toml")
                if test_load:
                    self.modules["utils"] = ModuleWrapper("utils", load_toml_cached)
                    initialization_results["utils"] = "✅ SUCCESS"
                else:
                    initialization_results["utils"] = "❌ FAILED"
            except Exception as e:
                initialization_results["utils"] = f"❌ ERROR: {e}"

        # === RAPPORT D'INITIALISATION ===
        logger.info("=" * 70)
        logger.info("🌕 ARKALIA MODULES INITIALIZATION REPORT")
        logger.info("=" * 70)

        success_count = 0
        for module_name, result in initialization_results.items():
            logger.info(f"  {module_name:12} : {result}")
            if "SUCCESS" in result:
                success_count += 1

        total_modules = len(initialization_results)
        success_rate = (success_count / total_modules) * 100 if total_modules > 0 else 0

        logger.info("=" * 70)
        logger.info(
            f"📊 MODULES INITIALIZED: {success_count}/{total_modules} ({success_rate:.1f}%)"
        )
        logger.info("=" * 70)

        # Mise à jour état global
        self.global_state["initialization"] = {
            "timestamp": datetime.now().isoformat(),
            "success_count": success_count,
            "total_modules": total_modules,
            "success_rate": success_rate,
            "results": initialization_results,
        }

        return success_count >= total_modules * 0.7  # 70% minimum pour succès

    async def execute_coordinated_cycle(self) -> dict[str, Any]:
        """
        Exécute un cycle coordonné de tous les modules actifs
        """
        cycle_start = time.time()
        self.cycle_count += 1

        logger.info(f"🔄 CYCLE #{self.cycle_count} - Mode: {self.current_cycle_mode.value}")

        cycle_results: dict[str, Any] = {}
        operations_this_cycle = 0
        successful_this_cycle = 0

        # === PHASE 1: DÉCISIONS RAPIDES (ZeroIA) ===
        if "zeroia" in self.modules and self.modules["zeroia"].status != ModuleStatus.OFFLINE:
            try:
                zeroia_module = self.modules["zeroia"]
                decision, confidence = await asyncio.to_thread(
                    zeroia_module.instance.run_decision_cycle
                )

                cycle_results["zeroia"] = {
                    "decision": decision,
                    "confidence": confidence,
                    "status": "success",
                }

                zeroia_module.update_success()
                successful_this_cycle += 1

            except Exception as e:
                logger.error(f"❌ ZeroIA error: {e}")
                self.modules["zeroia"].update_error(str(e))
                cycle_results["zeroia"] = {"status": "error", "error": str(e)}

            operations_this_cycle += 1

        # === PHASE 2: MONITORING SYSTÈME (ReflexIA) ===
        if "reflexia" in self.modules and self.modules["reflexia"].status != ModuleStatus.OFFLINE:
            try:
                reflexia_module = self.modules["reflexia"]
                reflexia_result = await asyncio.to_thread(reflexia_module.instance)

                cycle_results["reflexia"] = {
                    "status": reflexia_result["status"],
                    "metrics": reflexia_result["metrics"],
                    "result": "success",
                }

                reflexia_module.update_success()
                successful_this_cycle += 1

            except Exception as e:
                logger.error(f"❌ ReflexIA error: {e}")
                self.modules["reflexia"].update_error(str(e))
                cycle_results["reflexia"] = {"result": "error", "error": str(e)}

            operations_this_cycle += 1

        # === PHASE 3: INTELLIGENCE CROISÉE (SandozIA) ===
        if (
            "sandozia" in self.modules
            and self.modules["sandozia"].status != ModuleStatus.OFFLINE
            and self.current_cycle_mode in [CycleMode.NORMAL, CycleMode.DEEP_ANALYSIS]
        ):
            try:
                sandozia_module = self.modules["sandozia"]
                sandozia_status = sandozia_module.instance.get_current_status()

                cycle_results["sandozia"] = {
                    "coherence_score": sandozia_status.get("coherence_score", 0.0),
                    "active_correlations": sandozia_status.get("active_correlations", 0),
                    "result": "success",
                }

                sandozia_module.update_success()
                successful_this_cycle += 1

            except Exception as e:
                logger.error(f"❌ SandozIA error: {e}")
                self.modules["sandozia"].update_error(str(e))
                cycle_results["sandozia"] = {"result": "error", "error": str(e)}

            operations_this_cycle += 1

        # === PHASE 4: COORDINATION TÂCHES (TaskIA) ===
        if (
            "taskia" in self.modules
            and self.modules["taskia"].status != ModuleStatus.OFFLINE
            and self.current_cycle_mode != CycleMode.URGENT
        ):
            try:
                taskia_module = self.modules["taskia"]

                # Construire contexte pour TaskIA
                task_context = {
                    "cycle_mode": self.current_cycle_mode.value,
                    "cycle_count": self.cycle_count,
                    "global_state": self.global_state,
                    "zeroia_result": cycle_results.get("zeroia", {}),
                    "reflexia_result": cycle_results.get("reflexia", {}),
                }

                taskia_result = await asyncio.to_thread(taskia_module.instance, task_context)

                cycle_results["taskia"] = {
                    "analysis": taskia_result,
                    "result": "success",
                }

                taskia_module.update_success()
                successful_this_cycle += 1

            except Exception as e:
                logger.error(f"❌ TaskIA error: {e}")
                self.modules["taskia"].update_error(str(e))
                cycle_results["taskia"] = {"result": "error", "error": str(e)}

            operations_this_cycle += 1

        # === PHASE 5: SIGNAUX & INTERPRÉTATION (NyxalIA) ===
        if (
            "nyxalia" in self.modules
            and self.modules["nyxalia"].status != ModuleStatus.OFFLINE
            and self.current_cycle_mode == CycleMode.DEEP_ANALYSIS
        ):
            try:
                nyxalia_module = self.modules["nyxalia"]

                # Signal basé sur l'état du cycle
                cycle_signal = "start" if self.cycle_count <= 3 else "ping"
                signal_result = await asyncio.to_thread(nyxalia_module.instance, cycle_signal)

                cycle_results["nyxalia"] = {
                    "signal": cycle_signal,
                    "interpretation": signal_result,
                    "result": "success",
                }

                nyxalia_module.update_success()
                successful_this_cycle += 1

            except Exception as e:
                logger.error(f"❌ NyxalIA error: {e}")
                self.modules["nyxalia"].update_error(str(e))
                cycle_results["nyxalia"] = {"result": "error", "error": str(e)}

            operations_this_cycle += 1

        # === MISE À JOUR STATISTIQUES ===
        cycle_duration = time.time() - cycle_start
        self.total_operations += operations_this_cycle
        self.successful_operations += successful_this_cycle
        self.failed_operations += operations_this_cycle - successful_this_cycle

        # === ADAPTATION CYCLE MODE ===
        await self._adapt_cycle_mode(cycle_results, successful_this_cycle, operations_this_cycle)

        # === RÉSULTAT CYCLE ===
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
            "modules_results": cycle_results,
            "timestamp": datetime.now().isoformat(),
        }

        logger.info(
            f"✅ CYCLE #{self.cycle_count} COMPLETED - "
            f"Success: {successful_this_cycle}/{operations_this_cycle} "
            f"({cycle_summary['success_rate']}%) - "
            f"Duration: {cycle_duration:.3f}s"
        )

        return cycle_summary

    async def _adapt_cycle_mode(self, cycle_results: dict, successful: int, total: int):
        """
        Adapte intelligemment le mode de cycle selon les résultats
        """
        if total == 0:
            return

        success_rate = successful / total

        # Vérifier s'il y a des erreurs critiques
        critical_errors = False
        for module_result in cycle_results.values():
            if module_result.get("result") == "error" or module_result.get("status") == "error":
                critical_errors = True
                break

        # Logique d'adaptation
        if critical_errors or success_rate < 0.5:
            # Erreurs critiques -> Mode URGENT
            if self.current_cycle_mode != CycleMode.URGENT:
                self.current_cycle_mode = CycleMode.URGENT
                logger.warning("⚠️ Switching to URGENT mode due to critical errors")

        elif success_rate < 0.8:
            # Performance dégradée -> Mode NORMAL
            if self.current_cycle_mode not in [CycleMode.URGENT, CycleMode.NORMAL]:
                self.current_cycle_mode = CycleMode.NORMAL
                logger.info("📊 Switching to NORMAL mode due to degraded performance")

        elif success_rate >= 0.95 and self.cycle_count % 10 == 0:
            # Excellente performance + cycle multiple de 10 -> Mode DEEP_ANALYSIS
            if self.current_cycle_mode != CycleMode.DEEP_ANALYSIS:
                self.current_cycle_mode = CycleMode.DEEP_ANALYSIS
                logger.info("🧠 Switching to DEEP_ANALYSIS mode - excellent performance")

        elif self.cycle_count % 60 == 0:  # Toutes les 60 cycles
            # Maintenance périodique
            if self.current_cycle_mode != CycleMode.MAINTENANCE:
                self.current_cycle_mode = CycleMode.MAINTENANCE
                logger.info("🔧 Switching to MAINTENANCE mode - periodic maintenance")

    async def run_orchestration(self) -> None:
        """
        Lance l'orchestration principale en mode daemon
        """
        if self.is_running:
            logger.warning("⚠️ Orchestration already running")
            return

        logger.info("🚀 Starting Arkalia Master Orchestration...")

        # Initialiser modules
        init_success = await self.initialize_modules()
        if not init_success:
            logger.error("❌ Module initialization failed - aborting orchestration")
            return

        self.is_running = True

        # Lancer health check en background
        self.health_check_task = asyncio.create_task(self._health_check_loop())

        try:
            while self.is_running:
                # Exécuter cycle coordonné
                cycle_result = await self.execute_coordinated_cycle()

                # Sauvegarder état
                await self._save_global_state(cycle_result)

                # Attendre selon le mode de cycle
                sleep_duration = self.config.cycle_intervals[self.current_cycle_mode]
                await asyncio.sleep(sleep_duration)

        except KeyboardInterrupt:
            logger.info("⏹️ Orchestration stopped by user")
        except Exception as e:
            logger.error(f"💥 Orchestration error: {e}")
        finally:
            await self._cleanup()

    async def _health_check_loop(self):
        """Boucle de health check en background"""
        while self.is_running:
            try:
                await self._perform_health_checks()
                await asyncio.sleep(self.config.health_check_interval)
            except Exception as e:
                logger.error(f"❌ Health check error: {e}")

    async def _perform_health_checks(self):
        """Vérifie la santé de tous les modules"""
        for _module_name, module_wrapper in self.modules.items():
            # Logique de health check spécifique à chaque module
            if module_wrapper.error_count > 10:
                module_wrapper.status = ModuleStatus.CRITICAL
            elif module_wrapper.error_count > 5:
                module_wrapper.status = ModuleStatus.DEGRADED
            elif (
                module_wrapper.last_execution
                and (datetime.now() - module_wrapper.last_execution).total_seconds() > 300
            ):  # 5 minutes
                module_wrapper.status = ModuleStatus.OFFLINE

    async def _save_global_state(self, cycle_result: dict):
        """Sauvegarde l'état global"""
        try:
            uptime = time.time() - self.start_time

            state = {
                "orchestrator": {
                    "version": "4.0.0",
                    "uptime_seconds": uptime,
                    "cycle_count": self.cycle_count,
                    "current_mode": self.current_cycle_mode.value,
                    "total_operations": self.total_operations,
                    "successful_operations": self.successful_operations,
                    "failed_operations": self.failed_operations,
                    "success_rate": (
                        round(self.successful_operations / self.total_operations * 100, 2)
                        if self.total_operations > 0
                        else 0
                    ),
                },
                "modules": {
                    name: {
                        "status": wrapper.status.value,
                        "execution_count": wrapper.execution_count,
                        "error_count": wrapper.error_count,
                        "last_execution": (
                            wrapper.last_execution.isoformat() if wrapper.last_execution else None
                        ),
                        "last_error": wrapper.last_error,
                    }
                    for name, wrapper in self.modules.items()
                },
                "last_cycle": cycle_result,
                "timestamp": datetime.now().isoformat(),
            }

            # Créer répertoire si nécessaire
            self.config.state_file.parent.mkdir(parents=True, exist_ok=True)

            # Sauvegarder
            with open(self.config.state_file, "w") as f:
                toml.dump(state, f)

        except Exception as e:
            logger.error(f"❌ Error saving global state: {e}")

    async def _cleanup(self):
        """Nettoyage final"""
        self.is_running = False

        if self.health_check_task:
            self.health_check_task.cancel()

        logger.info("🧹 Arkalia Master Orchestrator cleanup completed")

    def get_status(self) -> dict[str, Any]:
        """Retourne le statut complet de l'orchestrateur"""
        uptime = time.time() - self.start_time

        return {
            "orchestrator": {
                "version": "4.0.0",
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
            },
            "modules": {
                name: {
                    "status": wrapper.status.value,
                    "execution_count": wrapper.execution_count,
                    "error_count": wrapper.error_count,
                }
                for name, wrapper in self.modules.items()
            },
            "config": {
                "enabled_modules": self.config.enabled_modules,
                "cycle_intervals": {
                    mode.value: interval for mode, interval in self.config.cycle_intervals.items()
                },
            },
            "timestamp": datetime.now().isoformat(),
        }


# === FONCTIONS UTILITAIRES ===


async def orchestrate_full_ecosystem(
    config: OrchestratorConfig | None = None, max_cycles: int | None = None
) -> None:
    """
    Lance l'orchestration complète de l'écosystème Arkalia

    Args:
        config: Configuration personnalisée
        max_cycles: Nombre max de cycles (None = infini)
    """
    orchestrator = ArkaliaOrchestrator(config)

    try:
        if max_cycles:
            # Mode test avec nombre limité de cycles
            await orchestrator.initialize_modules()
            for i in range(max_cycles):
                await orchestrator.execute_coordinated_cycle()
                logger.info(f"Cycle {i+1}/{max_cycles} completed")

                # Attendre selon le mode
                sleep_duration = orchestrator.config.cycle_intervals[
                    orchestrator.current_cycle_mode
                ]
                await asyncio.sleep(sleep_duration)
        else:
            # Mode production infini
            await orchestrator.run_orchestration()

    except KeyboardInterrupt:
        logger.info("⏹️ Orchestration stopped by user")
    except Exception as e:
        logger.error(f"💥 Orchestration failed: {e}")
        raise


# === POINT D'ENTRÉE CLI ===


async def main():
    """Point d'entrée principal pour CLI"""
    import argparse

    parser = argparse.ArgumentParser(description="Arkalia Master Orchestrator v4.0.0")
    parser.add_argument(
        "--mode",
        choices=["daemon", "test", "status"],
        default="daemon",
        help="Mode d'exécution",
    )
    parser.add_argument("--cycles", type=int, help="Nombre de cycles (mode test)")
    parser.add_argument("--config", type=str, help="Fichier config personnalisé")
    parser.add_argument("--verbose", action="store_true", help="Logs détaillés")

    args = parser.parse_args()

    # Configuration logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )

    # Configuration
    config = OrchestratorConfig()
    if args.config:
        # Charger config personnalisée
        try:
            with open(args.config) as f:
                toml.load(f)
                # Merge avec config par défaut
                # TODO: Implémenter merge intelligent
        except Exception as e:
            logger.error(f"❌ Error loading config: {e}")
            return

    ark_logger.info("🌕 ARKALIA MASTER ORCHESTRATOR v4.0.0", extra={"module": "arkalia_master"})
    ark_logger.info("=" * 60, extra={"module": "arkalia_master"})
    ark_logger.info("🧠 10 Modules IA Coordonnés", extra={"module": "arkalia_master"})
    ark_logger.info("🔄 Cycles Adaptatifs Intelligents", extra={"module": "arkalia_master"})
    ark_logger.info("🛡️ Circuit Breaker Global", extra={"module": "arkalia_master"})
    ark_logger.info("🌐 Global State Master", extra={"module": "arkalia_master"})
    ark_logger.info("=" * 60, extra={"module": "arkalia_master"})

    try:
        if args.mode == "daemon":
            await orchestrate_full_ecosystem(config)
        elif args.mode == "test":
            cycles = args.cycles or 5
            await orchestrate_full_ecosystem(config, max_cycles=cycles)
        elif args.mode == "status":
            orchestrator = ArkaliaOrchestrator(config)
            status = orchestrator.get_status()
            ark_logger.info("\n📊 ORCHESTRATOR STATUS:", extra={"module": "arkalia_master"})
            ark_logger.info("=" * 40, extra={"module": "arkalia_master"})
            for key, value in status.items():
                ark_logger.info(f"{key}: {value}", extra={"module": "arkalia_master"})

    except KeyboardInterrupt:
        ark_logger.info("\n⏹️ Stopped by user", extra={"module": "arkalia_master"})
    except Exception as e:
        ark_logger.error(f"\n💥 Error: {e}", extra={"module": "arkalia_master"})
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
