#!/usr/bin/env python3
"""
💥 Error Recovery System Core - Système de récupération d'erreurs consolidé SOLID
Fusion des systèmes error_recovery et zeroia/error_recovery_system

Architecture SOLID :
- Interfaces pour les stratégies de récupération
- Factory pattern pour l'injection de dépendances
- Stratégies extensibles et configurables
- Métriques temps réel
"""

import asyncio
import logging
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional, TypedDict

import toml

logger = logging.getLogger(__name__)


# ============================================================================
# INTERFACES SOLID
# ============================================================================


class IRecoveryStrategy:
    """Interface pour les stratégies de récupération (ISP)"""

    async def execute(self, error_context: "ErrorContext") -> dict[str, Any]:
        """Exécute la stratégie de récupération"""
        raise NotImplementedError


class IErrorHandler:
    """Interface pour les gestionnaires d'erreurs (ISP)"""

    async def handle(self, error_type: "ErrorType", error_message: str) -> dict[str, Any]:
        """Gère une erreur spécifique"""
        raise NotImplementedError


# ============================================================================
# ENUMS ET TYPES
# ============================================================================


class RecoveryStrategy(Enum):
    """Stratégies de récupération disponibles (OCP)"""

    IMMEDIATE_RETRY = "immediate_retry"
    EXPONENTIAL_BACKOFF = "exponential_backoff"
    CIRCUIT_BREAK = "circuit_break"
    GRACEFUL_DEGRADATION = "graceful_degradation"
    SYSTEM_RESTART = "system_restart"
    MANUAL_INTERVENTION = "manual_intervention"
    RECONNECT = "reconnect"
    RESTORE_STATE = "restore_state"
    FORCE_RESTART = "force_restart"


class ErrorSeverity(Enum):
    """Niveaux de gravité des erreurs"""

    LOW = "low"  # Erreurs mineures, retry automatique
    MEDIUM = "medium"  # Erreurs modérées, backoff
    HIGH = "high"  # Erreurs graves, circuit breaker
    CRITICAL = "critical"  # Erreurs critiques, restart système
    FATAL = "fatal"  # Erreurs fatales, intervention manuelle


class ErrorType(Enum):
    """Types d'erreurs gérées par le système"""

    TIMEOUT = "timeout"
    MEMORY = "memory"
    CONTRADICTION = "contradiction"
    CONNECTION_LOST = "connection_lost"
    STATE_CORRUPTED = "state_corrupted"
    DEADLOCK = "deadlock"
    UNKNOWN = "unknown"


class RecoveryMetrics(TypedDict):
    """Métriques de récupération"""

    total_errors: int
    successful_recoveries: int
    failed_recoveries: int
    contradiction_count: int
    last_error_time: str | None


class RecoveryAttempt(TypedDict):
    """Tentative de récupération"""

    type: str
    zeroia_state: str
    reflexia_state: str
    resolved: bool


# ============================================================================
# EXCEPTIONS
# ============================================================================


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


# ============================================================================
# MODÈLES DE DONNÉES
# ============================================================================


class ErrorContext:
    """Contexte d'erreur pour la récupération"""

    def __init__(self, error_type: ErrorType, error_message: str, max_retries: int = 3) -> None:
        self.error_type = error_type
        self.error_message = error_message
        self.timestamp = datetime.utcnow().isoformat()
        self.attempt_count = 0
        self.max_retries = max_retries


class ModuleError:
    """Erreur d'un module"""

    def __init__(
        self,
        module_name: str,
        error_type: str,
        error_message: str,
        stack_trace: str | None = None,
        context: dict[str, Any] | None = None,
    ):
        self.module_name = module_name
        self.error_type = error_type
        self.error_message = error_message
        self.timestamp = datetime.now()
        self.stack_trace = stack_trace
        self.context = context or {}


class RecoveryAction:
    """Action de récupération"""

    def __init__(self, module_name: str, action_type: str, parameters: dict, priority: int = 1):
        self.module_name = module_name
        self.action_type = action_type
        self.parameters = parameters
        self.timestamp = datetime.now()
        self.priority = priority


