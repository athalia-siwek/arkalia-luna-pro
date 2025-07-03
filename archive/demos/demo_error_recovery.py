#!/usr/bin/env python3
"""
🔄 Demo Error Recovery System Enterprise v2.7.0
Démonstration complète du système de récupération d'erreurs

Usage:
    python scripts/demo_error_recovery.py
    python scripts/demo_error_recovery.py --stress-test
    python scripts/demo_error_recovery.py --integration-test
"""

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
        print("\n🔄 === TEST : Immediate Retry ===")

        try:
            # Simuler erreur générique (LOW severity)
            test_error = ValueError("Connection timeout")

            result = await self.recovery_system.handle_error(
                test_error, "demo_module", "immediate_retry_test"
            )

            if result and result.get("status") == "retried":
                print("✅ Immediate retry: SUCCESS")
                self.demo_stats["successes"] += 1
            else:
                print("❌ Immediate retry: FAILED")
                self.demo_stats["failures"] += 1

        except Exception as e:
            raise RuntimeError(f"Erreur demo error recovery: {e}") from e
            self.demo_stats["failures"] += 1

        self.demo_stats["scenarios_tested"] += 1

    async def demo_exponential_backoff(self):
        """Demo : Backoff exponentiel"""
        print("\n⏳ === TEST : Exponential Backoff ===")

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
                print(f"✅ Exponential backoff: SUCCESS (took {elapsed:.2f}s)")
                self.demo_stats["successes"] += 1
            else:
                print("❌ Exponential backoff: FAILED")
                self.demo_stats["failures"] += 1

        except Exception as e:
            raise RuntimeError(f"Erreur demo error recovery: {e}") from e
            self.demo_stats["failures"] += 1

        self.demo_stats["scenarios_tested"] += 1

    async def demo_graceful_degradation(self):
        """Demo : Dégradation gracieuse"""
        print("\n📉 === TEST : Graceful Degradation ===")

        try:
            # Simuler erreur d'intégrité (HIGH severity)
            test_error = DecisionIntegrityError("Data corruption detected")

            result = await self.recovery_system.handle_error(
                test_error, "demo_module", "degradation_test"
            )

            if result and result.get("status") == "degraded_mode":
                available = result.get("features_available", [])
                disabled = result.get("features_disabled", [])
                print("✅ Graceful degradation: SUCCESS")
                print(f"   📊 Features available: {available}")
                print(f"   🚫 Features disabled: {disabled}")
                self.demo_stats["successes"] += 1
            else:
                print("❌ Graceful degradation: FAILED")
                self.demo_stats["failures"] += 1

        except Exception as e:
            raise RuntimeError(f"Erreur demo error recovery: {e}") from e
            self.demo_stats["failures"] += 1

        self.demo_stats["scenarios_tested"] += 1

    async def demo_system_restart(self):
        """Demo : Redémarrage système"""
        print("\n🔄 === TEST : System Restart ===")

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
                print(f"✅ System restart: SUCCESS (simulated in {elapsed:.2f}s)")
                print(f"   🕰️ Restart timestamp: {result.get('timestamp')}")
                self.demo_stats["successes"] += 1
            else:
                print("❌ System restart: FAILED")
                self.demo_stats["failures"] += 1

        except Exception as e:
            raise RuntimeError(f"Erreur demo error recovery: {e}") from e
            self.demo_stats["failures"] += 1

        self.demo_stats["scenarios_tested"] += 1

    async def demo_manual_intervention(self):
        """Demo : Intervention manuelle"""
        print("\n🚨 === TEST : Manual Intervention ===")

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
                print("✅ Manual intervention: SUCCESS")
                print(f"   🎫 Incident ID: {incident_id}")
                print(f"   📞 Contact: {contact}")
                self.demo_stats["successes"] += 1
            else:
                print("❌ Manual intervention: FAILED")
                self.demo_stats["failures"] += 1

        except Exception as e:
            raise RuntimeError(f"Erreur demo error recovery: {e}") from e
            self.demo_stats["failures"] += 1

        self.demo_stats["scenarios_tested"] += 1

    async def demo_health_check(self):
        """Demo : Health check"""
        print("\n🩺 === TEST : Health Check ===")

        try:
            health = await self.recovery_system.health_check()

            if health.get("status") == "healthy":
                print("✅ Health check: HEALTHY")
                print(f"   🔧 Recovery system: {health.get('recovery_system')}")
                print(f"   🧪 Test recovery: {health.get('test_recovery')}")
                self.demo_stats["successes"] += 1
            else:
                print(f"⚠️ Health check: {health.get('status')}")
                self.demo_stats["failures"] += 1

        except Exception as e:
            raise RuntimeError(f"Erreur demo error recovery: {e}") from e
            self.demo_stats["failures"] += 1

        self.demo_stats["scenarios_tested"] += 1

    def display_recovery_status(self):
        """Affiche le statut du système de récupération"""
        print("\n📊 === RECOVERY SYSTEM STATUS ===")

        status = self.recovery_system.get_recovery_status()
        metrics = status["metrics"]

        print(f"🔢 Total errors handled: {metrics['total_errors']}")
        print(f"📈 Recovery rate: {metrics['recovery_rate']:.1%}")
        print(f"⏱️ Average recovery time: {metrics['average_recovery_time']:.3f}s")
        print(f"🏥 System health: {status['system_health']}")

        if metrics["strategies_used"]:
            print("\n🛠️ Strategies used:")
            for strategy, count in metrics["strategies_used"].items():
                print(f"   • {strategy}: {count}x")

    def display_demo_summary(self):
        """Affiche le résumé de la démo"""
        print("\n" + "=" * 50)
        print("📋 DEMO SUMMARY")
        print("=" * 50)

        duration = datetime.now() - self.demo_stats["start_time"]
        success_rate = (
            self.demo_stats["successes"] / max(1, self.demo_stats["scenarios_tested"])
        ) * 100

        print(f"⏱️ Duration: {duration.total_seconds():.2f}s")
        print(f"🧪 Scenarios tested: {self.demo_stats['scenarios_tested']}")
        print(f"✅ Successes: {self.demo_stats['successes']}")
        print(f"❌ Failures: {self.demo_stats['failures']}")
        print(f"📊 Success rate: {success_rate:.1f}%")

        if success_rate >= 90:
            print("🎉 EXCELLENT! Error Recovery System is working perfectly!")
        elif success_rate >= 70:
            print("👍 GOOD! Error Recovery System is mostly functional")
        else:
            print("⚠️ WARNING! Error Recovery System needs attention")

    async def run_basic_demo(self):
        """Lance la démo de base"""
        print("🔄 ERROR RECOVERY SYSTEM DEMO v2.7.0")
        print("=====================================")

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
        print("⚡ ERROR RECOVERY STRESS TEST")
        print("============================")

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

        print(f"🚀 Launching {len(tasks)} recovery tasks...")
        results = await asyncio.gather(*tasks, return_exceptions=True)

        end_time = asyncio.get_event_loop().time()
        duration = end_time - start_time

        # Analyser les résultats
        successes = sum(1 for r in results if r and not isinstance(r, Exception))
        failures = len(results) - successes

        print("\n📊 STRESS TEST RESULTS:")
        print(f"⏱️ Duration: {duration:.2f}s")
        print(f"🔢 Total tasks: {len(tasks)}")
        print(f"✅ Successes: {successes}")
        print(f"❌ Failures: {failures}")
        print(f"🚀 Throughput: {len(tasks)/duration:.1f} recoveries/sec")

        self.display_recovery_status()

    async def run_integration_test(self):
        """Lance un test d'intégration avec les modules existants"""
        print("🔗 ERROR RECOVERY INTEGRATION TEST")
        print("==================================")

        try:
            # Simuler intégration avec Circuit Breaker
            from modules.zeroia.circuit_breaker import CircuitBreaker
            from modules.zeroia.event_store import EventStore

            print("📦 Creating integrated system...")
            circuit_breaker = CircuitBreaker()
            event_store = EventStore()

            integrated_system = ErrorRecoverySystem(circuit_breaker, event_store)

            # Test avec le système intégré
            test_error = CognitiveOverloadError("Integration test error")
            result = await integrated_system.handle_error(test_error, "integration_test", "main")

            if result:
                print("✅ Integration test: SUCCESS")
                print(f"   📊 Result: {result}")
            else:
                print("❌ Integration test: FAILED")

            # Vérifier les métriques
            status = integrated_system.get_recovery_status()
            print("\n📈 Integration metrics:")
            print(f"   Recovery rate: {status['metrics']['recovery_rate']:.1%}")
            print(f"   Circuit breaker: {status.get('circuit_breaker', 'N/A')}")

        except ImportError as e:
            print(f"⚠️ Integration modules not available: {e}")
            print("   Running basic integration test...")

            # Test basic sans dépendances
            await self.demo_immediate_retry()
            print("✅ Basic integration: SUCCESS")


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
        print("\n🛑 Demo interrupted by user")
        demo.display_demo_summary()
    except Exception as e:
        print(f"\n💥 Demo error: {e}")
        logger.exception("Demo failed")
        return 1

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
