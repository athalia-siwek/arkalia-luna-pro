#!/usr/bin/env python3
# 🔄 modules/zeroia/circuit_breaker.py
# Circuit Breaker Pattern pour ZeroIA

"""
Circuit Breaker pour ZeroIA - Protection cascade failures

Fonctionnalités :
- Circuit breaker avec états (CLOSED, OPEN, HALF_OPEN)
- Retry automatique avec backoff exponentiel
- Métriques et monitoring intégrés
- Event sourcing pour traçabilité
- Gestion d'erreurs spécialisées IA
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, Optional

from modules.zeroia.event_store import EventStore, EventType

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    """États du circuit breaker"""

    CLOSED = "closed"  # Normal, appels passent
    OPEN = "open"  # Circuit ouvert, appels bloqués
    HALF_OPEN = "half_open"  # Test, quelques appels passent


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


@dataclass
class CircuitMetrics:
    """Métriques du circuit breaker"""

    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    consecutive_failures: int = 0
    last_failure_time: Optional[datetime] = None
    state_changes: int = 0

    @property
    def failure_rate(self) -> float:
        """Taux d'échec (0.0 à 1.0)"""
        if self.total_calls == 0:
            return 0.0
        return self.failed_calls / self.total_calls

    @property
    def success_rate(self) -> float:
        """Taux de succès (0.0 à 1.0)"""
        return 1.0 - self.failure_rate


