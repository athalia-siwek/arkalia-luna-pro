#!/usr/bin/env python3
"""
🔄 Demo Error Recovery System Enterprise v2.7.0
Démonstration complète du système de récupération d'erreurs

Usage:
    python scripts/demo_error_recovery.py
    python scripts/demo_error_recovery.py --stress-test
    python scripts/demo_error_recovery.py --integration-test
"""

from core.ark_logger import ark_logger
import argparse
import asyncio
import logging
import sys
from datetime import datetime
from pathlib import Path

# Ajouter le module au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.zeroia.error_recovery_system import (
    CognitiveOverloadError,
    DecisionIntegrityError,
    ErrorRecoverySystem,
    ErrorSeverity,
    RecoveryStrategy,
    SystemRebootRequired,
    ZeroIAError,
)

# Configuration du logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ErrorRecoveryDemo:
    """Démonstration du système Error Recovery"""

    def __init__(self) -> None:
        self.recovery_system = ErrorRecoverySystem()
        self.demo_stats = {
            "scenarios_tested": 0,
            "successes": 0,
            "failures": 0,
            "start_time": datetime.now(),
        }

    async def demo_immediate_retry(self):
        """Demo : Retry immédiat"""
        ark_logger.info("\n🔄 === TEST : Immediate Retry ===", extra={"module": "scripts"})

        try:
            # Simuler erreur générique (LOW severity)
            test_error = ValueError("Connection timeout")

            result = await self.recovery_system.handle_error(
                test_error, "demo_module", "immediate_retry_test"
            )

            if result and result.get("status") == "retried":
                ark_logger.info("✅ Immediate retry: SUCCESS", extra={"module": "scripts"})
                self.demo_stats["successes"] += 1
            else:
                ark_logger.error("❌ Immediate retry: FAILED", extra={"module": "scripts"})
                self.demo_stats["failures"] += 1

        except Exception as e:
            raise RuntimeError(f"Erreur demo error recovery: {e}") from e
            self.demo_stats["failures"] += 1

        self.demo_stats["scenarios_tested"] += 1

    async def demo_exponential_backoff(self):
        """Demo : Backoff exponentiel"""
        ark_logger.info("\n⏳ === TEST : Exponential Backoff ===", extra={"module": "scripts"})

        try:
            # Simuler erreur ZeroIA (MEDIUM severity)
            test_error = ZeroIAError("Processing overload")

            start_time = asyncio.get_event_loop().time()
            result = await self.recovery_system.handle_error(
                test_error, "demo_module", "backoff_test"
            )
            end_time = asyncio.get_event_loop().time()

            if result and result.get("status") == "backoff_completed":
                elapsed = end_time - start_time
                ark_logger.info(f"✅ Exponential backoff: SUCCESS (took {elapsed:.2f}s, extra={"module": "scripts"})")
                self.demo_stats["successes"] += 1
            else:
                ark_logger.error("❌ Exponential backoff: FAILED", extra={"module": "scripts"})
                self.demo_stats["failures"] += 1

        except Exception as e:
            raise RuntimeError(f"Erreur demo error recovery: {e}") from e
            self.demo_stats["failures"] += 1

        self.demo_stats["scenarios_tested"] += 1

    async def demo_graceful_degradation(self):
        """Demo : Dégradation gracieuse"""
        ark_logger.info("\n📉 === TEST : Graceful Degradation ===", extra={"module": "scripts"})

        try:
            # Simuler erreur d'intégrité (HIGH severity)
            test_error = DecisionIntegrityError("Data corruption detected")

            result = await self.recovery_system.handle_error(
                test_error, "demo_module", "degradation_test"
            )

            if result and result.get("status") == "degraded_mode":
                available = result.get("features_available", [])
                disabled = result.get("features_disabled", [])
                ark_logger.info("✅ Graceful degradation: SUCCESS", extra={"module": "scripts"})
                ark_logger.info(f"   📊 Features available: {available}", extra={"module": "scripts"})
                ark_logger.info(f"   🚫 Features disabled: {disabled}", extra={"module": "scripts"})
                self.demo_stats["successes"] += 1
            else:
                ark_logger.error("❌ Graceful degradation: FAILED", extra={"module": "scripts"})
                self.demo_stats["failures"] += 1

        except Exception as e:
            raise RuntimeError(f"Erreur demo error recovery: {e}") from e
            self.demo_stats["failures"] += 1

        self.demo_stats["scenarios_tested"] += 1

    async def demo_system_restart(self):
        """Demo : Redémarrage système"""
        ark_logger.info("\n🔄 === TEST : System Restart ===", extra={"module": "scripts"})

        try:
            # Simuler erreur critique
            test_error = SystemRebootRequired("Critical system failure")

            start_time = asyncio.get_event_loop().time()
            result = await self.recovery_system.handle_error(
                test_error, "demo_module", "restart_test"
            )
            end_time = asyncio.get_event_loop().time()

            if result and result.get("status") == "system_restarted":
                elapsed = end_time - start_time
                ark_logger.info(f"✅ System restart: SUCCESS (simulated in {elapsed:.2f}s, extra={"module": "scripts"})")
                ark_logger.info(f"   🕰️ Restart timestamp: {result.get('timestamp', extra={"module": "scripts"})}")
                self.demo_stats["successes"] += 1
            else:
                ark_logger.error("❌ System restart: FAILED", extra={"module": "scripts"})
                self.demo_stats["failures"] += 1

        except Exception as e:
            raise RuntimeError(f"Erreur demo error recovery: {e}") from e
            self.demo_stats["failures"] += 1

        self.demo_stats["scenarios_tested"] += 1

    async def demo_manual_intervention(self):
        """Demo : Intervention manuelle"""
        ark_logger.info("\n🚨 === TEST : Manual Intervention ===", extra={"module": "scripts"})

        try:
            # Simuler erreur fatale
            test_error = Exception("Unrecoverable system error")

            # Modifier temporairement la config pour forcer l'intervention manuelle
            original_config = self.recovery_system.error_strategies["Exception"]
            self.recovery_system.error_strategies["Exception"] = {
                "severity": ErrorSeverity.FATAL,
                "strategy": RecoveryStrategy.MANUAL_INTERVENTION,
                "max_attempts": 1,
            }

            result = await self.recovery_system.handle_error(
                test_error, "demo_module", "manual_intervention_test"
            )

            # Restaurer la config originale
            self.recovery_system.error_strategies["Exception"] = original_config

            if result and result.get("status") == "manual_intervention_required":
                incident_id = result.get("incident_id")
                contact = result.get("contact")
                ark_logger.info("✅ Manual intervention: SUCCESS", extra={"module": "scripts"})
                ark_logger.info(f"   🎫 Incident ID: {incident_id}", extra={"module": "scripts"})
                ark_logger.info(f"   📞 Contact: {contact}", extra={"module": "scripts"})
                self.demo_stats["successes"] += 1
            else:
                ark_logger.error("❌ Manual intervention: FAILED", extra={"module": "scripts"})
                self.demo_stats["failures"] += 1

        except Exception as e:
            raise RuntimeError(f"Erreur demo error recovery: {e}") from e
            self.demo_stats["failures"] += 1

        self.demo_stats["scenarios_tested"] += 1

    async def demo_health_check(self):
        """Demo : Health check"""
        ark_logger.info("\n🩺 === TEST : Health Check ===", extra={"module": "scripts"})

        try:
            health = await self.recovery_system.health_check()

            if health.get("status") == "healthy":
                ark_logger.info("✅ Health check: HEALTHY", extra={"module": "scripts"})
                ark_logger.info(f"   🔧 Recovery system: {health.get('recovery_system', extra={"module": "scripts"})}")
                ark_logger.info(f"   🧪 Test recovery: {health.get('test_recovery', extra={"module": "scripts"})}")
                self.demo_stats["successes"] += 1
            else:
                ark_logger.info(f"⚠️ Health check: {health.get('status', extra={"module": "scripts"})}")
                self.demo_stats["failures"] += 1

        except Exception as e:
            raise RuntimeError(f"Erreur demo error recovery: {e}") from e
            self.demo_stats["failures"] += 1

        self.demo_stats["scenarios_tested"] += 1

    def display_recovery_status(self):
        """Affiche le statut du système de récupération"""
        ark_logger.info("\n📊 === RECOVERY SYSTEM STATUS ===", extra={"module": "scripts"})

        status = self.recovery_system.get_recovery_status()
        metrics = status["metrics"]

        ark_logger.error(f"🔢 Total errors handled: {metrics['total_errors']}", extra={"module": "scripts"})
        ark_logger.info(f"📈 Recovery rate: {metrics['recovery_rate']:.1%}", extra={"module": "scripts"})
        ark_logger.info(f"⏱️ Average recovery time: {metrics['average_recovery_time']:.3f}s", extra={"module": "scripts"})
        ark_logger.info(f"🏥 System health: {status['system_health']}", extra={"module": "scripts"})

        if metrics["strategies_used"]:
            ark_logger.info("\n🛠️ Strategies used:", extra={"module": "scripts"})
            for strategy, count in metrics["strategies_used"].items():
                ark_logger.info(f"   • {strategy}: {count}x", extra={"module": "scripts"})

    def display_demo_summary(self):
        """Affiche le résumé de la démo"""
        ark_logger.info("\n" + "=" * 50, extra={"module": "scripts"})
        ark_logger.info("📋 DEMO SUMMARY", extra={"module": "scripts"})
        ark_logger.info("=" * 50, extra={"module": "scripts"})

        duration = datetime.now() - self.demo_stats["start_time"]
        success_rate = (
            self.demo_stats["successes"] / max(1, self.demo_stats["scenarios_tested"])
        ) * 100

        ark_logger.info(f"⏱️ Duration: {duration.total_seconds(, extra={"module": "scripts"}):.2f}s")
        ark_logger.info(f"🧪 Scenarios tested: {self.demo_stats['scenarios_tested']}", extra={"module": "scripts"})
        ark_logger.info(f"✅ Successes: {self.demo_stats['successes']}", extra={"module": "scripts"})
        ark_logger.error(f"❌ Failures: {self.demo_stats['failures']}", extra={"module": "scripts"})
        ark_logger.info(f"📊 Success rate: {success_rate:.1f}%", extra={"module": "scripts"})

        if success_rate >= 90:
            ark_logger.error("🎉 EXCELLENT! Error Recovery System is working perfectly!", extra={"module": "scripts"})
        elif success_rate >= 70:
            ark_logger.error("👍 GOOD! Error Recovery System is mostly functional", extra={"module": "scripts"})
        else:
            ark_logger.error("⚠️ WARNING! Error Recovery System needs attention", extra={"module": "scripts"})

    async def run_basic_demo(self):
        """Lance la démo de base"""
        ark_logger.error("🔄 ERROR RECOVERY SYSTEM DEMO v2.7.0", extra={"module": "scripts"})
        ark_logger.info("=====================================", extra={"module": "scripts"})

        # Tests de base
        await self.demo_immediate_retry()
        await self.demo_exponential_backoff()
        await self.demo_graceful_degradation()
        await self.demo_system_restart()
        await self.demo_manual_intervention()
        await self.demo_health_check()

        # Affichage des résultats
        self.display_recovery_status()
        self.display_demo_summary()

    async def run_stress_test(self):
        """Lance un test de stress"""
        ark_logger.error("⚡ ERROR RECOVERY STRESS TEST", extra={"module": "scripts"})
        ark_logger.info("============================", extra={"module": "scripts"})

        stress_errors = [
            ValueError("Stress error 1"),
            ZeroIAError("Stress error 2"),
            CognitiveOverloadError("Stress error 3"),
            DecisionIntegrityError("Stress error 4"),
            Exception("Stress error 5"),
        ]

        start_time = asyncio.get_event_loop().time()

        # Lancer 50 erreurs en parallèle
        tasks = []
        for i in range(10):
            for error in stress_errors:
                task = self.recovery_system.handle_error(error, "stress_test", f"batch_{i}")
                tasks.append(task)

        ark_logger.info(f"🚀 Launching {len(tasks, extra={"module": "scripts"})} recovery tasks...")
        results = await asyncio.gather(*tasks, return_exceptions=True)

        end_time = asyncio.get_event_loop().time()
        duration = end_time - start_time

        # Analyser les résultats
        successes = sum(1 for r in results if r and not isinstance(r, Exception))
        failures = len(results) - successes

        ark_logger.info("\n📊 STRESS TEST RESULTS:", extra={"module": "scripts"})
        ark_logger.info(f"⏱️ Duration: {duration:.2f}s", extra={"module": "scripts"})
        ark_logger.info(f"🔢 Total tasks: {len(tasks, extra={"module": "scripts"})}")
        ark_logger.info(f"✅ Successes: {successes}", extra={"module": "scripts"})
        ark_logger.error(f"❌ Failures: {failures}", extra={"module": "scripts"})
        ark_logger.info(f"🚀 Throughput: {len(tasks, extra={"module": "scripts"})/duration:.1f} recoveries/sec")

        self.display_recovery_status()

    async def run_integration_test(self):
        """Lance un test d'intégration avec les modules existants"""
        ark_logger.error("🔗 ERROR RECOVERY INTEGRATION TEST", extra={"module": "scripts"})
        ark_logger.info("==================================", extra={"module": "scripts"})

        try:
            # Simuler intégration avec Circuit Breaker
            from modules.zeroia.circuit_breaker import CircuitBreaker
            from modules.zeroia.event_store import EventStore

            ark_logger.info("📦 Creating integrated system...", extra={"module": "scripts"})
            circuit_breaker = CircuitBreaker()
            event_store = EventStore()

            integrated_system = ErrorRecoverySystem(circuit_breaker, event_store)

            # Test avec le système intégré
            test_error = CognitiveOverloadError("Integration test error")
            result = await integrated_system.handle_error(test_error, "integration_test", "main")

            if result:
                ark_logger.info("✅ Integration test: SUCCESS", extra={"module": "scripts"})
                ark_logger.info(f"   📊 Result: {result}", extra={"module": "scripts"})
            else:
                ark_logger.error("❌ Integration test: FAILED", extra={"module": "scripts"})

            # Vérifier les métriques
            status = integrated_system.get_recovery_status()
            ark_logger.info("\n📈 Integration metrics:", extra={"module": "scripts"})
            ark_logger.info(f"   Recovery rate: {status['metrics']['recovery_rate']:.1%}", extra={"module": "scripts"})
            ark_logger.info(f"   Circuit breaker: {status.get('circuit_breaker', 'N/A', extra={"module": "scripts"})}")

        except ImportError as e:
            ark_logger.info(f"⚠️ Integration modules not available: {e}", extra={"module": "scripts"})
            ark_logger.info("   Running basic integration test...", extra={"module": "scripts"})

            # Test basic sans dépendances
            await self.demo_immediate_retry()
            ark_logger.info("✅ Basic integration: SUCCESS", extra={"module": "scripts"})


async def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(description="Error Recovery System Demo")
    parser.add_argument("--stress-test", action="store_true", help="Run stress test")
    parser.add_argument("--integration-test", action="store_true", help="Run integration test")

    args = parser.parse_args()

    demo = ErrorRecoveryDemo()

    try:
        if args.stress_test:
            await demo.run_stress_test()
        elif args.integration_test:
            await demo.run_integration_test()
        else:
            await demo.run_basic_demo()

    except KeyboardInterrupt:
        ark_logger.info("\n🛑 Demo interrupted by user", extra={"module": "scripts"})
        demo.display_demo_summary()
    except Exception as e:
        ark_logger.error(f"\n💥 Demo error: {e}", extra={"module": "scripts"})
        logger.exception("Demo failed")
        return 1

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
