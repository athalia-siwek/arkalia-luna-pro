"""
🔄 Error Recovery System Enterprise v2.7.0
Système central de récupération d'erreurs pour Arkalia-LUNA

Fonctionnalités :
- Recovery automatique intelligent
- Escalation d'erreurs hiérarchique
- Métriques temps réel
- Patterns de récupération configurables
- Intégration Event Sourcing + Circuit Breaker
"""

import asyncio
import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional

try:
    from .circuit_breaker import CircuitBreaker
    from .event_store import EventStore, EventType
except ImportError:
    # Fallback si modules pas disponibles
    CircuitBreaker = None
    EventStore = None
    EventType = None

logger = logging.getLogger(__name__)


# Définir nos propres exceptions pour éviter les conflits
class ZeroIAError(Exception):
    """Exception de base pour ZeroIA"""

    pass


class CognitiveOverloadError(ZeroIAError):
    """Surcharge cognitive détectée"""

    pass


class DecisionIntegrityError(ZeroIAError):
    """Erreur d'intégrité des décisions"""

    pass


class SystemRebootRequired(ZeroIAError):
    """Redémarrage système requis"""

    pass


class RecoveryStrategy(Enum):
    """Stratégies de récupération disponibles"""

    IMMEDIATE_RETRY = "immediate_retry"
    EXPONENTIAL_BACKOFF = "exponential_backoff"
    CIRCUIT_BREAK = "circuit_break"
    GRACEFUL_DEGRADATION = "graceful_degradation"
    SYSTEM_RESTART = "system_restart"
    MANUAL_INTERVENTION = "manual_intervention"


class ErrorSeverity(Enum):
    """Niveaux de gravité des erreurs"""

    LOW = "low"  # Erreurs mineures, retry automatique
    MEDIUM = "medium"  # Erreurs modérées, backoff
    HIGH = "high"  # Erreurs graves, circuit breaker
    CRITICAL = "critical"  # Erreurs critiques, restart système
    FATAL = "fatal"  # Erreurs fatales, intervention manuelle


@dataclass
class RecoveryMetrics:
    """Métriques de récupération"""

    total_errors: int = 0
    recovered_errors: int = 0
    failed_recoveries: int = 0
    total_recovery_time: float = 0.0
    last_recovery_attempt: Optional[datetime] = None
    recovery_strategies_used: Dict[str, int] = field(default_factory=dict)

    @property
    def recovery_rate(self) -> float:
        """Taux de récupération (0.0 à 1.0)"""
        if self.total_errors == 0:
            return 0.0
        return self.recovered_errors / self.total_errors

    @property
    def average_recovery_time(self) -> float:
        """Temps moyen de récupération en secondes"""
        if self.recovered_errors == 0:
            return 0.0
        return self.total_recovery_time / self.recovered_errors


@dataclass
class ErrorContext:
    """Contexte d'une erreur pour la récupération"""

    error: Exception
    severity: ErrorSeverity
    module: str
    function: str
    timestamp: datetime
    attempt_count: int = 0
    max_attempts: int = 3
    recovery_strategy: Optional[RecoveryStrategy] = None
    context_data: Dict[str, Any] = field(default_factory=dict)

    @property
    def can_retry(self) -> bool:
        """Vérifie si on peut encore tenter une récupération"""
        return self.attempt_count < self.max_attempts


