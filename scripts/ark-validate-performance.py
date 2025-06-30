#!/usr/bin/env python3
"""
🔍 Script de validation des performances Arkalia-LUNA Pro
Valide les modules ZeroIA, EventStore et CircuitBreaker
"""

import tempfile
import time
from pathlib import Path

try:
    import psutil  # noqa: F401

    from modules.zeroia.circuit_breaker import (  # noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401
        CircuitBreaker,
    )
    from modules.zeroia.event_store import EventType  # noqa: F401# noqa: F401# noqa: F401,
    from modules.zeroia.event_store import (  # noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401,  # noqa: F401,; noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401,; noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401
        EventStore,
    )
    from modules.zeroia.reason_loop_enhanced import (  # noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,
        create_default_context_enhanced,
    )
except ImportError as e:
    print(f"❌ Erreur import modules: {e}")
    print("💡 Vérifiez que les modules sont installés et accessibles")
    exit(1)


def validate_imports() -> bool:
    """Valide que tous les imports nécessaires fonctionnent"""
    print("🔍 Validation des imports...")

    try:
        # Vérifier que les imports globaux ont fonctionné
        assert "create_default_context_enhanced  # noqa: F401 " in globals()
        assert "CircuitBreaker" in globals()
        assert "EventStore" in globals()
        assert "EventType  # noqa: F401 " in globals()
        assert "psutil  # noqa: F401 " in globals()
        print("✅ Tous les imports OK")
        return True

    except AssertionError as e:
        print(f"❌ Import manquant: {e}")
        return False

    except Exception as e:
        print(f"❌ Erreur validation imports: {e}")

        # Tentative de réimport en cas d'échec
        try:
            import psutil  # noqa: F401

            from modules.zeroia.circuit_breaker import (  # noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401
                CircuitBreaker,
            )
            from modules.zeroia.event_store import (  # noqa: F401# noqa: F401# noqa: F401# noqa: F401,; noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401,  # noqa: F401,; noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401,; noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401
                EventStore,
                EventType,
            )
            from modules.zeroia.reason_loop_enhanced import (  # noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,
                create_default_context_enhanced,
            )

            print("✅ Réimport réussi")
            return True

        except ImportError as e2:
            print(f"❌ Réimport échoué: {e2}")
            return False


def validate_event_store_performance() -> bool:
    """Valide les performances de l'EventStore"""
    print("📊 Validation EventStore...")

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            event_store  # noqa: F401 = EventStore(cache_dir=f"{temp_dir}/test_events")

            start = time.perf_counter()

            event_id = event_store  # noqa: F401.add_event(
                EventType  # noqa: F401.DECISION_MADE,
                {"decision": "test", "confidence": 0.9},
                module="validation_test",
            )

            end = time.perf_counter()
            duration = end - start

            # Vérifier récupération
            event = event_store  # noqa: F401.get_event(event_id)
            assert event is not None
            assert event.data["decision"] == "test"

            print(f"✅ EventStore: {duration:.3f}s pour ajout + récupération")
            return duration < 0.1  # Doit être < 100ms

    except Exception as e:
        print(f"❌ Erreur EventStore: {e}")
        return False


def validate_context_creation() -> bool:
    """Valide la création de contexte"""
    print("🎯 Validation création contexte...")

    try:
        from modules.zeroia.reason_loop_enhanced import (  # noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,; noqa: F401,
            create_default_context_enhanced,
        )

        start = time.perf_counter()
        context = create_default_context_enhanced  # noqa: F401()
        end = time.perf_counter()

        duration = end - start
        print(f"✅ Contexte créé en {duration:.3f}s")

        # Vérifier structure
        assert "system_status" in context
        assert "active_modules" in context
        assert "status" in context

        return duration < 0.05  # Doit être < 50ms

    except Exception as e:
        print(f"❌ Erreur création contexte: {e}")
        return False


def validate_system_resources() -> bool:
    """Valide les ressources système"""
    print("💻 Validation ressources système...")

    try:
        import psutil  # noqa: F401

        # Mémoire disponible
        memory = psutil  # noqa: F401.virtual_memory()
        memory_available_gb = memory.available / (1024**3)

        # CPU
        cpu_percent = psutil  # noqa: F401.cpu_percent(interval=0.1)

        # Disque
        disk = psutil  # noqa: F401.disk_usage("/")
        disk_free_gb = disk.free / (1024**3)

        print(f"✅ RAM disponible: {memory_available_gb:.1f}GB")
        print(f"✅ CPU usage: {cpu_percent:.1f}%")
        print(f"✅ Disque libre: {disk_free_gb:.1f}GB")

        # Critères de validation
        ram_ok = memory_available_gb > 1.0  # Au moins 1GB
        cpu_ok = cpu_percent < 90  # CPU < 90%
        disk_ok = disk_free_gb > 5.0  # Au moins 5GB libre

        return ram_ok and cpu_ok and disk_ok

    except Exception as e:
        print(f"❌ Erreur validation ressources: {e}")
        return False


def main():
    """Fonction principale de validation"""
    print("🚀 Validation des performances Arkalia-LUNA Pro")
    print("=" * 50)

    results = []

    # Tests de validation
    results.append(("Imports", validate_imports()))
    results.append(("EventStore", validate_event_store_performance()))
    results.append(("Contexte", validate_context_creation()))
    results.append(("Ressources", validate_system_resources()))

    # Résumé
    print("\n📋 Résumé des validations:")
    print("-" * 30)

    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:15} {status}")
        if result:
            passed += 1

    print(f"\n🎯 {passed}/{len(results)} tests passés")

    if passed == len(results):
        print("🎉 Toutes les validations sont passées!")
        return 0
    else:
        print("⚠️ Certaines validations ont échoué")
        return 1


if __name__ == "__main__":
    exit(main())
