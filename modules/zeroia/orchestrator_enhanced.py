# 🚀 modules/zeroia/orchestrator_enhanced.py
"""
Orchestrateur ZeroIA Enhanced avec Circuit Breaker + Event Sourcing

CHANGEMENTS v2.6.0:
- Intégration Circuit Breaker pour protection cascade failures
- Event Sourcing pour traçabilité complète des décisions
- Resilience patterns enterprise pour production
- Monitoring et métriques temps réel
"""

import logging
import time
from typing import Any, Optional

from .circuit_breaker import CognitiveOverloadError, DecisionIntegrityError, SystemRebootRequired
from .event_store import EventType
from .reason_loop_enhanced import cleanup_components, initialize_components, reason_loop_enhanced

logger = logging.getLogger(__name__)


class ZeroIAOrchestrator:
    """
    Orchestrateur ZeroIA Enhanced avec patterns de resilience

    Features:
    - Circuit Breaker intégré pour protection system-wide
    - Event Sourcing pour audit et debugging
    - Graceful degradation en cas de surcharge
    - Métriques et monitoring temps réel
    """

    def __init__(
        self,
        max_loops: int | None = None,
        interval_seconds: float = 2.5,
        circuit_failure_threshold: int = 10,
        timeout: int = 60,
    ):
        self.max_loops = max_loops
        self.interval_seconds = interval_seconds
        self.loop_count = 0
        self.start_time = time.time()

        # Initialiser les composants enhanced
        self.circuit_breaker, self.event_store = initialize_components()

        # Configurer les seuils du circuit breaker après initialisation
        self.circuit_breaker.failure_threshold = circuit_failure_threshold
        self.circuit_breaker.timeout = timeout

        # Statistiques de session
        self.session_stats = {
            "total_decisions": 0,
            "successful_decisions": 0,
            "failed_decisions": 0,
            "circuit_openings": 0,
            "start_time": self.start_time,
        }

        logger.info("🚀 ZeroIA Orchestrator Enhanced initialisé")

    def run(self) -> None:
        """Exécute la boucle orchestrée avec resilience patterns"""
        logger.info(f"🎯 Démarrage orchestration (max_loops={self.max_loops})")

        try:
            while self._should_continue():
                self._execute_single_loop()
                time.sleep(self.interval_seconds)

        except KeyboardInterrupt:
            logger.info("⏹️ Arrêt orchestration (Ctrl+C)")
        except SystemExit:
            logger.info("⏹️ Arrêt orchestration (SystemExit)")
        except Exception as e:
            logger.error(f"💥 Erreur fatale orchestration: {e}")
            self.event_store.add_event(
                EventType.SYSTEM_ERROR,
                {"error": str(e), "error_type": type(e).__name__},
                module="orchestrator",
            )
        finally:
            self._cleanup_and_report()

    def _execute_single_loop(self) -> None:
        """Exécute une seule itération de la boucle avec protection"""
        self.loop_count += 1
        logger.debug(f"🔄 Loop #{self.loop_count}")

        try:
            # Exécuter decision via Circuit Breaker
            decision, score = self.circuit_breaker.call(reason_loop_enhanced)

            # Log succès
            logger.info(f"✅ Décision: {decision} | Score: {score:.3f}")
            self.session_stats["successful_decisions"] += 1

            # Event Sourcing
            self.event_store.add_event(
                EventType.DECISION_MADE,
                {
                    "decision": decision,
                    "confidence_score": score,
                    "loop_number": self.loop_count,
                    "circuit_state": self.circuit_breaker.state,
                },
                module="orchestrator",
            )

        except SystemRebootRequired as e:
            logger.warning(f"🔄 System reboot requis: {e}")
            self.session_stats["circuit_openings"] += 1
            self._handle_system_reboot()

        except (CognitiveOverloadError, DecisionIntegrityError) as e:
            logger.warning(f"⚠️ Erreur gérée: {e}")
            self.session_stats["failed_decisions"] += 1

        except Exception as e:
            logger.error(f"💥 Erreur inattendue loop #{self.loop_count}: {e}")
            self.session_stats["failed_decisions"] += 1

        finally:
            self.session_stats["total_decisions"] += 1

    def _should_continue(self) -> bool:
        """Vérifie si l'orchestration doit continuer"""
        if self.max_loops and self.loop_count >= self.max_loops:
            logger.info(f"⏹️ Max loops atteint ({self.max_loops})")
            return False
        return True

    def _handle_system_reboot(self) -> None:
        """Gère la procédure de reboot système"""
        logger.warning("🔄 Procédure reboot système en cours...")

        # Attendre recovery du circuit breaker
        time.sleep(self.circuit_breaker.timeout)

        # Log event
        self.event_store.add_event(
            EventType.SYSTEM_ERROR,
            {
                "action": "system_reboot_handled",
                "circuit_state": self.circuit_breaker.state,
                "loop_number": self.loop_count,
            },
            module="orchestrator",
        )

    def get_status(self) -> dict[str, Any]:
        """Retourne le statut complet de l'orchestrateur"""
        uptime = time.time() - self.start_time
        circuit_status = self.circuit_breaker.get_status()

        return {
            "orchestrator": {
                "loop_count": self.loop_count,
                "uptime_seconds": uptime,
                "max_loops": self.max_loops,
                "interval_seconds": self.interval_seconds,
            },
            "session_stats": self.session_stats,
            "circuit_breaker": circuit_status,
            "event_store": {
                "total_events": self.event_store.event_counter,
                "cache_info": "Disk cache active",
            },
        }

    def _cleanup_and_report(self) -> None:
        """Nettoyage final et rapport de session"""
        uptime = time.time() - self.start_time

        # Rapport final
        logger.info("=" * 60)
        logger.info("🎯 RAPPORT FINAL ORCHESTRATION")
        logger.info("=" * 60)
        logger.info(f"⏱️ Durée: {uptime:.1f}s")
        logger.info(f"🔄 Loops: {self.loop_count}")
        logger.info(f"✅ Succès: {self.session_stats['successful_decisions']}")
        logger.info(f"❌ Échecs: {self.session_stats['failed_decisions']}")
        logger.info(f"🔄 Circuit ouvertures: {self.session_stats['circuit_openings']}")

        if self.session_stats["total_decisions"] > 0:
            success_rate = (
                self.session_stats["successful_decisions"] / self.session_stats["total_decisions"]
            ) * 100
            logger.info(f"📊 Taux succès: {success_rate:.1f}%")

        # Event final
        self.event_store.add_event(
            EventType.SYSTEM_ERROR,  # Pas d'event ORCHESTRATOR_STOPPED, on utilise SYSTEM_ERROR
            {
                "action": "orchestration_stopped",
                "session_stats": self.session_stats,
                "uptime_seconds": uptime,
            },
            module="orchestrator",
        )

        # Cleanup
        cleanup_components(self.circuit_breaker, self.event_store)
        logger.info("🧹 Cleanup terminé")


def orchestrate_zeroia_enhanced(
    max_loops: int | None = None,
    interval_seconds: float = 1.5,
    circuit_failure_threshold: int = 5,
    timeout: int = 30,
) -> None:
    """
    Lance l'orchestration ZeroIA Enhanced

    Args:
        max_loops: Nombre max de loops (None = infini)
        interval_seconds: Intervalle entre loops
        circuit_failure_threshold: Seuil d'échecs pour ouvrir circuit
        timeout: Timeout recovery circuit (secondes)
    """
    orchestrator = ZeroIAOrchestrator(
        max_loops=max_loops,
        interval_seconds=interval_seconds,
        circuit_failure_threshold=circuit_failure_threshold,
        timeout=timeout,
    )

    orchestrator.run()


if __name__ == "__main__":
    # Exemple d'utilisation
    orchestrate_zeroia_enhanced(max_loops=10)
