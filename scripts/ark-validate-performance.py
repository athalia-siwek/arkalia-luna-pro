#!/usr/bin/env python3
# 🧪 scripts/ark-validate-performance.py
# Validation rapide des composants performance

"""
Script de validation rapide des performances Arkalia-LUNA

Tests légers pour vérifier que les composants clés fonctionnent
avant de lancer la suite complète de benchmarks.
"""

import sys
import time
from pathlib import Path

# Ajouter le chemin des modules
sys.path.insert(0, str(Path(__file__).parent.parent))

# Imports des modules pour éviter les erreurs de type checking
try:
    from modules.zeroia.circuit_breaker import CircuitBreaker
    from modules.zeroia.event_store import EventStore, EventType
except ImportError:
    # Les erreurs d'import seront gérées par test_imports()
    pass


def test_imports():
    """Test d'importation des modules critiques"""
    print("🔍 Test des imports...")

    try:
        # Vérifier que les imports globaux ont fonctionné
        assert "create_default_context_enhanced" in globals()
        assert "CircuitBreaker" in globals()
        assert "EventStore" in globals()
        assert "EventType" in globals()
        assert "psutil" in globals()
        print("✅ Tous les imports OK")
        return True
    except (ImportError, AssertionError) as e:
        print(f"❌ Erreur d'import : {e}")
        # Tentative de réimport en cas d'échec
        try:
            import psutil  # noqa: F401

            from modules.zeroia.circuit_breaker import CircuitBreaker  # noqa: F401
            from modules.zeroia.event_store import EventStore, EventType  # noqa: F401
            from modules.zeroia.reason_loop_enhanced import (  # noqa: F401
                create_default_context_enhanced,
            )

            print("✅ Réimport réussi")
            return True
        except ImportError as e2:
            print(f"❌ Échec du réimport : {e2}")
            return False


def test_circuit_breaker_basic():
    """Test basique du Circuit Breaker"""
    print("⚡ Test Circuit Breaker...")

    try:
        circuit = CircuitBreaker(failure_threshold=3, recovery_timeout=30)

        # Test fonction simple
        def simple_func() -> None:
            return "success"

        start = time.perf_counter()
        result = circuit.call(simple_func)
        end = time.perf_counter()

        latency_ms = (end - start) * 1000

        assert result == "success"
        assert latency_ms < 50  # Seuil généreux pour validation

        print(f"✅ Circuit Breaker OK ({latency_ms:.2f}ms)")
        return True

    except Exception as e:
        print(f"❌ Circuit Breaker échec : {e}")
        return False


def test_event_store_basic():
    """Test basique de l'Event Store"""
    print("💾 Test Event Store...")

    try:
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            event_store = EventStore(cache_dir=f"{temp_dir}/test_events")

            start = time.perf_counter()

            event_id = event_store.add_event(
                EventType.DECISION_MADE,
                {"decision": "test", "confidence": 0.9},
                module="validation_test",
            )

            end = time.perf_counter()

            latency_ms = (end - start) * 1000

            assert event_id is not None
            assert latency_ms < 100  # Seuil généreux pour validation

            # Vérifier récupération
            event = event_store.get_event(event_id)
            assert event is not None
            assert event.data["decision"] == "test"

            print(f"✅ Event Store OK ({latency_ms:.2f}ms)")
            return True

    except Exception as e:
        print(f"❌ Event Store échec : {e}")
        return False


def test_zeroia_context():
    """Test création contexte ZeroIA"""
    print("🧠 Test contexte ZeroIA...")

    try:
        from modules.zeroia.reason_loop_enhanced import create_default_context_enhanced

        start = time.perf_counter()
        context = create_default_context_enhanced()
        end = time.perf_counter()

        latency_ms = (end - start) * 1000

        assert context is not None
        assert isinstance(context, dict)
        assert "system" in context

        print(f"✅ Contexte ZeroIA OK ({latency_ms:.2f}ms)")
        return True

    except Exception as e:
        print(f"❌ Contexte ZeroIA échec : {e}")
        return False


def test_system_resources():
    """Test disponibilité des ressources système"""
    print("💻 Test ressources système...")

    try:
        import psutil

        # Mémoire disponible
        memory = psutil.virtual_memory()
        memory_available_gb = memory.available / (1024**3)

        # CPU
        cpu_percent = psutil.cpu_percent(interval=0.1)

        # Disque
        disk = psutil.disk_usage("/")
        disk_free_gb = disk.free / (1024**3)

        print(f"📊 Mémoire libre : {memory_available_gb:.1f} GB")
        print(f"📊 CPU usage : {cpu_percent:.1f}%")
        print(f"📊 Disque libre : {disk_free_gb:.1f} GB")

        # Vérifications minimales
        assert memory_available_gb > 0.5, "Mémoire insuffisante"
        assert cpu_percent < 95, "CPU surchargé"
        assert disk_free_gb > 1.0, "Disque plein"

        print("✅ Ressources système OK")
        return True

    except Exception as e:
        print(f"❌ Ressources système : {e}")
        return False


def main():
    """Validation complète"""
    print("🚀 VALIDATION PERFORMANCE ARKALIA-LUNA")
    print("=" * 50)

    tests = [
        ("Imports", test_imports),
        ("Circuit Breaker", test_circuit_breaker_basic),
        ("Event Store", test_event_store_basic),
        ("Contexte ZeroIA", test_zeroia_context),
        ("Ressources système", test_system_resources),
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}...")
        success = test_func()
        results.append((test_name, success))

    print("\n" + "=" * 50)
    print("📊 RÉSULTATS VALIDATION")

    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1

    print(f"\n🎯 Score : {passed}/{len(tests)} tests réussis")

    if passed == len(tests):
        print("✅ Système prêt pour les benchmarks performance !")
        return True
    else:
        print("⚠️ Certains composants ont des problèmes")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
