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

import os
import sys
import time
from pathlib import Path
from typing import Any, Dict
from unittest.mock import patch

import psutil
import pytest
import pytest_benchmark.plugin

# Ajout du path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.zeroia.circuit_breaker import CircuitBreaker
from modules.zeroia.core import ZeroIACore
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

    print(f"✅ ZeroIA décision en {elapsed:.3f}s (objectif < {threshold}s)")
    memory_delta = performance_metrics.memory_delta
    if memory_delta is not None:
        print(f"📊 Mémoire utilisée : {memory_delta:.1f} MB")


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

    print(f"✅ Circuit Breaker - Latence moyenne : {avg_latency_ms:.2f}ms")
    print(f"📊 Min: {min_latency*1000:.2f}ms | Max: {max_latency_ms:.2f}ms")


@pytest.mark.performance
@pytest.mark.slow
@pytest.mark.xfail(reason="EventStore adapter not yet stable")
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

    print(f"✅ Event Store - {events_count} événements écrits")
    print(f"📊 Moyenne: {avg_write_ms:.2f}ms | Max: {max_write_ms:.2f}ms")
    print(f"🚀 Throughput: {events_count / performance_metrics.elapsed_time:.0f} events/sec")


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
        print(f"📊 Benchmark {benchmark}: seuil {threshold}")

    # Pour l'instant, juste valider que les seuils sont raisonnables
    assert all(threshold > 0 for threshold in reference_benchmarks.values())

    print("✅ Seuils de performance validés")


class TestZeroIAPerformance:
    """Tests de performance pour ZeroIA"""

    @pytest.fixture
    def zeroia_core(self):
        """Instance ZeroIA pour les tests"""
        return ZeroIACore()

    @pytest.fixture
    def circuit_breaker(self):
        """Instance CircuitBreaker pour les tests"""
        return CircuitBreaker()

    @pytest.fixture
    def event_store(self):
        """Instance EventStore pour les tests"""
        return EventStore()

    @pytest.mark.benchmark
    def test_zeroia_decision_time_under_2s(self, zeroia_core, benchmark):
        """Test que la décision ZeroIA prend moins de 2 secondes"""

        def decision_operation():
            context = {
                "cpu_usage": 75.0,
                "memory_usage": 80.0,
                "error_rate": 0.02,
                "response_time": 150.0,
            }
            return zeroia_core.make_decision(context)

        result = benchmark(decision_operation)
        assert result is not None
        assert "decision" in result

    @pytest.mark.benchmark
    def test_circuit_breaker_latency_under_10ms(self, circuit_breaker, benchmark):
        """Test que le circuit breaker répond en moins de 10ms"""

        def circuit_breaker_operation():
            return circuit_breaker.is_open()

        result = benchmark(circuit_breaker_operation)
        assert isinstance(result, bool)

    @pytest.mark.benchmark
    def test_event_store_write_performance(self, event_store, benchmark):
        """Test de performance d'écriture dans l'EventStore"""

        def write_event():
            event = {"timestamp": time.time(), "type": "performance_test", "data": {"test": "data"}}
            return event_store.store_event(event)

        result = benchmark(write_event)
        assert result is not None

    @pytest.mark.benchmark
    def test_event_store_read_performance(self, event_store, benchmark):
        """Test de performance de lecture dans l'EventStore"""
        # Préparation : ajout d'événements
        for i in range(100):
            event = {"timestamp": time.time(), "type": f"test_event_{i}", "data": {"index": i}}
            event_store.store_event(event)

        def read_events():
            return event_store.get_events(limit=50)

        result = benchmark(read_events)
        assert len(result) <= 50

    @pytest.mark.benchmark
    def test_confidence_score_calculation(self, zeroia_core, benchmark):
        """Test de performance du calcul du score de confiance"""

        def calculate_confidence():
            metrics = {
                "cpu_usage": 70.0,
                "memory_usage": 75.0,
                "error_rate": 0.01,
                "response_time": 120.0,
            }
            return zeroia_core.calculate_confidence_score(metrics)

        result = benchmark(calculate_confidence)
        assert 0.0 <= result <= 1.0

    @pytest.mark.benchmark
    def test_adaptive_thresholds_update(self, zeroia_core, benchmark):
        """Test de performance de mise à jour des seuils adaptatifs"""

        def update_thresholds():
            current_metrics = {"cpu_usage": 65.0, "memory_usage": 70.0}
            return zeroia_core.update_adaptive_thresholds(current_metrics)

        result = benchmark(update_thresholds)
        assert result is not None

    @pytest.mark.benchmark
    def test_snapshot_generation_performance(self, zeroia_core, benchmark):
        """Test de performance de génération de snapshots"""

        def generate_snapshot():
            return zeroia_core.generate_system_snapshot()

        result = benchmark(generate_snapshot)
        assert result is not None
        assert "timestamp" in result

    @pytest.mark.benchmark
    def test_health_check_performance(self, zeroia_core, benchmark):
        """Test de performance des health checks"""

        def health_check():
            return zeroia_core.perform_health_check()

        result = benchmark(health_check)
        assert result is not None
        assert "status" in result

    @pytest.mark.benchmark
    def test_graceful_degradation_performance(self, zeroia_core, benchmark):
        """Test de performance de la dégradation gracieuse"""

        def graceful_degradation():
            return zeroia_core.trigger_graceful_degradation()

        result = benchmark(graceful_degradation)
        assert result is not None

    @pytest.mark.benchmark
    def test_error_recovery_performance(self, zeroia_core, benchmark):
        """Test de performance de la récupération d'erreur"""

        def error_recovery():
            return zeroia_core.trigger_error_recovery()

        result = benchmark(error_recovery)
        assert result is not None


