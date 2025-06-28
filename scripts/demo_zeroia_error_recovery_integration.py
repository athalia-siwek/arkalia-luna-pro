#!/usr/bin/env python3
"""
🔄 Demo ZeroIA Enhanced + Error Recovery Integration v2.7.0
Démontre l'intégration complète du système Error Recovery
dans la boucle de raisonnement ZeroIA Enhanced.
"""

import logging
import sys
import time
from pathlib import Path

# Ajout du chemin modules
sys.path.insert(0, str(Path(__file__).parent.parent / "modules"))

from zeroia.reason_loop_enhanced import (
    get_circuit_status,
    get_degradation_status,
    get_error_recovery_status,
    get_event_analytics,
    initialize_components_with_recovery,
    reason_loop_enhanced_with_recovery,
)

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/zeroia_error_recovery_demo.log"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


def create_test_context(cpu_usage: float, ram_usage: float) -> dict:
    """
    Crée un contexte de test avec des métriques système spécifiques

    Args:
        cpu_usage: Utilisation CPU en pourcentage
        ram_usage: Utilisation RAM en pourcentage

    Returns:
        Dictionnaire contexte
    """
    return {
        "status": {
            "cpu": cpu_usage,
            "ram": ram_usage,
            "disk_usage": 70.0,
            "network_latency": 25.0,
            "severity": "normal",
        },
        "metadata": {"timestamp": time.time(), "source": "demo_integration_test"},
    }


def simulate_context_file(context_data: dict, temp_path: Path) -> None:
    """
    Simule un fichier de contexte temporaire

    Args:
        context_data: Données de contexte
        temp_path: Chemin du fichier temporaire
    """
    import toml

    temp_path.parent.mkdir(parents=True, exist_ok=True)

    with open(temp_path, "w") as f:
        toml.dump(context_data, f)


def test_scenario(
    scenario_name: str, cpu: float, ram: float, expected_behavior: str
) -> dict:
    """
    Teste un scénario spécifique avec Error Recovery

    Args:
        scenario_name: Nom du scénario de test
        cpu: Utilisation CPU
        ram: Utilisation RAM
        expected_behavior: Comportement attendu

    Returns:
        Résultats du test
    """
    print(f"\n🧪 === TEST SCENARIO: {scenario_name} ===")
    print(f"💻 CPU: {cpu}%, RAM: {ram}% - Attendu: {expected_behavior}")

    # Créer contexte temporaire
    temp_context_path = Path(f"temp/demo_context_{int(time.time())}.toml")
    context_data = create_test_context(cpu, ram)
    simulate_context_file(context_data, temp_context_path)

    try:
        # Exécuter boucle avec Error Recovery
        start_time = time.time()
        decision, score = reason_loop_enhanced_with_recovery(
            context_path=temp_context_path
        )
        duration = time.time() - start_time

        print(f"✅ Décision: {decision} (confiance: {score:.2f})")
        print(f"⏱️ Durée: {duration:.3f}s")

        # Nettoyer fichier temporaire
        if temp_context_path.exists():
            temp_context_path.unlink()

        return {
            "scenario": scenario_name,
            "decision": decision,
            "score": score,
            "duration": duration,
            "cpu": cpu,
            "ram": ram,
            "success": True,
        }

    except Exception as e:
        print(f"❌ Erreur: {e}")

        # Nettoyer en cas d'erreur
        if temp_context_path.exists():
            temp_context_path.unlink()

        return {
            "scenario": scenario_name,
            "error": str(e),
            "cpu": cpu,
            "ram": ram,
            "success": False,
        }


def main():
    """Fonction principale du demo"""
    print("🔄 DEMO: ZeroIA Enhanced + Error Recovery Integration v2.7.0")
    print("=" * 70)

    # Initialiser les composants
    try:
        cb, es, error_recovery, graceful_degradation = (
            initialize_components_with_recovery()
        )
        print("✅ Composants initialisés avec succès")

        if error_recovery:
            print("🔄 Error Recovery System: DISPONIBLE")
        else:
            print("⚠️ Error Recovery System: NON DISPONIBLE")

        if graceful_degradation:
            print("📉 Graceful Degradation: DISPONIBLE")
        else:
            print("⚠️ Graceful Degradation: NON DISPONIBLE")

    except Exception as e:
        print(f"❌ Erreur initialisation: {e}")
        return

    # Scénarios de test
    scenarios = [
        ("Normal Operation", 45.0, 60.0, "analyze"),
        ("Light Load", 25.0, 40.0, "increase_load"),
        ("High Load", 75.0, 80.0, "monitor"),
        ("Heavy Load", 85.0, 90.0, "optimize"),
        ("Critical Load", 95.0, 97.0, "reduce_load"),
        ("Extreme Load", 98.0, 99.0, "error_recovery_triggered"),
    ]

    results = []

    for scenario_name, cpu, ram, expected in scenarios:
        try:
            result = test_scenario(scenario_name, cpu, ram, expected)
            results.append(result)
            time.sleep(1)  # Petite pause entre tests

        except KeyboardInterrupt:
            print("\n🛑 Arrêt manuel détecté")
            break

    # Statistiques finales
    print("\n📊 === RÉSULTATS FINAUX ===")

    successful_tests = [r for r in results if r.get("success", False)]
    failed_tests = [r for r in results if not r.get("success", False)]

    print(f"✅ Tests réussis: {len(successful_tests)}")
    print(f"❌ Tests échoués: {len(failed_tests)}")
    print(f"📈 Taux de succès: {len(successful_tests)/len(results)*100:.1f}%")

    if successful_tests:
        avg_duration = sum(r["duration"] for r in successful_tests) / len(
            successful_tests
        )
        print(f"⏱️ Durée moyenne: {avg_duration:.3f}s")

    # Status des composants
    print("\n🔧 === STATUS DES COMPOSANTS ===")

    try:
        circuit_status = get_circuit_status()
        print(f"🔄 Circuit Breaker: {circuit_status.get('state', 'unknown')}")

        metrics = circuit_status.get("metrics", {})
        if metrics:
            print(f"📊 Success Rate: {metrics.get('success_rate', 0):.1f}%")
    except Exception as e:
        print(f"⚠️ Status Circuit Breaker: erreur ({e})")

    try:
        error_recovery_status = get_error_recovery_status()
        print(f"🔄 Error Recovery: {error_recovery_status.get('status', 'unknown')}")
    except Exception as e:
        print(f"⚠️ Status Error Recovery: erreur ({e})")

    try:
        degradation_status = get_degradation_status()
        print(f"📉 Graceful Degradation: {degradation_status.get('status', 'unknown')}")
    except Exception as e:
        print(f"⚠️ Status Graceful Degradation: erreur ({e})")

    try:
        event_analytics = get_event_analytics()
        total_events = event_analytics.get("total_events", 0)
        print(f"📋 Event Store: {total_events} événements")
    except Exception as e:
        print(f"⚠️ Status Event Store: erreur ({e})")

    print("\n🎉 Demo terminé avec succès !")
    print("💡 L'Error Recovery System est maintenant intégré dans ZeroIA Enhanced")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Demo interrompu manuellement")
    except Exception as e:
        logger.error(f"❌ Erreur dans demo: {e}")
        print(f"❌ Erreur inattendue: {e}")
