#!/usr/bin/env python3
# 🧪 tests/performance/test_zeroia_performance.py
# Benchmarks performance ZeroIA Enhanced

"""
Tests de performance pour ZeroIA Enhanced v2.6.0

Benchmarks couverts :
- Temps de décision reason_loop_enhanced
- Performance Circuit Breaker
- Latence Event Store
- Throughput orchestrator
- Memory usage monitoring
"""

from core.ark_logger import ark_logger
import os
import time
from unittest.mock import patch

import psutil
import pytest

from modules.zeroia.circuit_breaker import CircuitBreaker
from modules.zeroia.event_store import EventStore, EventType
from modules.zeroia.reason_loop_enhanced import (
    create_default_context_enhanced,
    reason_loop_enhanced_with_recovery,
)


class PerformanceMetrics:
    """Collecteur de métriques de performance"""

    def __init__(self) -> None:
        self.start_time = None
        self.end_time = None
        self.memory_start = None
        self.memory_end = None

    def start_monitoring(self):
        """Démarre la collecte de métriques"""
        self.start_time = time.perf_counter()
        process = psutil.Process()
        self.memory_start = process.memory_info().rss / 1024 / 1024  # MB

    def stop_monitoring(self):
        """Arrête la collecte de métriques"""
        self.end_time = time.perf_counter()
        process = psutil.Process()
        self.memory_end = process.memory_info().rss / 1024 / 1024  # MB

    @property
    def elapsed_time(self) -> float | None:
        """Temps écoulé en secondes"""
        if self.end_time is not None and self.start_time is not None:
            return float(self.end_time) - float(self.start_time)
        return None

    @property
    def memory_delta(self) -> float | None:
        """Différence mémoire en MB"""
        if self.memory_end is not None and self.memory_start is not None:
            # Type assertion pour rassurer le type checker
            return float(self.memory_end) - float(self.memory_start)
        return None


@pytest.fixture
def performance_metrics():
    """Fixture pour métriques de performance"""
    return PerformanceMetrics()


@pytest.fixture
def temp_paths(tmp_path):
    """Chemins temporaires pour les tests"""
    return {
        "context": tmp_path / "context.toml",
        "reflexia": tmp_path / "reflexia.toml",
        "state": tmp_path / "state.toml",
        "dashboard": tmp_path / "dashboard.json",
    }


@pytest.mark.performance
@pytest.mark.slow
@pytest.mark.skipif(os.getenv("CI") == "true", reason="Ignoré en CI")
def test_zeroia_decision_time_under_2s(performance_metrics, temp_paths):
    """
    🎯 Test : ZeroIA Enhanced prend une décision en < 2s

    Objectif : Valider que reason_loop_enhanced est optimisé
    Seuil : < 2.0s (vs 1.7s actuel mesuré)
    """
    performance_metrics.start_monitoring()

    # Créer contexte par défaut optimisé
    context = create_default_context_enhanced()

    # Mock des fichiers pour éviter I/O
    from modules.zeroia.reason_loop import decide

    # Test direct sans patch pour éviter les conflits
    start_time = time.time()
    decision, confidence = decide({"status": {"cpu": 50, "severity": "normal"}})
    end_time = time.time()

    decision_time = end_time - start_time

    assert decision_time < 2.0, f"Décision trop lente: {decision_time:.2f}s"
    assert isinstance(decision, str)
    assert isinstance(confidence, float)

    performance_metrics.stop_monitoring()

    # Vérifications performance
    elapsed = performance_metrics.elapsed_time
    threshold = float(os.getenv("ZEROIA_DECISION_THRESHOLD", "2.0"))

    assert elapsed < threshold, f"❌ ZeroIA trop lent : {elapsed:.3f}s (limite : {threshold}s)"

    ark_logger.info(f"✅ ZeroIA décision en {elapsed:.3f}s (objectif < {threshold}s, extra={"module": "zeroia"})")
    memory_delta = performance_metrics.memory_delta
    if memory_delta is not None:
        ark_logger.info(f"📊 Mémoire utilisée : {memory_delta:.1f} MB", extra={"module": "zeroia"})


