#!/usr/bin/env python3
# 🧪 tests/unit/zeroia/event_store/test_basic.py
# Tests de base pour l'Event Store ZeroIA

import tempfile

import pytest

from modules.zeroia.event_store import EventStore, EventType


@pytest.fixture
def temp_event_store():
    """Event store temporaire pour les tests"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield EventStore(cache_dir=f"{temp_dir}/test_events", size_limit=10_000_000)


def test_event_store_initialization(temp_event_store):
    """🧪 Test initialisation Event Store"""
    assert temp_event_store.event_counter == 0
    # Le cache_dir peut ne pas exister immédiatement, vérifier seulement qu'il est défini
    assert temp_event_store.cache_dir is not None


def test_add_event(temp_event_store):
    """🧪 Test ajout d'événement"""
    event_id = temp_event_store.add_event(
        EventType.DECISION_MADE,
        {"decision": "monitor", "confidence": 0.8, "cpu": 75},
        module="zeroia",
    )
    assert event_id.startswith("zeroia_decision_made_")
    assert temp_event_store.event_counter == 1
    event = temp_event_store.get_event(event_id)
    assert event is not None
    assert event.event_type == EventType.DECISION_MADE
    assert event.module == "zeroia"
    assert event.data["decision"] == "monitor"
    assert event.data["confidence"] == 0.8


def test_get_event_by_id(temp_event_store):
    """🧪 Test récupération événement par ID"""
    event_id = temp_event_store.add_event(
        EventType.CIRCUIT_SUCCESS, {"state": "closed", "success_rate": 0.95}
    )
    event = temp_event_store.get_event(event_id)
    assert event is not None
    assert event.id == event_id
    assert event.event_type == EventType.CIRCUIT_SUCCESS
    assert event.data["success_rate"] == 0.95


def test_get_events_by_type(temp_event_store):
    """🧪 Test récupération événements par type"""
    temp_event_store.add_event(EventType.DECISION_MADE, {"decision": "monitor"})
    temp_event_store.add_event(EventType.CIRCUIT_SUCCESS, {"state": "closed"})
    temp_event_store.add_event(EventType.DECISION_MADE, {"decision": "reduce_load"})
    temp_event_store.add_event(EventType.SYSTEM_ERROR, {"error": "test error"})
    decisions = temp_event_store.get_events_by_type(EventType.DECISION_MADE)
    assert len(decisions) == 2
    assert all(event.event_type == EventType.DECISION_MADE for event in decisions)
    assert decisions[0].data["decision"] == "reduce_load"
    assert decisions[1].data["decision"] == "monitor"


def test_get_events_by_module(temp_event_store):
    """🧪 Test récupération événements par module"""
    temp_event_store.add_event(EventType.DECISION_MADE, {"decision": "monitor"}, module="zeroia")
    temp_event_store.add_event(EventType.DECISION_MADE, {"decision": "analyze"}, module="reflexia")
    temp_event_store.add_event(EventType.CIRCUIT_SUCCESS, {"state": "closed"}, module="zeroia")
    zeroia_events = temp_event_store.get_events_by_module("zeroia")
    assert len(zeroia_events) == 2
    assert all(event.module == "zeroia" for event in zeroia_events)


def test_get_recent_events(temp_event_store):
    """🧪 Test récupération événements récents"""
    for i in range(5):
        temp_event_store.add_event(
            EventType.DECISION_MADE, {"decision": f"decision_{i}"}, module="zeroia"
        )
    recent_events = temp_event_store.get_recent_events(limit=3)
    assert len(recent_events) == 3
    timestamps = [event.timestamp for event in recent_events]
    assert timestamps == sorted(timestamps, reverse=True)
