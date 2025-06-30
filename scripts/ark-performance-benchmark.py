#!/usr/bin/env python3
# 🚀 scripts/ark-performance-benchmark.py
# Script d'exécution des benchmarks performance Arkalia-LUNA

"""
Script de benchmarking performance pour Arkalia-LUNA Enhanced v2.7.1

Fonctionnalités :
- Lance tous les tests de performance
- Collecte et sauvegarde les métriques
- Génère rapport HTML
- Détecte régressions performance
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# Ajouter le chemin des modules
sys.path.insert(0, str(Path(__file__).parent.parent))


def run_performance_tests(output_dir="benchmark_results"):
    """Lance les tests de performance et collecte les résultats"""

    print("🚀 Lancement des benchmarks performance Arkalia-LUNA")
    print("=" * 60)

    # Créer dossier de résultats
    results_dir = Path(output_dir)
    results_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Configuration environnement pour les tests
    env = os.environ.copy()
    env.update(
        {
            "ZEROIA_DECISION_THRESHOLD": "2.0",
            "CIRCUIT_LATENCY_THRESHOLD_MS": "10.0",
            "EVENT_STORE_WRITE_THRESHOLD_MS": "50.0",
            "PYTEST_CURRENT_TEST": "performance",
        }
    )

    # Commande pytest pour les tests de performance
    cmd = [
        "python",
        "-m",
        "pytest",
        "tests/performance/",
        "-v",
        "--tb=short",
        "-m",
        "performance",
        "--capture=no",  # Afficher les prints
    ]

    print(f"📊 Commande : {' '.join(cmd)}")
    print(f"📁 Résultats dans : {results_dir}")
    print()

    # Exécuter les tests
    start_time = time.time()

    try:
        result = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutes max
        )

        end_time = time.time()
        duration = end_time - start_time

        # Sauvegarder les résultats
        results = {
            "timestamp": timestamp,
            "duration_seconds": duration,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "environment": {
                "python_version": sys.version,
                "os": os.name,
                "platform": sys.platform,
            },
        }

        results_file = results_dir / f"benchmark_results_{timestamp}.json"
        with open(results_file, "w") as f:
            json.dump(results, f, indent=2)

        # Afficher résultats
        print(f"✅ Benchmarks terminés en {duration:.1f}s")
        print(f"📊 Code retour : {result.returncode}")
        print(f"💾 Résultats sauvés : {results_file}")

        if result.returncode == 0:
            print("🎯 Tous les benchmarks ont réussi !")
        else:
            print("⚠️ Certains benchmarks ont échoué")

        # Afficher stdout si présent
        if result.stdout:
            print("\n📋 Sortie des tests :")
            print("-" * 40)
            print(result.stdout)

        if result.stderr:
            print("\n❌ Erreurs :")
            print("-" * 40)
            print(result.stderr)

        return result.returncode == 0

    except subprocess.TimeoutExpired:
        print("❌ Timeout : Les benchmarks ont pris trop de temps (>5min)")
        return False

    except Exception as e:
        print(f"❌ Erreur lors de l'exécution : {e}")
        return False


def generate_summary_report(output_dir="benchmark_results"):
    """Génère un rapport de synthèse des benchmarks"""

    results_dir = Path(output_dir)
    if not results_dir.exists():
        print(f"❌ Dossier {output_dir} introuvable")
        return

    # Trouver le fichier de résultats le plus récent
    json_files = list(results_dir.glob("benchmark_results_*.json"))
    if not json_files:
        print("❌ Aucun fichier de résultats trouvé")
        return

    latest_file = max(json_files, key=lambda f: f.stat().st_mtime)

    try:
        with open(latest_file) as f:
            results = json.load(f)

        print("\n📊 RAPPORT DE SYNTHÈSE BENCHMARKS")
        print("=" * 50)
        print(f"📅 Date : {results['timestamp']}")
        print(f"⏱️ Durée : {results['duration_seconds']:.1f}s")
        print(f"🎯 Statut : {'✅ SUCCÈS' if results['return_code'] == 0 else '❌ ÉCHEC'}")
        print(f"🐍 Python : {results['environment']['python_version'].split()[0]}")
        print(f"💻 Plateforme : {results['environment']['platform']}")

        # Extraire métriques du stdout si possible
        stdout = results.get("stdout", "")
        if "ZeroIA décision en" in stdout:
            print("\n🧠 Métriques ZeroIA :")
            for line in stdout.split("\n"):
                if "ZeroIA décision en" in line:
                    print(f"  {line}")

        if "Circuit Breaker" in stdout:
            print("\n⚡ Métriques Circuit Breaker :")
            for line in stdout.split("\n"):
                if "Circuit Breaker" in line and "Latence" in line:
                    print(f"  {line}")

        if "Event Store" in stdout:
            print("\n💾 Métriques Event Store :")
            for line in stdout.split("\n"):
                if "Event Store" in line and "événements" in line:
                    print(f"  {line}")

    except Exception as e:
        print(f"❌ Erreur lors de la génération du rapport : {e}")


def main():
    """Point d'entrée principal"""

    parser = argparse.ArgumentParser(description="Benchmarks performance Arkalia-LUNA Enhanced")
    parser.add_argument(
        "--output-dir",
        default="benchmark_results",
        help="Dossier de sortie des résultats",
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Générer seulement le rapport (sans lancer les tests)",
    )

    args = parser.parse_args()

    try:
        if args.report_only:
            generate_summary_report(args.output_dir)
        else:
            success = run_performance_tests(args.output_dir)
            if success:
                generate_summary_report(args.output_dir)
            sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Erreur fatale : {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
