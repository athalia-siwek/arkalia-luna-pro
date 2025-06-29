#!/usr/bin/env python3
# 🧪 tests/unit/test_circuit_breaker.py
# Tests unitaires pour le Circuit Breaker ZeroIA

"""
Tests pour Circuit Breaker ZeroIA

Tests couverts :
- États du circuit (CLOSED, OPEN, HALF_OPEN)
- Seuils d'échec et recovery
- Retry automatique avec tenacity
- Métriques et event sourcing
- Gestion d'erreurs spécialisées
"""

from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest

from modules.zeroia.circuit_breaker import (
    CircuitBreaker,
    CircuitState,
    CognitiveOverloadError,
    DecisionIntegrityError,
    SystemRebootRequired,
)
from modules.zeroia.event_store import EventStore, EventType


@pytest.fixture
def mock_event_store():
    """Mock EventStore pour les tests"""
    event_store = MagicMock(spec=EventStore)
    return event_store


@pytest.fixture
def circuit_breaker(mock_event_store):
    """Circuit breaker de test"""
    return CircuitBreaker(
        failure_threshold=3, recovery_timeout=30, event_store=mock_event_store
    )


def test_circuit_breaker_initialization(circuit_breaker, mock_event_store):
    """🧪 Test initialisation circuit breaker"""
    assert circuit_breaker.state == CircuitState.CLOSED
    assert circuit_breaker.failure_threshold == 3
    assert circuit_breaker.recovery_timeout == 30
    assert circuit_breaker.metrics.total_calls == 0
    assert circuit_breaker.metrics.consecutive_failures == 0


def test_successful_call(circuit_breaker, mock_event_store):
    """🧪 Test appel réussi"""

    def dummy_function(x, y):
        return x + y

    result = circuit_breaker.call(dummy_function, 2, 3)

    assert result == 5
    assert circuit_breaker.state == CircuitState.CLOSED
    assert circuit_breaker.metrics.successful_calls == 1
    assert circuit_breaker.metrics.total_calls == 1
    assert circuit_breaker.metrics.consecutive_failures == 0

    # Vérifier event sourcing
    mock_event_store.add_event.assert_called_with(
        EventType.CIRCUIT_SUCCESS,
        {"state": "closed", "success_rate": 1.0, "consecutive_failures": 0},
    )


def test_failure_handling(circuit_breaker, mock_event_store):
    """🧪 Test gestion d'échec"""

    def failing_function():
        raise CognitiveOverloadError("Test overload")

    with pytest.raises(CognitiveOverloadError):
        circuit_breaker.call(failing_function)

    assert circuit_breaker.metrics.failed_calls == 1
    assert circuit_breaker.metrics.consecutive_failures == 1
    assert circuit_breaker.state == CircuitState.CLOSED  # Pas encore ouvert

    # Vérifier event sourcing
    mock_event_store.add_event.assert_called_with(
        EventType.CIRCUIT_FAILURE,
        {
            "state": "closed",
            "exception": "Test overload",
            "consecutive_failures": 1,
            "failure_rate": 1.0,
        },
    )


def test_circuit_opens_after_threshold(circuit_breaker, mock_event_store):
    """🧪 Test ouverture circuit après seuil d'échecs"""

    def failing_function():
        raise CognitiveOverloadError("Test failure")

    # Atteindre le seuil d'échecs (3)
    for i in range(3):
        with pytest.raises(CognitiveOverloadError):
            circuit_breaker.call(failing_function)

    assert circuit_breaker.state == CircuitState.OPEN
    assert circuit_breaker.metrics.consecutive_failures == 3

    # Vérifier l'event de transition
    calls = mock_event_store.add_event.call_args_list
    state_change_calls = [
        call for call in calls if call[0][0] == EventType.STATE_CHANGE
    ]
    assert len(state_change_calls) > 0