class ErrorRecoverySystem:
    """
    Système central de récupération d'erreurs Enterprise

    Architecture :
    - Classification automatique des erreurs
    - Stratégies de récupération configurables
    - Métriques temps réel
    - Intégration complète avec Event Sourcing
    """

    def __init__(
        self,
        circuit_breaker: Optional[Any] = None,
        event_store: Optional[Any] = None,
        config_path: Optional[str] = None,
    ):
        self.circuit_breaker = circuit_breaker
        self.event_store = event_store
        self.metrics = RecoveryMetrics()

        # Configuration des stratégies par type d'erreur
        self.error_strategies = self._load_error_strategies(config_path)

        # Handlers de récupération
        self.recovery_handlers = {
            RecoveryStrategy.IMMEDIATE_RETRY: self._immediate_retry,
            RecoveryStrategy.EXPONENTIAL_BACKOFF: self._exponential_backoff,
            RecoveryStrategy.CIRCUIT_BREAK: self._circuit_break_recovery,
            RecoveryStrategy.GRACEFUL_DEGRADATION: self._graceful_degradation,
            RecoveryStrategy.SYSTEM_RESTART: self._system_restart,
            RecoveryStrategy.MANUAL_INTERVENTION: self._manual_intervention,
        }

        logger.info("🔄 ErrorRecoverySystem initialisé")

    def _load_error_strategies(self, config_path: Optional[str]) -> Dict[str, Dict]:
        """Charge la configuration des stratégies d'erreur"""
        default_config = {
            "ZeroIAError": {
                "severity": ErrorSeverity.MEDIUM,
                "strategy": RecoveryStrategy.EXPONENTIAL_BACKOFF,
                "max_attempts": 3,
            },
            "CognitiveOverloadError": {
                "severity": ErrorSeverity.HIGH,
                "strategy": RecoveryStrategy.CIRCUIT_BREAK,
                "max_attempts": 2,
            },
            "DecisionIntegrityError": {
                "severity": ErrorSeverity.HIGH,
                "strategy": RecoveryStrategy.GRACEFUL_DEGRADATION,
                "max_attempts": 2,
            },
            "SystemRebootRequired": {
                "severity": ErrorSeverity.CRITICAL,
                "strategy": RecoveryStrategy.SYSTEM_RESTART,
                "max_attempts": 1,
            },
            "Exception": {
                "severity": ErrorSeverity.LOW,
                "strategy": RecoveryStrategy.IMMEDIATE_RETRY,
                "max_attempts": 3,
            },
        }

        if config_path and Path(config_path).exists():
            try:
                with open(config_path) as f:
                    custom_config = json.load(f)
                default_config.update(custom_config)
            except Exception as e:
                logger.warning(f"⚠️ Impossible de charger la config: {e}")

        return default_config

    async def handle_error(
        self,
        error: Exception,
        module: str,
        function: str,
        context_data: Optional[Dict[str, Any]] = None,
    ) -> Optional[Any]:
        """
        Point d'entrée principal pour la gestion d'erreurs

        Args:
            error: Exception à traiter
            module: Module où l'erreur s'est produite
            function: Fonction où l'erreur s'est produite
            context_data: Données contextuelles

        Returns:
            Résultat de la récupération si succès, None sinon
        """
        self.metrics.total_errors += 1

        # Classifier l'erreur
        error_context = self._classify_error(error, module, function, context_data)

        # Logger l'erreur
        logger.error(
            f"🚨 Erreur détectée [{error_context.severity.value}] "
            f"dans {module}.{function}: {error}"
        )

        # Event sourcing si disponible
        if self.event_store and hasattr(self.event_store, "add_event"):
            try:
                self.event_store.add_event(
                    "SYSTEM_ERROR",  # EventType.SYSTEM_ERROR
                    {
                        "module": module,
                        "function": function,
                        "error_type": type(error).__name__,
                        "error_message": str(error),
                        "severity": error_context.severity.value,
                        "strategy": (
                            error_context.recovery_strategy.value
                            if error_context.recovery_strategy
                            else None
                        ),
                        "timestamp": error_context.timestamp.isoformat(),
                    },
                )
            except Exception as e:
                logger.warning(f"⚠️ Event sourcing failed: {e}")

        # Tenter la récupération
        return await self._attempt_recovery(error_context)

    def _classify_error(
        self,
        error: Exception,
        module: str,
        function: str,
        context_data: Optional[Dict[str, Any]] = None,
    ) -> ErrorContext:
        """Classifie une erreur et détermine la stratégie de récupération"""
        error_type = type(error).__name__

        # Chercher config spécifique ou utiliser générique
        config = self.error_strategies.get(
            error_type, self.error_strategies["Exception"]
        )

        return ErrorContext(
            error=error,
            severity=config["severity"],
            module=module,
            function=function,
            timestamp=datetime.now(),
            max_attempts=config["max_attempts"],
            recovery_strategy=config["strategy"],
            context_data=context_data or {},
        )

    async def _attempt_recovery(self, error_context: ErrorContext) -> Optional[Any]:
        """Tente la récupération selon la stratégie définie"""
        if not error_context.can_retry:
            logger.error(f"❌ Maximum de tentatives atteint pour {error_context.error}")
            self.metrics.failed_recoveries += 1
            return None

        error_context.attempt_count += 1
        recovery_start = time.time()

        try:
            # Choisir et exécuter la stratégie
            strategy = error_context.recovery_strategy
            if strategy is None:
                logger.error("❌ Aucune stratégie définie")
                return None

            handler = self.recovery_handlers.get(strategy)

            if not handler:
                logger.error(f"❌ Stratégie inconnue: {strategy}")
                return None

            result = await handler(error_context)

            # Succès de récupération
            recovery_time = time.time() - recovery_start
            self._record_successful_recovery(strategy, recovery_time)

            return result

        except Exception as recovery_error:
            recovery_time = time.time() - recovery_start
            logger.error(f"❌ Échec de récupération: {recovery_error}")

            # Event sourcing de l'échec si disponible
            if self.event_store and hasattr(self.event_store, "add_event"):
                try:
                    self.event_store.add_event(
                        "SYSTEM_ERROR",
                        {
                            "recovery_failed": True,
                            "original_error": str(error_context.error),
                            "recovery_error": str(recovery_error),
                            "strategy": strategy.value if strategy else "unknown",
                            "attempt": error_context.attempt_count,
                            "recovery_time": recovery_time,
                        },
                    )
                except Exception:
                    pass

            # Essayer récupération récursive si possible
            if error_context.can_retry:
                return await self._attempt_recovery(error_context)

            self.metrics.failed_recoveries += 1
            return None

    def _record_successful_recovery(
        self, strategy: RecoveryStrategy, recovery_time: float
    ):
        """Enregistre une récupération réussie"""
        self.metrics.recovered_errors += 1
        self.metrics.total_recovery_time += recovery_time
        self.metrics.last_recovery_attempt = datetime.now()

        # Compter les stratégies utilisées
        strategy_name = strategy.value
        self.metrics.recovery_strategies_used[strategy_name] = (
            self.metrics.recovery_strategies_used.get(strategy_name, 0) + 1
        )

        logger.info(
            f"✅ Récupération réussie avec {strategy_name} en {recovery_time:.3f}s"
        )

        # Event sourcing du succès si disponible
        if self.event_store and hasattr(self.event_store, "add_event"):
            try:
                self.event_store.add_event(
                    "CIRCUIT_SUCCESS",
                    {
                        "recovery_successful": True,
                        "strategy": strategy_name,
                        "recovery_time": recovery_time,
                        "recovery_rate": self.metrics.recovery_rate,
                    },
                )
            except Exception:
                pass

    async def _immediate_retry(self, error_context: ErrorContext) -> Optional[Any]:
        """Stratégie : Retry immédiat"""
        logger.info(f"🔄 Retry immédiat pour {error_context.function}")
        await asyncio.sleep(0.1)  # Délai minimal
        return {"status": "retried", "strategy": "immediate"}

    async def _exponential_backoff(self, error_context: ErrorContext) -> Optional[Any]:
        """Stratégie : Backoff exponentiel"""
        delay = 2**error_context.attempt_count
        logger.info(f"⏳ Backoff {delay}s pour {error_context.function}")
        await asyncio.sleep(delay)
        return {"status": "backoff_completed", "delay": delay}

    async def _circuit_break_recovery(
        self, error_context: ErrorContext
    ) -> Optional[Any]:
        """Stratégie : Récupération via Circuit Breaker"""
        logger.info(f"🔄 Circuit breaker recovery pour {error_context.function}")

        # Forcer la réinitialisation du circuit si nécessaire
        if self.circuit_breaker and hasattr(self.circuit_breaker, "reset"):
            self.circuit_breaker.reset()

        await asyncio.sleep(5)  # Attente de stabilisation
        return {"status": "circuit_reset", "strategy": "circuit_break"}

    async def _graceful_degradation(self, error_context: ErrorContext) -> Optional[Any]:
        """Stratégie : Dégradation gracieuse"""
        logger.info(f"📉 Dégradation gracieuse pour {error_context.function}")

        # Mode dégradé avec fonctionnalités réduites
        return {
            "status": "degraded_mode",
            "features_available": ["basic", "monitoring"],
            "features_disabled": ["advanced", "analytics"],
        }

    async def _system_restart(self, error_context: ErrorContext) -> Optional[Any]:
        """Stratégie : Redémarrage système (simulé)"""
        logger.critical(f"🔄 Redémarrage système requis pour {error_context.function}")

        # En production, ceci déclencherait un vrai restart
        # Ici on simule avec un reset complet
        await asyncio.sleep(10)

        return {"status": "system_restarted", "timestamp": datetime.now().isoformat()}

    async def _manual_intervention(self, error_context: ErrorContext) -> Optional[Any]:
        """Stratégie : Intervention manuelle requise"""
        logger.critical(f"🚨 INTERVENTION MANUELLE REQUISE: {error_context.error}")

        # Créer ticket d'incident (simulé)
        incident_id = f"INC-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        return {
            "status": "manual_intervention_required",
            "incident_id": incident_id,
            "contact": "admin@arkalia-luna.com",
        }

    def get_recovery_status(self) -> Dict[str, Any]:
        """Retourne l'état actuel du système de récupération"""
        circuit_status = None
        if self.circuit_breaker and hasattr(self.circuit_breaker, "get_status"):
            try:
                circuit_status = self.circuit_breaker.get_status()
            except Exception:
                circuit_status = {"status": "unavailable"}

        return {
            "metrics": {
                "total_errors": self.metrics.total_errors,
                "recovery_rate": round(self.metrics.recovery_rate, 3),
                "average_recovery_time": round(self.metrics.average_recovery_time, 3),
                "strategies_used": self.metrics.recovery_strategies_used,
            },
            "circuit_breaker": circuit_status,
            "last_recovery": (
                self.metrics.last_recovery_attempt.isoformat()
                if self.metrics.last_recovery_attempt
                else None
            ),
            "system_health": (
                "healthy" if self.metrics.recovery_rate > 0.8 else "degraded"
            ),
        }

    async def health_check(self) -> Dict[str, Any]:
        """Vérification de santé du système de récupération"""
        try:
            # Test basic recovery
            test_error = Exception("Test error")
            result = await self.handle_error(test_error, "test", "health_check")

            return {
                "status": "healthy",
                "recovery_system": "operational",
                "test_recovery": "success" if result else "failed",
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }


# Factory function pour faciliter l'utilisation
def create_error_recovery_system(
    circuit_breaker: Optional[Any] = None, event_store: Optional[Any] = None
) -> ErrorRecoverySystem:
    """Factory pour créer un système de récupération configuré"""
    return ErrorRecoverySystem(circuit_breaker, event_store)
