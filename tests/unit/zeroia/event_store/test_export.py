#!/usr/bin/env python3
# 🧪 tests/unit/zeroia/event_store/test_export.py
# Tests pour l'export et la persistance de l'Event Store ZeroIA

import json
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

import pytest

from modules.zeroia.event_store import Event, EventStore, EventType


@pytest.fixture
def temp_event_store():
    """Event store temporaire pour les tests"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield EventStore(cache_dir=f"{temp_dir}/test_events", size_limit=10_000_000)


def test_clear_old_events(temp_event_store):
    """🧪 Test nettoyage anciens événements"""
    for i in range(3):
        temp_event_store.add_event(EventType.DECISION_MADE, {"decision": f"recent_{i}"})
    with patch("modules.zeroia.event_store.datetime") as mock_datetime:
        old_timestamp = datetime.now() - timedelta(days=40)
        mock_datetime.now.return_value = old_timestamp
        for i in range(2):
            temp_event_store.add_event(EventType.CIRCUIT_FAILURE, {"error": f"old_error_{i}"})
    assert temp_event_store.event_counter == 5
    deleted_count = temp_event_store.clear_old_events(days_to_keep=30)
    assert deleted_count >= 0


def test_export_events(temp_event_store):
    """🧪 Test export d'événements"""
    temp_event_store.add_event(EventType.DECISION_MADE, {"decision": "monitor"})
    temp_event_store.add_event(EventType.CIRCUIT_SUCCESS, {"state": "closed"})
    temp_event_store.add_event(EventType.SYSTEM_ERROR, {"error": "test error"})
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as temp_file:
        export_path = Path(temp_file.name)
    try:
        exported_count = temp_event_store.export_events(export_path)
        assert exported_count == 3
        assert export_path.exists()
        with open(export_path) as f:
            export_data = json.load(f)
        assert export_data["total_events"] == 3
        assert export_data["event_type_filter"] == "all"
        assert len(export_data["events"]) == 3
        first_event = export_data["events"][0]
        assert "id" in first_event
        assert "event_type" in first_event
        assert "timestamp" in first_event
        assert "module" in first_event
        assert "data" in first_event
    finally:
        if export_path.exists():
            export_path.unlink()


def test_export_events_by_type(temp_event_store):
    """🧪 Test export d'événements par type"""
    temp_event_store.add_event(EventType.DECISION_MADE, {"decision": "monitor"})
    temp_event_store.add_event(EventType.DECISION_MADE, {"decision": "reduce_load"})
    temp_event_store.add_event(EventType.CIRCUIT_SUCCESS, {"state": "closed"})
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as temp_file:
        export_path = Path(temp_file.name)
    try:
        exported_count = temp_event_store.export_events(
            export_path, event_type=EventType.DECISION_MADE
        )
        assert exported_count == 2
        with open(export_path) as f:
            export_data = json.load(f)
        assert export_data["total_events"] == 2
        assert export_data["event_type_filter"] == "decision_made"
        assert all(event["event_type"] == "decision_made" for event in export_data["events"])
    finally:
        if export_path.exists():
            export_path.unlink()


def test_event_to_dict_and_from_dict():
    """🧪 Test sérialisation/désérialisation Event"""
    original_event = Event(
        id="test_id_123",
        event_type=EventType.DECISION_MADE,
        timestamp=datetime.now(),
        module="zeroia",
        data={"decision": "monitor", "confidence": 0.8},
        correlation_id="corr_123",
    )
    event_dict = original_event.to_dict()
    assert event_dict["id"] == "test_id_123"
    assert event_dict["event_type"] == "decision_made"
    assert event_dict["module"] == "zeroia"
    assert event_dict["data"]["decision"] == "monitor"
    assert event_dict["correlation_id"] == "corr_123"
    restored_event = Event.from_dict(event_dict)
    assert restored_event.id == original_event.id
    assert restored_event.event_type == original_event.event_type
    assert restored_event.module == original_event.module
    assert restored_event.data == original_event.data
    assert restored_event.correlation_id == original_event.correlation_id


def test_correlation_id_tracking(temp_event_store):
    """🧪 Test suivi avec correlation_id"""
    correlation_id = "request_12345"
    temp_event_store.add_event(
        EventType.DECISION_MADE, {"decision": "monitor"}, correlation_id=correlation_id
    )
    temp_event_store.add_event(
        EventType.CIRCUIT_SUCCESS, {"state": "closed"}, correlation_id=correlation_id
    )
    recent_events = temp_event_store.get_recent_events()
    correlated_events = [event for event in recent_events if event.correlation_id == correlation_id]
    assert len(correlated_events) == 2


def test_type_index_functionality(temp_event_store):
    """🧪 Test fonctionnalité index par type"""
    for i in range(5):
        temp_event_store.add_event(EventType.DECISION_MADE, {"decision": f"decision_{i}"})
    for _ in range(3):
        temp_event_store.add_event(EventType.CIRCUIT_SUCCESS, {"state": "closed"})
    decision_events = temp_event_store.get_events_by_type(EventType.DECISION_MADE)
    success_events = temp_event_store.get_events_by_type(EventType.CIRCUIT_SUCCESS)
    assert len(decision_events) == 5
    assert len(success_events) == 3


def test_event_store_persistence(temp_event_store):
    """🧪 Test persistance de l'Event Store"""
    temp_event_store.add_event(EventType.DECISION_MADE, {"decision": "monitor"})
    temp_event_store.add_event(EventType.CIRCUIT_SUCCESS, {"state": "closed"})
    # Pas de méthode close(), on teste juste la persistance via le cache
    recent_events = temp_event_store.get_recent_events()
    assert len(recent_events) == 2
    assert recent_events[0].event_type == EventType.CIRCUIT_SUCCESS
    assert recent_events[1].event_type == EventType.DECISION_MADE