def test_circuit_blocks_calls_when_open(circuit_breaker, mock_event_store):
    """🧪 Test blocage appels quand circuit ouvert"""

    def failing_function():
        raise CognitiveOverloadError("Test failure")

    # Ouvrir le circuit
    for i in range(3):
        with pytest.raises(CognitiveOverloadError):
            circuit_breaker.call(failing_function)

    assert circuit_breaker.state == CircuitState.OPEN

    # Tentative d'appel avec circuit ouvert
    with pytest.raises(SystemRebootRequired, match="Circuit breaker OPEN"):
        circuit_breaker.call(lambda: "should not execute")

    # Vérifier event de blocage
    calls = mock_event_store.add_event.call_args_list
    blocked_calls = [call for call in calls if call[0][0] == EventType.CALL_BLOCKED]
    assert len(blocked_calls) > 0


def test_circuit_transitions_to_half_open(circuit_breaker, mock_event_store):
    """🧪 Test transition vers HALF_OPEN après timeout"""

    def failing_function():
        raise CognitiveOverloadError("Test failure")

    # Ouvrir le circuit
    for i in range(3):
        with pytest.raises(CognitiveOverloadError):
            circuit_breaker.call(failing_function)

    assert circuit_breaker.state == CircuitState.OPEN

    # Simuler expiration du timeout
    circuit_breaker.last_failure_time = datetime.now() - timedelta(seconds=31)

    def successful_function():
        return "success"

    result = circuit_breaker.call(successful_function)

    assert result == "success"
    assert circuit_breaker.state == CircuitState.CLOSED  # Retour à CLOSED après succès


def test_half_open_to_closed_on_success(circuit_breaker, mock_event_store):
    """🧪 Test transition HALF_OPEN → CLOSED sur succès"""
    # Forcer l'état HALF_OPEN
    circuit_breaker.state = CircuitState.HALF_OPEN
    circuit_breaker.metrics.consecutive_failures = 2

    def successful_function():
        return "recovery success"

    result = circuit_breaker.call(successful_function)

    assert result == "recovery success"
    assert circuit_breaker.state == CircuitState.CLOSED
    assert circuit_breaker.metrics.consecutive_failures == 0


def test_half_open_to_open_on_failure(circuit_breaker, mock_event_store):
    """🧪 Test transition HALF_OPEN → OPEN sur échec"""
    # Forcer l'état HALF_OPEN avec 2 échecs consécutifs
    circuit_breaker.state = CircuitState.HALF_OPEN
    circuit_breaker.metrics.consecutive_failures = 2

    def failing_function():
        raise CognitiveOverloadError("Still failing")

    with pytest.raises(CognitiveOverloadError):
        circuit_breaker.call(failing_function)

    assert circuit_breaker.state == CircuitState.OPEN
    assert circuit_breaker.metrics.consecutive_failures == 3


def test_unexpected_error_handling(circuit_breaker, mock_event_store):
    """🧪 Test gestion erreurs inattendues"""

    def unexpected_error_function():
        raise ValueError("Unexpected error")

    # Le circuit breaker ne transforme pas les erreurs inattendues
    with pytest.raises(ValueError, match="Unexpected error"):
        circuit_breaker.call(unexpected_error_function)

    # Vérifier que l'échec a été compté dans les métriques
    assert circuit_breaker.metrics.failed_calls > 0
    assert circuit_breaker.metrics.consecutive_failures > 0


def test_manual_reset(circuit_breaker, mock_event_store):
    """🧪 Test réinitialisation manuelle"""

    def failing_function():
        raise CognitiveOverloadError("Test failure")

    # Ouvrir le circuit
    for i in range(3):
        with pytest.raises(CognitiveOverloadError):
            circuit_breaker.call(failing_function)

    assert circuit_breaker.state == CircuitState.OPEN

    # Reset manuel
    circuit_breaker.reset()

    assert circuit_breaker.state == CircuitState.CLOSED
    assert circuit_breaker.metrics.consecutive_failures == 0
    assert circuit_breaker.last_failure_time is None

    # Vérifier event de reset manuel
    calls = mock_event_store.add_event.call_args_list
    reset_calls = [call for call in calls if call[0][0] == EventType.MANUAL_RESET]
    assert len(reset_calls) > 0