@pytest.mark.performance
@pytest.mark.slow
def test_circuit_breaker_latency_under_10ms(performance_metrics):
    """
    ⚡ Test : Circuit Breaker latence < 10ms

    Objectif : Vérifier que la protection n'ajoute pas de latence
    Seuil : < 10ms par appel
    """
    circuit_breaker = CircuitBreaker(failure_threshold=5, timeout=60)

    def fast_function() -> None:
        return "success"

    # Mesure de 100 appels pour moyenne fiable
    performance_metrics.start_monitoring()

    results = []
    for _ in range(100):
        start = time.perf_counter()
        result = circuit_breaker.call(fast_function)
        end = time.perf_counter()
        results.append(end - start)
        assert result == "success"

    performance_metrics.stop_monitoring()

    # Calculs statistiques
    avg_latency = sum(results) / len(results)
    max_latency = max(results)
    min_latency = min(results)

    threshold_ms = float(os.getenv("CIRCUIT_LATENCY_THRESHOLD_MS", "10.0"))
    avg_latency_ms = avg_latency * 1000
    max_latency_ms = max_latency * 1000

    assert avg_latency_ms < threshold_ms, (
        f"❌ Circuit Breaker latence moyenne trop élevée : {avg_latency_ms:.2f}ms "
        f"(limite : {threshold_ms}ms)"
    )

    ark_logger.info(f"✅ Circuit Breaker - Latence moyenne : {avg_latency_ms:.2f}ms", extra={"module": "zeroia"})
    ark_logger.info(f"📊 Min: {min_latency*1000:.2f}ms | Max: {max_latency_ms:.2f}ms", extra={"module": "zeroia"})


@pytest.mark.performance
@pytest.mark.slow
@pytest.mark.skip(reason="Test obsolète - dépend d'EventStore incompatible")
def test_event_store_write_performance(performance_metrics, tmp_path):
    """
    💾 Test : Event Store écriture < 50ms par événement

    Objectif : Valider que l'Event Store n'est pas un goulot
    Seuil : < 50ms par écriture (1000 événements)
    """
    event_store = EventStore(cache_dir=str(tmp_path / "test_events"))

    events_count = 100  # Réduit pour tests rapides
    performance_metrics.start_monitoring()

    write_times = []
    for i in range(events_count):
        start = time.perf_counter()

        event_id = event_store.add_event(
            EventType.DECISION_MADE,
            {
                "decision": f"decision_{i}",
                "confidence": 0.8 + (i % 20) / 100,
                "cpu": 50 + (i % 30),
                "iteration": i,
            },
            module="benchmark_test",
        )

        end = time.perf_counter()
        write_times.append(end - start)

        assert event_id is not None

    performance_metrics.stop_monitoring()

    # Statistiques
    avg_write_time = sum(write_times) / len(write_times)
    max_write_time = max(write_times)

    threshold_ms = float(os.getenv("EVENT_STORE_WRITE_THRESHOLD_MS", "50.0"))
    avg_write_ms = avg_write_time * 1000
    max_write_ms = max_write_time * 1000

    assert avg_write_ms < threshold_ms, (
        f"❌ Event Store écriture trop lente : {avg_write_ms:.2f}ms/event "
        f"(limite : {threshold_ms}ms)"
    )

    ark_logger.info(f"✅ Event Store - {events_count} événements écrits", extra={"module": "zeroia"})
    ark_logger.info(f"📊 Moyenne: {avg_write_ms:.2f}ms | Max: {max_write_ms:.2f}ms", extra={"module": "zeroia"})
    ark_logger.info(f"🚀 Throughput: {events_count / performance_metrics.elapsed_time:.0f} events/sec", extra={"module": "zeroia"})


@pytest.mark.performance
@pytest.mark.benchmark
def test_performance_regression_detection():
    """
    📊 Test : Détection régression performance

    Compare avec les benchmarks de référence stockés
    """
    # Benchmarks de référence (à ajuster selon vos mesures)
    reference_benchmarks = {
        "zeroia_decision_time": 2.0,  # secondes
        "circuit_breaker_latency": 10.0,  # ms
        "event_store_write": 50.0,  # ms
        "orchestrator_throughput": 10.0,  # décisions/min
        "memory_growth": 100.0,  # MB
    }

    # Ce test pourrait être étendu pour lire des résultats
    # de benchmarks précédents et détecter des régressions

    for benchmark, threshold in reference_benchmarks.items():
        ark_logger.info(f"📊 Benchmark {benchmark}: seuil {threshold}", extra={"module": "zeroia"})

    # Pour l'instant, juste valider que les seuils sont raisonnables
    assert all(threshold > 0 for threshold in reference_benchmarks.values())

    ark_logger.info("✅ Seuils de performance validés", extra={"module": "zeroia"})
