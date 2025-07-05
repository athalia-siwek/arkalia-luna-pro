#!/usr/bin/env python3
"""
🔄 Demo ZeroIA Enhanced + Error Recovery Integration v2.7.0
Démontre l'intégration complète du système Error Recovery
dans la boucle de raisonnement ZeroIA Enhanced.
"""

import asyncio
import logging
import pathlib
import subprocess
import sys
import time
from pathlib import Path

from core.ark_logger import ark_logger

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


def test_scenario(scenario_name: str, cpu: float, ram: float, expected_behavior: str) -> dict:
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
    ark_logger.info(f"\n🧪 === TEST SCENARIO: {scenario_name} ===", extra={"module": "scripts"})
    ark_logger.info(f"💻 CPU: {cpu}%, RAM: {ram}% - Attendu: {expected_behavior}", extra={"module": "scripts"})

    # Créer contexte temporaire
    temp_context_path = Path(f"temp/demo_context_{int(time.time())}.toml")
    context_data = create_test_context(cpu, ram)
    simulate_context_file(context_data, temp_context_path)

    try:
        # Exécuter boucle avec Error Recovery
        start_time = time.time()
        decision, score = reason_loop_enhanced_with_recovery(context_path=temp_context_path)
        duration = time.time() - start_time

        ark_logger.info(f"✅ Décision: {decision} (confiance: {score:.2f}, extra={"module": "scripts"})")
        ark_logger.info(f"⏱️ Durée: {duration:.3f}s", extra={"module": "scripts"})

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
        ark_logger.info(f"❌ Erreur: {e}", extra={"module": "scripts"})

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


def format_generated():
    """Formate tous les dossiers generated avec isort + black."""
    for d in pathlib.Path(".").rglob("generated"):
        try:
            # Tri des imports avec isort (compatible black)
            subprocess.run(["isort", str(d), "--profile", "black"], check=True)
            # Formatage du code avec black
            subprocess.run(["black", str(d), "--quiet"], check=True)
            ark_logger.info(f"✅ Formaté: {d}", extra={"module": "scripts"})
        except subprocess.CalledProcessError as e:
            ark_logger.info(f"⚠️ Erreur formatage {d}: {e}", extra={"module": "scripts"})
            # Fallback: essayer au moins isort
            try:
                subprocess.run(["isort", str(d), "--fix"], check=False)
                ark_logger.info(f"⚠️ Fallback isort appliqué: {d}", extra={"module": "scripts"})
            except Exception:
                ark_logger.info(f"❌ Fallback échoué: {d}", extra={"module": "scripts"})


async def main():
    """Fonction principale du demo"""
    ark_logger.error("🔄 DEMO: ZeroIA Enhanced + Error Recovery Integration v2.7.0", extra={"module": "scripts"})
    ark_logger.info("=" * 70, extra={"module": "scripts"})

    # Initialiser les composants
    try:
        cb, es, error_recovery, graceful_degradation = initialize_components_with_recovery()
        ark_logger.info("✅ Composants initialisés avec succès", extra={"module": "scripts"})

        if error_recovery:
            ark_logger.error("🔄 Error Recovery System: DISPONIBLE", extra={"module": "scripts"})
        else:
            ark_logger.error("⚠️ Error Recovery System: NON DISPONIBLE", extra={"module": "scripts"})

        if graceful_degradation:
            ark_logger.info("📉 Graceful Degradation: DISPONIBLE", extra={"module": "scripts"})
        else:
            ark_logger.info("⚠️ Graceful Degradation: NON DISPONIBLE", extra={"module": "scripts"})

    except Exception as e:
        raise RuntimeError(f"Erreur initialisation: {e}") from e
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
            ark_logger.info("\n🛑 Arrêt manuel détecté", extra={"module": "scripts"})
            break

    # Statistiques finales
    ark_logger.info("\n📊 === RÉSULTATS FINAUX ===", extra={"module": "scripts"})

    successful_tests = [r for r in results if r.get("success", False)]
    failed_tests = [r for r in results if not r.get("success", False)]

    ark_logger.info(f"✅ Tests réussis: {len(successful_tests, extra={"module": "scripts"})}")
    ark_logger.error(f"❌ Tests échoués: {len(failed_tests, extra={"module": "scripts"})}")
    ark_logger.info(f"📈 Taux de succès: {len(successful_tests, extra={"module": "scripts"})/len(results)*100:.1f}%")

    if successful_tests:
        avg_duration = sum(r["duration"] for r in successful_tests) / len(successful_tests)
        ark_logger.info(f"⏱️ Durée moyenne: {avg_duration:.3f}s", extra={"module": "scripts"})

    # Status des composants
    ark_logger.info("\n🔧 === STATUS DES COMPOSANTS ===", extra={"module": "scripts"})

    try:
        circuit_status = get_circuit_status()
        ark_logger.info(f"🔄 Circuit Breaker: {circuit_status.get('state', 'unknown', extra={"module": "scripts"})}")

        metrics = circuit_status.get("metrics", {})
        if metrics:
            ark_logger.info(f"📊 Success Rate: {metrics.get('success_rate', 0, extra={"module": "scripts"}):.1f}%")
    except Exception as e:
        ark_logger.info(f"⚠️ Status Circuit Breaker: erreur ({e}, extra={"module": "scripts"})")

    try:
        error_recovery_status = get_error_recovery_status()
        ark_logger.error(f"🔄 Error Recovery: {error_recovery_status.get('status', 'unknown', extra={"module": "scripts"})}")
    except Exception as e:
        ark_logger.error(f"⚠️ Status Error Recovery: erreur ({e}, extra={"module": "scripts"})")

    try:
        degradation_status = get_degradation_status()
        ark_logger.info(f"📉 Graceful Degradation: {degradation_status.get('status', 'unknown', extra={"module": "scripts"})}")
    except Exception as e:
        ark_logger.info(f"⚠️ Status Graceful Degradation: erreur ({e}, extra={"module": "scripts"})")

    try:
        event_analytics = get_event_analytics()
        total_events = event_analytics.get("total_events", 0)
        ark_logger.info(f"📋 Event Store: {total_events} événements", extra={"module": "scripts"})
    except Exception as e:
        ark_logger.info(f"⚠️ Status Event Store: erreur ({e}, extra={"module": "scripts"})")

    ark_logger.info("\n🎉 Demo terminé avec succès !", extra={"module": "scripts"})
    ark_logger.error("💡 L'Error Recovery System est maintenant intégré dans ZeroIA Enhanced", extra={"module": "scripts"})

    format_generated()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        ark_logger.info("\n🛑 Demo interrompu manuellement", extra={"module": "scripts"})
    except Exception as e:
        logger.error(f"❌ Erreur dans demo: {e}")
        ark_logger.info(f"❌ Erreur inattendue: {e}", extra={"module": "scripts"})
        raise RuntimeError(f"Erreur demo zeroia error recovery integration: {e}") from e
