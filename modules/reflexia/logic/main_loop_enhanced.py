#!/usr/bin/env python3
# 🧠 modules/reflexia/logic/main_loop_enhanced.py
"""
Reflexia Enhanced Main Loop v2.6.0

Boucle principale améliorée avec :
- Vraies métriques système
- Analyse des containers Docker
- Détection d'anomalies intelligente
- Logs structurés
"""

import logging
import time
from datetime import datetime
from typing import Any, Optional

from .decision import monitor_status
from .metrics_enhanced import read_metrics, read_metrics_enhanced
from .snapshot import save_snapshot

logger = logging.getLogger(__name__)


def analyze_system_health(metrics: dict[str, Any]) -> dict[str, str]:
    """
    Analyse avancée de la santé du système

    Returns:
        Dict avec analyse détaillée par composant
    """
    analysis: dict[str, Any] = {}

    # Analyse système
    system = metrics.get("system", {})
    cpu = system.get("cpu_percent", 0)
    ram = system.get("memory_percent", 0)
    disk = system.get("disk_usage", 0)

    if cpu > 80:
        analysis["cpu"] = "critical"
    elif cpu > 60:
        analysis["cpu"] = "warning"
    else:
        analysis["cpu"] = "ok"

    if ram > 85:
        analysis["memory"] = "critical"
    elif ram > 70:
        analysis["memory"] = "warning"
    else:
        analysis["memory"] = "ok"

    if disk > 90:
        analysis["disk"] = "critical"
    elif disk > 80:
        analysis["disk"] = "warning"
    else:
        analysis["disk"] = "ok"

    # Analyse containers
    containers = metrics.get("containers", {})
    if isinstance(containers, dict) and "error" not in containers:
        healthy_count = len([c for c in containers.values() if c == "healthy"])
        total_count = len(containers)

        if total_count == 0:
            analysis["containers"] = "critical"
        elif healthy_count == total_count:
            analysis["containers"] = "ok"
        elif healthy_count >= total_count * 0.75:
            analysis["containers"] = "warning"
        else:
            analysis["containers"] = "critical"
    else:
        analysis["containers"] = "warning"

    # 🔥 NOUVELLE ANALYSE - Modules Arkalia spécifiques
    analysis["arkalia_modules"] = {}

    # Vérifier les modules principaux
    arkalia_modules: dict[str, str] = {
        "zeroia": "modules/zeroia/state/zeroia_state.toml",
        "sandozia": "state/sandozia",
        "assistantia": "modules/assistantia",
        "helloria": "helloria",
        "nyxalia": "modules/nyxalia",
        "taskia": "modules/taskia",
    }

    for module_name, module_path in arkalia_modules.items():
        try:
            from pathlib import Path

            path = Path(module_path)

            if path.exists():
                if module_name == "zeroia":
                    # Vérifier l'état ZeroIA spécifiquement
                    try:
                        import toml

                        zeroia_state = toml.load(path)
                        if zeroia_state.get("decision", {}).get("last_decision"):
                            analysis["arkalia_modules"][module_name] = "ok"
                        else:
                            analysis["arkalia_modules"][module_name] = "warning"
                    except Exception:
                        analysis["arkalia_modules"][module_name] = "warning"
                else:
                    analysis["arkalia_modules"][module_name] = "ok"
            else:
                analysis["arkalia_modules"][module_name] = "missing"
        except Exception:
            analysis["arkalia_modules"][module_name] = "error"

    return analysis


def generate_recommendations(analysis: dict[str, str], metrics: dict[str, Any]) -> list:
    """Génère des recommandations basées sur l'analyse"""
    recommendations: list[Any] = []

    if analysis.get("cpu") == "critical":
        recommendations.append("🔥 CPU critique: Vérifier les processus lourds")
    elif analysis.get("cpu") == "warning":
        recommendations.append("⚠️ CPU élevé: Surveiller l'activité")

    if analysis.get("memory") == "critical":
        recommendations.append("🔥 RAM critique: Redémarrer des services si nécessaire")
    elif analysis.get("memory") == "warning":
        recommendations.append("⚠️ RAM élevée: Optimiser l'usage mémoire")

    if analysis.get("disk") == "critical":
        recommendations.append("🔥 Disque plein: Nettoyer les logs et caches")

    if analysis.get("containers") == "critical":
        recommendations.append("🔥 Containers défaillants: Vérifier docker-compose")
    elif analysis.get("containers") == "warning":
        recommendations.append("⚠️ Certains containers instables")

    # 🔥 NOUVELLES RECOMMANDATIONS - Modules Arkalia
    arkalia_modules = analysis.get("arkalia_modules", {})

    if isinstance(arkalia_modules, dict):
        for module_name, status in arkalia_modules.items():
            if status == "missing":
                recommendations.append(
                    f"🔧 Module {module_name}: Fichiers manquants - Vérifier installation"
                )
            elif status == "error":
                recommendations.append(
                    f"❌ Module {module_name}: Erreur de chargement - Redémarrer"
                )
            elif status == "warning":
                recommendations.append(f"⚠️ Module {module_name}: État instable - Surveiller")

        # Recommandations spécifiques par module
        if arkalia_modules.get("zeroia") == "warning":
            recommendations.append("🧠 ZeroIA: Vérifier la boucle de raisonnement")

        if arkalia_modules.get("sandozia") == "missing":
            recommendations.append("🧠 Sandozia: Initialiser l'intelligence croisée")

        if arkalia_modules.get("assistantia") == "error":
            recommendations.append("💬 AssistantIA: Vérifier la connexion Ollama")

    if not recommendations:
        recommendations.append("✅ Système nominal - Continuer surveillance")

    return recommendations