class RecoveryResult:
    """Résultat d'une récupération"""

    def __init__(self, success: bool, action: RecoveryAction, error_fixed: bool, new_state: str):
        self.success = success
        self.action = action
        self.error_fixed = error_fixed
        self.new_state = new_state
        self.timestamp = datetime.now()


# ============================================================================
# STRATÉGIES DE RÉCUPÉRATION (OCP)
# ============================================================================


class ImmediateRetryStrategy(IRecoveryStrategy):
    """Stratégie : Retry immédiat"""

    async def execute(self, error_context: ErrorContext) -> dict[str, Any]:
        logger.info(f"🔄 Retry immédiat pour: {error_context.error_message}")
        await asyncio.sleep(1)  # Petit délai
        return {"status": "retry_completed", "strategy": "immediate_retry"}


class ExponentialBackoffStrategy(IRecoveryStrategy):
    """Stratégie : Backoff exponentiel"""

    async def execute(self, error_context: ErrorContext) -> dict[str, Any]:
        delay = 2**error_context.attempt_count
        logger.info(f"⏳ Backoff {delay}s pour {error_context.error_message}")
        await asyncio.sleep(delay)
        return {"status": "backoff_completed", "delay": delay}


class CircuitBreakStrategy(IRecoveryStrategy):
    """Stratégie : Circuit breaker"""

    async def execute(self, error_context: ErrorContext) -> dict[str, Any]:
        logger.info(f"🔌 Circuit break pour: {error_context.error_message}")
        await asyncio.sleep(5)  # Délai circuit breaker
        return {"status": "circuit_break_completed"}


class GracefulDegradationStrategy(IRecoveryStrategy):
    """Stratégie : Dégradation gracieuse"""

    async def execute(self, error_context: ErrorContext) -> dict[str, Any]:
        logger.info(f"📉 Dégradation gracieuse pour: {error_context.error_message}")
        await asyncio.sleep(2)
        return {"status": "degradation_completed", "mode": "graceful"}


class SystemRestartStrategy(IRecoveryStrategy):
    """Stratégie : Redémarrage système"""

    async def execute(self, error_context: ErrorContext) -> dict[str, Any]:
        logger.info(f"🔄 Redémarrage système pour: {error_context.error_message}")
        await asyncio.sleep(10)  # Simuler redémarrage
        return {"status": "system_restart_completed"}


class ReconnectStrategy(IRecoveryStrategy):
    """Stratégie : Reconnexion"""

    async def execute(self, error_context: ErrorContext) -> dict[str, Any]:
        logger.info(f"🔗 Reconnexion pour: {error_context.error_message}")
        await asyncio.sleep(2)  # Simuler reconnexion
        return {"status": "reconnect_completed"}


class RestoreStateStrategy(IRecoveryStrategy):
    """Stratégie : Restauration d'état"""

    async def execute(self, error_context: ErrorContext) -> dict[str, Any]:
        logger.info(f"💾 Restauration d'état pour: {error_context.error_message}")
        await asyncio.sleep(3)  # Simuler restauration
        return {"status": "state_restored"}


# ============================================================================
# FACTORY PATTERN (DIP)
# ============================================================================


class RecoveryStrategyFactory:
    """Factory pour créer les stratégies de récupération (DIP)"""

    _strategies = {
        RecoveryStrategy.IMMEDIATE_RETRY: ImmediateRetryStrategy,
        RecoveryStrategy.EXPONENTIAL_BACKOFF: ExponentialBackoffStrategy,
        RecoveryStrategy.CIRCUIT_BREAK: CircuitBreakStrategy,
        RecoveryStrategy.GRACEFUL_DEGRADATION: GracefulDegradationStrategy,
        RecoveryStrategy.SYSTEM_RESTART: SystemRestartStrategy,
        RecoveryStrategy.RECONNECT: ReconnectStrategy,
        RecoveryStrategy.RESTORE_STATE: RestoreStateStrategy,
    }

    @classmethod
    def create_strategy(cls, strategy_type: RecoveryStrategy) -> IRecoveryStrategy:
        """Crée une stratégie de récupération"""
        strategy_class = cls._strategies.get(strategy_type)
        if not strategy_class:
            raise ValueError(f"Stratégie inconnue: {strategy_type}")
        return strategy_class()

    @classmethod
    def register_strategy(
        cls, strategy_type: RecoveryStrategy, strategy_class: type[IRecoveryStrategy]
    ) -> None:
        """Enregistre une nouvelle stratégie (OCP)"""
        cls._strategies[strategy_type] = strategy_class