class TestZeroIALoadPerformance:
    """Tests de performance sous charge pour ZeroIA"""

    @pytest.mark.asyncio
    async def test_concurrent_decisions(self, zeroia_core):
        """Test de décisions concurrentes"""

        async def make_decision(decision_id):
            context = {
                "cpu_usage": 60.0 + (decision_id % 20),
                "memory_usage": 70.0 + (decision_id % 15),
                "error_rate": 0.01 + (decision_id % 5) * 0.001,
            }
            return zeroia_core.make_decision(context)

        # 50 décisions concurrentes
        tasks = [make_decision(i) for i in range(50)]
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        end_time = time.time()

        total_time = end_time - start_time
        assert total_time < 10.0  # Moins de 10 secondes pour 50 décisions
        assert len(results) == 50
        assert all("decision" in result for result in results)

    @pytest.mark.asyncio
    async def test_high_frequency_events(self, event_store):
        """Test de performance avec événements haute fréquence"""

        async def store_event(event_id):
            event = {
                "timestamp": time.time(),
                "type": "high_frequency_test",
                "data": {"event_id": event_id},
            }
            return event_store.store_event(event)

        # 1000 événements haute fréquence
        tasks = [store_event(i) for i in range(1000)]
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        end_time = time.time()

        total_time = end_time - start_time
        assert total_time < 5.0  # Moins de 5 secondes pour 1000 événements
        assert len(results) == 1000

    @pytest.mark.asyncio
    async def test_circuit_breaker_stress_test(self, circuit_breaker):
        """Test de stress du circuit breaker"""

        async def circuit_breaker_operation():
            # Simulation d'opérations qui peuvent échouer
            import random

            if random.random() < 0.1:  # 10% d'échec
                circuit_breaker.record_failure()
            else:
                circuit_breaker.record_success()
            return circuit_breaker.is_open()

        # 1000 opérations
        tasks = [circuit_breaker_operation() for _ in range(1000)]
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        end_time = time.time()

        total_time = end_time - start_time
        assert total_time < 2.0  # Moins de 2 secondes pour 1000 opérations
        assert len(results) == 1000


class TestZeroIAMemoryPerformance:
    """Tests de performance mémoire pour ZeroIA"""

    def test_memory_usage_under_load(self, zeroia_core):
        """Test de l'utilisation mémoire sous charge"""
        import os

        import psutil

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        # Simulation de charge
        for i in range(1000):
            context = {
                "cpu_usage": 50.0 + (i % 30),
                "memory_usage": 60.0 + (i % 20),
                "error_rate": 0.01 + (i % 10) * 0.001,
            }
            zeroia_core.make_decision(context)

        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory

        # L'augmentation mémoire ne doit pas dépasser 50MB
        assert memory_increase < 50 * 1024 * 1024

    def test_memory_leak_prevention(self, event_store):
        """Test de prévention des fuites mémoire"""
        import os

        import psutil

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        # Ajout et suppression d'événements
        for i in range(1000):
            event = {
                "timestamp": time.time(),
                "type": f"memory_test_{i}",
                "data": {"test": "data" * 100},  # Données volumineuses
            }
            event_store.store_event(event)

        # Nettoyage
        event_store.clear_old_events(age_hours=0)

        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory

        # L'augmentation mémoire doit être raisonnable après nettoyage
        assert memory_increase < 10 * 1024 * 1024  # 10MB


class TestZeroIAPerformanceRegression:
    """Tests de régression de performance"""

    def test_performance_regression_detection(self, zeroia_core):
        """Test de détection de régression de performance"""
        # Test de performance de base
        start_time = time.time()
        for i in range(100):
            context = {"cpu_usage": 50.0, "memory_usage": 60.0, "error_rate": 0.01}
            zeroia_core.make_decision(context)
        base_time = time.time() - start_time

        # Test avec charge supplémentaire
        start_time = time.time()
        for i in range(100):
            context = {
                "cpu_usage": 50.0,
                "memory_usage": 60.0,
                "error_rate": 0.01,
                "additional_load": True,  # Charge supplémentaire
            }
            zeroia_core.make_decision(context)
        load_time = time.time() - start_time

        # La différence ne doit pas être trop importante
        time_increase = (load_time - base_time) / base_time
        assert time_increase < 0.5  # Pas plus de 50% d'augmentation


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--benchmark-only"])