def reflexia_loop_enhanced(
    max_iterations: int | None = None,
    sleep_seconds: float = 10.0,
    verbose: bool = True,
) -> None:
    """
    🔁 Boucle réflexive enhanced de ReflexIA v2.6.0

    Fonctionnalités:
    - Vraies métriques système (CPU/RAM/Disk)
    - État containers Docker Arkalia
    - Analyse intelligente et recommandations
    - Logs structurés avec timestamps

    Args:
        max_iterations: Nombre max d'itérations (None = infini)
        sleep_seconds: Délai entre chaque cycle
        verbose: Affichage détaillé des logs
    """
    iteration = 0
    start_time = datetime.now()

    if verbose:
        logger.info("🧠 Reflexia Enhanced Loop v2.6.0 started")
        print("🧠 Reflexia Enhanced Loop v2.6.0 started")

    while True:
        cycle_start = datetime.now()

        try:
            # Collecte métriques enhanced
            metrics_enhanced = read_metrics_enhanced()
            metrics_simple = read_metrics()  # Pour compatibilité

            # Analyse système
            health_analysis = analyze_system_health(metrics_enhanced)
            recommendations = generate_recommendations(health_analysis, metrics_enhanced)

            # Décision via logique existante
            status = monitor_status(metrics_simple)

            # Sauvegarde snapshot
            save_snapshot(metrics_simple, status)

            # Logs détaillés
            cycle_time = (datetime.now() - cycle_start).total_seconds()

            if verbose:
                print(f"🔄 [{datetime.now().strftime('%H:%M:%S')}] Reflexia Cycle #{iteration + 1}")
                print(
                    f"   💻 CPU: {metrics_enhanced['system']['cpu_percent']}% | "
                    f"RAM: {metrics_enhanced['system']['memory_percent']}% | "
                    f"Status: {status}"
                )

                containers = metrics_enhanced.get("containers", {})
                if isinstance(containers, dict) and "error" not in containers:
                    print(f"   🐳 Containers: {len(containers)} actifs")
                    for name, state in containers.items():
                        print(f"      • {name}: {state}")

                print("   🎯 Recommandations:")
                for rec in recommendations[:2]:  # Max 2 recommendations
                    print(f"      • {rec}")

                print(f"   ⏱️ Cycle time: {cycle_time:.2f}s")
                print()

            logger.info(f"Reflexia cycle #{iteration + 1} completed - Status: {status}")

        except Exception as e:
            logger.error(f"Reflexia enhanced cycle error: {e}")
            if verbose:
                print(f"❌ Erreur cycle Reflexia: {e}")

        time.sleep(sleep_seconds)
        iteration += 1

        if max_iterations is not None and iteration >= max_iterations:
            total_time = (datetime.now() - start_time).total_seconds()
            if verbose:
                logger.info(
                    f"Reflexia Enhanced completed - {iteration} cycles in {total_time:.1f}s"
                )
                print(f"🛑 Reflexia Enhanced terminé - {iteration} cycles en {total_time:.1f}s")
            break


# Alias pour compatibilité
def reflexia_loop(max_iterations: int | None = None, sleep_seconds: float = 5.0) -> None:
    """Alias de compatibilité avec l'ancienne boucle"""
    reflexia_loop_enhanced(max_iterations, sleep_seconds, verbose=True)


if __name__ == "__main__":
    # Test de la boucle enhanced
    print("🧪 Test Reflexia Enhanced Loop (3 cycles)")
    reflexia_loop_enhanced(max_iterations=3, sleep_seconds=2, verbose=True)