# ============================================================================
# SYSTÈME PRINCIPAL
# ============================================================================


class ErrorRecoverySystem:
    """
    Système central de récupération d'erreurs consolidé SOLID

    Architecture :
    - Classification automatique des erreurs
    - Stratégies de récupération configurables
    - Métriques temps réel
    - Factory pattern pour l'extensibilité
    """

    def __init__(self) -> None:
        self.active_errors: dict[str, list[ModuleError]] = {}
        self.recovery_history: list[RecoveryResult] = []
        self.is_running = False
        self.max_retries = 3

        # Métriques
        self.metrics: RecoveryMetrics = {
            "total_errors": 0,
            "successful_recoveries": 0,
            "failed_recoveries": 0,
            "contradiction_count": 0,
            "last_error_time": None,
        }

        # Configuration des stratégies par type d'erreur
        self.error_strategies = self._load_error_strategies()

        logger.info("🔄 ErrorRecoverySystem initialisé")

    def _load_error_strategies(self) -> dict[str, dict]:
        """Charge la configuration des stratégies d'erreur"""
        return {
            "connection_lost": {
                "severity": ErrorSeverity.MEDIUM,
                "strategy": RecoveryStrategy.RECONNECT,
                "max_attempts": 3,
            },
            "state_corrupted": {
                "severity": ErrorSeverity.HIGH,
                "strategy": RecoveryStrategy.RESTORE_STATE,
                "max_attempts": 2,
            },
            "deadlock": {
                "severity": ErrorSeverity.CRITICAL,
                "strategy": RecoveryStrategy.SYSTEM_RESTART,
                "max_attempts": 1,
            },
            "timeout": {
                "severity": ErrorSeverity.MEDIUM,
                "strategy": RecoveryStrategy.EXPONENTIAL_BACKOFF,
                "max_attempts": 3,
            },
            "memory": {
                "severity": ErrorSeverity.HIGH,
                "strategy": RecoveryStrategy.GRACEFUL_DEGRADATION,
                "max_attempts": 2,
            },
            "contradiction": {
                "severity": ErrorSeverity.MEDIUM,
                "strategy": RecoveryStrategy.CIRCUIT_BREAK,
                "max_attempts": 2,
            },
        }

    async def register_error(self, error: ModuleError) -> dict:
        """Enregistre une nouvelle erreur"""
        if error.module_name not in self.active_errors:
            self.active_errors[error.module_name] = []

        self.active_errors[error.module_name].append(error)
        self.metrics["total_errors"] += 1
        self.metrics["last_error_time"] = datetime.now().isoformat()

        # Déclencher récupération automatique
        action = self._plan_recovery_action(error)
        if action:
            result = await self.execute_recovery(action)
            return {
                "status": "recovery_attempted",
                "success": result.success,
                "action": action.action_type,
            }

        return {"status": "error_registered", "pending_recovery": True}

    def _plan_recovery_action(self, error: ModuleError) -> RecoveryAction | None:
        """Planifie une action de récupération"""
        module_errors = self.active_errors.get(error.module_name, [])

        # Utiliser la configuration des stratégies
        strategy_config = self.error_strategies.get(
            error.error_type,
            {
                "strategy": RecoveryStrategy.IMMEDIATE_RETRY,
                "max_attempts": 3,
            },
        )

        # Vérifier le nombre de tentatives
        if len(module_errors) >= strategy_config["max_attempts"]:
            return RecoveryAction(
                module_name=error.module_name,
                action_type="restart",
                parameters={"clean": True},
                priority=3,
            )

        # Créer l'action selon la stratégie
        return RecoveryAction(
            module_name=error.module_name,
            action_type=strategy_config["strategy"].value,
            parameters={},
            priority=2,
        )

    async def execute_recovery(self, action: RecoveryAction) -> RecoveryResult:
        """Exécute une action de récupération"""
        logger.info(f"🔄 Exécution récupération: {action.module_name} - {action.action_type}")

        try:
            # Créer le contexte d'erreur
            error_context = ErrorContext(
                error_type=ErrorType.UNKNOWN,
                error_message=f"Recovery action: {action.action_type}",
                max_retries=self.max_retries,
            )

            # Obtenir la stratégie via factory
            strategy_type = RecoveryStrategy(action.action_type)
            strategy = RecoveryStrategyFactory.create_strategy(strategy_type)

            # Exécuter la stratégie
            result = await strategy.execute(error_context)

            success = result.get("status", "").endswith("_completed")

            # Créer le résultat
            recovery_result = RecoveryResult(
                success=success,
                action=action,
                error_fixed=success,
                new_state="recovered" if success else "failed",
            )

            # Mettre à jour métriques
            if success:
                self.metrics["successful_recoveries"] += 1
                self.active_errors[action.module_name] = []
            else:
                self.metrics["failed_recoveries"] += 1

            # Mettre à jour historique
            self.recovery_history.append(recovery_result)

            return recovery_result

        except Exception as e:
            logger.error(f"❌ Erreur récupération: {e}")
            self.metrics["failed_recoveries"] += 1

            return RecoveryResult(
                success=False,
                action=action,
                error_fixed=False,
                new_state="error",
            )

    async def handle_error(self, error_type: ErrorType, error_message: str) -> dict[str, Any]:
        """Gère une erreur avec le nouveau système"""
        error_context = ErrorContext(error_type, error_message)

        # Obtenir la stratégie appropriée
        strategy_config = self.error_strategies.get(
            error_type.value,
            {
                "strategy": RecoveryStrategy.IMMEDIATE_RETRY,
            },
        )

        strategy = RecoveryStrategyFactory.create_strategy(strategy_config["strategy"])
        result = await strategy.execute(error_context)

        return result

    def handle_contradiction(self, zeroia_state: str, reflexia_state: str) -> None:
        """Gère les contradictions entre modules"""
        self.metrics["contradiction_count"] += 1
        logger.warning(
            f"⚠️ Contradiction détectée: ZeroIA={zeroia_state}, ReflexIA={reflexia_state}"
        )

    async def run_recovery_loop(self):
        """Boucle principale de récupération"""
        self.is_running = True
        logger.info("💥 Démarrage boucle de récupération")

        while self.is_running:
            try:
                # Vérifier erreurs actives
                for _module_name, errors in self.active_errors.items():
                    if errors:
                        action = self._plan_recovery_action(errors[-1])
                        if action:
                            await self.execute_recovery(action)

                await asyncio.sleep(10)  # Intervalle de vérification

            except Exception as e:
                logger.error(f"❌ Erreur boucle récupération: {e}")
                await asyncio.sleep(5)

    def get_recovery_status(self) -> dict[str, Any]:
        """Retourne le statut du système de récupération"""
        return {
            "is_running": self.is_running,
            "active_errors": len(self.active_errors),
            "recovery_history": len(self.recovery_history),
            "metrics": self.metrics,
        }

    async def health_check(self) -> dict[str, Any]:
        """Health check du système"""
        return {
            "status": "healthy" if self.is_running else "stopped",
            "active_errors_count": sum(len(errors) for errors in self.active_errors.values()),
            "recovery_success_rate": (
                self.metrics["successful_recoveries"] / max(self.metrics["total_errors"], 1)
            ),
            "last_error_time": self.metrics["last_error_time"],
        }


# ============================================================================
# FACTORY FUNCTION
# ============================================================================


def create_error_recovery_system() -> ErrorRecoverySystem:
    """Factory function pour créer le système de récupération"""
    return ErrorRecoverySystem()