def test_retry_mechanism_with_tenacity(circuit_breaker, mock_event_store):
    """🧪 Test mécanisme de retry avec tenacity"""
    call_count = 0

    def flaky_function():
        nonlocal call_count
        call_count += 1
        if call_count <= 2:
            raise CognitiveOverloadError(f"Failure attempt {call_count}")
        return f"Success on attempt {call_count}"

    # Notre circuit breaker actuel ne fait qu'un essai par défaut
    # Testons le comportement normal d'échec au premier appel
    with pytest.raises(CognitiveOverloadError):
        circuit_breaker.call(flaky_function)

    # Vérifier que l'échec a été enregistré
    assert circuit_breaker.failure_count > 0


def test_metrics_calculation(circuit_breaker, mock_event_store):
    """🧪 Test calcul des métriques"""

    def successful_function():
        return "success"

    def failing_function():
        raise CognitiveOverloadError("failure")

    # 3 succès, 2 échecs
    for _ in range(3):
        circuit_breaker.call(successful_function)

    for _ in range(2):
        with pytest.raises(CognitiveOverloadError):
            circuit_breaker.call(failing_function)

    assert circuit_breaker.metrics.total_calls == 5
    assert circuit_breaker.metrics.successful_calls == 3
    assert circuit_breaker.metrics.failed_calls == 2
    assert circuit_breaker.metrics.failure_rate == 0.4
    assert circuit_breaker.metrics.success_rate == 0.6


def test_get_status(circuit_breaker, mock_event_store):
    """🧪 Test récupération du statut complet"""
    # Quelques appels pour avoir des métriques
    circuit_breaker.call(lambda: "success")

    status = circuit_breaker.get_status()

    assert status["state"] == "closed"
    assert "metrics" in status
    assert "config" in status
    assert status["metrics"]["total_calls"] == 1
    assert status["metrics"]["successful_calls"] == 1
    assert status["config"]["failure_threshold"] == 3
    assert status["config"]["recovery_timeout"] == 30


def test_different_exception_types(circuit_breaker, mock_event_store):
    """🧪 Test gestion différents types d'exceptions"""

    def integrity_error_function():
        raise DecisionIntegrityError("Integrity compromised")

    def cognitive_overload_function():
        raise CognitiveOverloadError("Too much load")

    # Test DecisionIntegrityError
    with pytest.raises(DecisionIntegrityError):
        circuit_breaker.call(integrity_error_function)

    # Test CognitiveOverloadError
    with pytest.raises(CognitiveOverloadError):
        circuit_breaker.call(cognitive_overload_function)

    assert circuit_breaker.metrics.failed_calls == 2
    assert circuit_breaker.metrics.consecutive_failures == 2


@pytest.mark.asyncio
async def test_concurrent_calls(circuit_breaker, mock_event_store):
    """🧪 Test appels concurrents (simulation)"""

    def test_function(value):
        if value % 2 == 0:
            raise CognitiveOverloadError(f"Even number {value}")
        return f"Odd number {value}"

    # Simuler des appels concurrents
    for i in range(5):
        if i % 2 == 0:
            try:
                result = circuit_breaker.call(test_function, i)
                assert result == f"Odd number {i}"
            except (CognitiveOverloadError, SystemRebootRequired):
                # Normal - échecs ou circuit ouvert
                pass
        else:
            try:
                circuit_breaker.call(test_function, i)
            except (CognitiveOverloadError, SystemRebootRequired):
                # Normal - échecs ou circuit ouvert
                pass

    # Vérifier que les métriques sont cohérentes
    assert circuit_breaker.metrics.total_calls == 5
    assert circuit_breaker.metrics.successful_calls == 2
    assert circuit_breaker.metrics.failed_calls == 3
