#!/usr/bin/env python3
# 🧪 tests/unit/zeroia/event_store/test_analytics.py
# Tests pour les analytics et anomalies de l'Event Store ZeroIA

import tempfile

import pytest

from modules.zeroia.event_store import EventStore, EventType


@pytest.fixture
def temp_event_store():
    """Event store temporaire pour les tests"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield EventStore(cache_dir=f"{temp_dir}/test_events", size_limit=10_000_000)


def test_get_decision_history(temp_event_store):
    """🧪 Test récupération historique des décisions"""
    decisions = ["monitor", "reduce_load", "normal", "emergency_shutdown"]
    for decision in decisions:
        temp_event_store.add_event(
            EventType.DECISION_MADE, {"decision": decision, "confidence": 0.8}
        )
    temp_event_store.add_event(EventType.CIRCUIT_SUCCESS, {"state": "closed"})
    temp_event_store.add_event(EventType.SYSTEM_ERROR, {"error": "test"})
    history = temp_event_store.get_decision_history()
    assert len(history) == 4
    assert all(event.event_type == EventType.DECISION_MADE for event in history)
    assert history[0].data["decision"] == "emergency_shutdown"


def test_get_system_health_events(temp_event_store):
    """🧪 Test récupération événements de santé système"""
    temp_event_store.add_event(EventType.CIRCUIT_FAILURE, {"error": "overload"})
    temp_event_store.add_event(EventType.SYSTEM_ERROR, {"error": "critical error"})
    temp_event_store.add_event(
        EventType.STATE_CHANGE, {"old_state": "closed", "new_state": "open"}
    )
    temp_event_store.add_event(EventType.CALL_BLOCKED, {"reason": "circuit open"})
    temp_event_store.add_event(EventType.DECISION_MADE, {"decision": "monitor"})
    temp_event_store.add_event(EventType.CIRCUIT_SUCCESS, {"state": "closed"})
    health_events = temp_event_store.get_system_health_events()
    assert len(health_events) == 4
    health_types = {event.event_type for event in health_events}
    expected_types = {
        EventType.CIRCUIT_FAILURE,
        EventType.SYSTEM_ERROR,
        EventType.STATE_CHANGE,
        EventType.CALL_BLOCKED,
    }
    assert health_types == expected_types


def test_detect_anomalies(temp_event_store):
    """🧪 Test détection d'anomalies"""
    for i in range(7):
        temp_event_store.add_event(EventType.CIRCUIT_FAILURE, {"error": f"failure_{i}"})
    for i in range(3):
        temp_event_store.add_event(
            EventType.SYSTEM_ERROR, {"error": f"system_error_{i}"}
        )
    anomalies = temp_event_store.detect_anomalies(window_minutes=60)
    assert anomalies["total_events"] == 10
    assert len(anomalies["anomalies"]) >= 2
    failure_anomaly = next(
        (a for a in anomalies["anomalies"] if a["type"] == "high_failure_rate"), None
    )
    assert failure_anomaly is not None
    assert failure_anomaly["severity"] == "high"
    assert failure_anomaly["count"] == 7
    error_anomaly = next(
        (a for a in anomalies["anomalies"] if a["type"] == "system_errors"), None
    )
    assert error_anomaly is not None
    assert error_anomaly["severity"] == "critical"


def test_get_analytics(temp_event_store):
    """🧪 Test génération d'analytics"""
    temp_event_store.add_event(
        EventType.DECISION_MADE, {"decision": "monitor"}, module="zeroia"
    )
    temp_event_store.add_event(
        EventType.DECISION_MADE, {"decision": "analyze"}, module="reflexia"
    )
    temp_event_store.add_event(
        EventType.CIRCUIT_SUCCESS, {"state": "closed"}, module="zeroia"
    )
    temp_event_store.add_event(
        EventType.CIRCUIT_FAILURE, {"error": "test"}, module="zeroia"
    )
    analytics = temp_event_store.get_analytics()
    assert analytics["total_events"] == 4
    assert analytics["recent_events_analyzed"] == 4
    assert analytics["events_by_type"]["decision_made"] == 2
    assert analytics["events_by_type"]["circuit_success"] == 1
    assert analytics["events_by_type"]["circuit_failure"] == 1
    assert analytics["events_by_module"]["zeroia"] == 3
    assert analytics["events_by_module"]["reflexia"] == 1
    assert "cache_info" in analytics