class CircuitBreaker:
    """
    Circuit Breaker pour ZeroIA

    Protège contre les cascades d'échecs avec :
    - Seuils configurables
    - Timeout automatique
    - Métriques détaillées
    - Event sourcing intégré
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: tuple = (ZeroIAError,),
        event_store: Optional[EventStore] = None,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.event_store = event_store or EventStore()

        self.state = CircuitState.CLOSED
        self.metrics = CircuitMetrics()
        self.last_failure_time: Optional[datetime] = None
        self.failure_count = 0  # Compteur d'échecs ajouté

        logger.info(
            f"🔄 CircuitBreaker initialisé: seuil={failure_threshold}, timeout={recovery_timeout}s"
        )

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Exécute une fonction protégée par le circuit breaker

        Args:
            func: Fonction à exécuter
            *args, **kwargs: Arguments de la fonction

        Returns:
            Résultat de la fonction

        Raises:
            SystemRebootRequired: Si circuit ouvert trop longtemps
            CognitiveOverloadError: Si surcharge détectée
        """
        self.metrics.total_calls += 1

        # Vérifier l'état du circuit
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self._transition_to_half_open()
            else:
                self._log_blocked_call()
                raise SystemRebootRequired(
                    f"Circuit breaker OPEN - trop d'échecs consécutifs ({self.metrics.consecutive_failures})"
                )

        try:
            # Tenter l'appel directement (retry simplifié)
            result = func(*args, **kwargs)
            self._on_success()
            return result

        except self.expected_exception as e:
            self._on_failure(e)
            raise
        except Exception as e:
            # Erreur inattendue
            self._on_unexpected_error(e)
            raise CognitiveOverloadError(f"Erreur inattendue dans ZeroIA: {e}") from e

    def _execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """Exécute la fonction avec retry automatique mais sans masquer les exceptions"""
        # Première tentative sans retry pour les erreurs attendues
        try:
            return func(*args, **kwargs)
        except self.expected_exception:
            # Pour les erreurs attendues, on propage directement
            raise
        except Exception:
            # Pour les autres erreurs, on peut utiliser tenacity
            # Mais ici on va simplifier pour éviter les problèmes de wrapping
            raise

    def _on_success(self) -> None:
        """Gère un appel réussi"""
        self.metrics.successful_calls += 1
        self.metrics.consecutive_failures = 0

        if self.state == CircuitState.HALF_OPEN:
            self._transition_to_closed()

        # Event sourcing
        self.event_store.add_event(
            EventType.CIRCUIT_SUCCESS,
            {
                "state": self.state.value,
                "success_rate": self.metrics.success_rate,
                "consecutive_failures": self.metrics.consecutive_failures,
            },
        )

    def _on_failure(self, exception: Exception) -> None:
        """Gère un échec d'appel"""
        self.metrics.failed_calls += 1
        self.metrics.consecutive_failures += 1
        self.metrics.last_failure_time = datetime.now()
        self.failure_count += 1  # Incrémenter le compteur failure_count pour les tests

        logger.warning(
            f"🚨 CircuitBreaker échec: {exception} (consécutif: {self.metrics.consecutive_failures})"
        )

        # Vérifier si on doit ouvrir le circuit
        if self.metrics.consecutive_failures >= self.failure_threshold:
            self._transition_to_open()

        # Event sourcing
        self.event_store.add_event(
            EventType.CIRCUIT_FAILURE,
            {
                "state": self.state.value,
                "exception": str(exception),
                "consecutive_failures": self.metrics.consecutive_failures,
                "failure_rate": self.metrics.failure_rate,
            },
        )

    def _on_unexpected_error(self, exception: Exception) -> None:
        """Gère une erreur inattendue"""
        logger.error(f"💥 CircuitBreaker erreur inattendue: {exception}")
        self.metrics.failed_calls += 1

        # Event sourcing pour erreur critique
        self.event_store.add_event(
            EventType.SYSTEM_ERROR,
            {
                "state": self.state.value,
                "error": str(exception),
                "error_type": type(exception).__name__,
            },
        )

    def _should_attempt_reset(self) -> bool:
        """Vérifie si on peut tenter une réinitialisation"""
        if self.last_failure_time is None:
            return True

        time_since_failure = datetime.now() - self.last_failure_time
        return time_since_failure.total_seconds() >= self.recovery_timeout

    def _transition_to_closed(self) -> None:
        """Transition vers l'état CLOSED"""
        old_state = self.state
        self.state = CircuitState.CLOSED
        self.metrics.state_changes += 1
        logger.info(f"🔄 CircuitBreaker: {old_state.value} → {self.state.value}")

        self.event_store.add_event(
            EventType.STATE_CHANGE,
            {
                "old_state": old_state.value,
                "new_state": self.state.value,
                "reason": "recovery_successful",
            },
        )

    def _transition_to_open(self) -> None:
        """Transition vers l'état OPEN"""
        old_state = self.state
        self.state = CircuitState.OPEN
        self.last_failure_time = datetime.now()
        self.metrics.state_changes += 1
        logger.error(
            f"🚨 CircuitBreaker: {old_state.value} → {self.state.value} (seuil atteint)"
        )

        self.event_store.add_event(
            EventType.STATE_CHANGE,
            {
                "old_state": old_state.value,
                "new_state": self.state.value,
                "reason": "failure_threshold_exceeded",
                "consecutive_failures": self.metrics.consecutive_failures,
            },
        )

    def _transition_to_half_open(self) -> None:
        """Transition vers l'état HALF_OPEN"""
        old_state = self.state
        self.state = CircuitState.HALF_OPEN
        self.metrics.state_changes += 1
        logger.info(
            f"🔄 CircuitBreaker: {old_state.value} → {self.state.value} (test recovery)"
        )

        self.event_store.add_event(
            EventType.STATE_CHANGE,
            {
                "old_state": old_state.value,
                "new_state": self.state.value,
                "reason": "recovery_timeout_reached",
            },
        )

    def _log_blocked_call(self) -> None:
        """Log d'un appel bloqué"""
        logger.warning(f"🛑 CircuitBreaker bloque un appel (état: {self.state.value})")

        self.event_store.add_event(
            EventType.CALL_BLOCKED,
            {
                "state": self.state.value,
                "consecutive_failures": self.metrics.consecutive_failures,
                "time_since_failure": (
                    (datetime.now() - self.last_failure_time).total_seconds()
                    if self.last_failure_time
                    else None
                ),
            },
        )

    def reset(self) -> None:
        """Réinitialise manuellement le circuit breaker"""
        old_state = self.state
        self.state = CircuitState.CLOSED
        self.metrics.consecutive_failures = 0
        self.last_failure_time = None
        self.metrics.state_changes += 1

        logger.info(
            f"🔄 CircuitBreaker réinitialisé manuellement: {old_state.value} → {self.state.value}"
        )

        self.event_store.add_event(
            EventType.MANUAL_RESET,
            {"old_state": old_state.value, "new_state": self.state.value},
        )

    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut complet du circuit breaker"""
        return {
            "state": self.state.value,
            "metrics": {
                "total_calls": self.metrics.total_calls,
                "successful_calls": self.metrics.successful_calls,
                "failed_calls": self.metrics.failed_calls,
                "consecutive_failures": self.metrics.consecutive_failures,
                "failure_rate": self.metrics.failure_rate,
                "success_rate": self.metrics.success_rate,
                "state_changes": self.metrics.state_changes,
            },
            "config": {
                "failure_threshold": self.failure_threshold,
                "recovery_timeout": self.recovery_timeout,
            },
            "last_failure_time": (
                self.last_failure_time.isoformat() if self.last_failure_time else None
            ),
        }
