#!/usr/bin/env python3
"""
🚀 Démonstration Intelligence Générative Avancée - Arkalia-LUNA v2.8.0
======================================================================

Script de démonstration pour tester les capacités d'auto-génération de code.
"""

import argparse
import asyncio
import pathlib
import subprocess
import sys
from pathlib import Path

from core.ark_logger import ark_logger

# Ajouter le répertoire modules au path
sys.path.insert(0, str(Path(__file__).parent.parent / "modules"))

from generative_ai.core import GenerativeAI


async def demo_generative_ai():
    """Démonstration complète de l'Intelligence Générative"""
    ark_logger.info("🚀 Démonstration Intelligence Générative Avancée", extra={"module": "scripts"})
    ark_logger.info("=" * 60, extra={"module": "scripts"})

    # === Initialisation ===
    ark_logger.info("\n1️⃣ Initialisation du système génératif...", extra={"module": "scripts"})
    generative_ai = GenerativeAI(mode="demo")

    if not generative_ai.enabled:
        ark_logger.info("❌ Intelligence Générative désactivée", extra={"module": "scripts"})
        return

    ark_logger.info("✅ Système génératif initialisé", extra={"module": "scripts"})

    # === Analyse de la base de code ===
    ark_logger.info("\n2️⃣ Analyse de la base de code...", extra={"module": "scripts"})
    analysis = generative_ai.analyze_codebase()

    ark_logger.info(f"📊 Modules analysés: {len(analysis['modules'], extra={"module": "scripts"})}")
    ark_logger.info(
        f"🔍 Patterns détectés: {len(analysis['patterns'], extra={"module": "scripts"})}"
    )
    ark_logger.info(
        f"🔧 Opportunités d'optimisation: {len(analysis['optimization_opportunities'], extra={"module": "scripts"})}"
    )
    ark_logger.info(
        f"🧪 Tests manquants: {len(analysis['missing_tests'], extra={"module": "scripts"})}"
    )

    # === Génération de code ===
    ark_logger.info("\n3️⃣ Génération de code automatique...", extra={"module": "scripts"})

    # Créer un module optimisé
    module_result = generative_ai.create_optimized_module(
        "demo_optimizer", "Module de démonstration pour l'optimisation automatique"
    )

    if "error" not in module_result:
        ark_logger.info(
            f"✅ Module généré: {module_result['module_path']}", extra={"module": "scripts"}
        )
        ark_logger.info(
            f"✅ Tests générés: {module_result['test_path']}", extra={"module": "scripts"}
        )
    else:
        ark_logger.error(
            f"❌ Erreur génération: {module_result['error']}", extra={"module": "scripts"}
        )

    # === Génération d'endpoint API ===
    ark_logger.info("\n4️⃣ Génération d'endpoint API...", extra={"module": "scripts"})

    api_code = generative_ai.generate_code(
        "api_endpoint",
        {
            "model_name": "DemoRequest",
            "endpoint_name": "demo_processing",
            "fields": "data: str\npriority: int = 1",
            "method": "post",
            "endpoint_path": "demo/process",
            "function_name": "process_demo_data",
            "endpoint_description": "Traite les données de démonstration",
        },
    )

    ark_logger.info("✅ Endpoint API généré:", extra={"module": "scripts"})
    ark_logger.info("-" * 40, extra={"module": "scripts"})
    ark_logger.info(api_code, extra={"module": "scripts"})
    ark_logger.info("-" * 40, extra={"module": "scripts"})

    # === Optimisation de code existant ===
    ark_logger.info("\n5️⃣ Optimisation de code existant...", extra={"module": "scripts"})

    # Chercher un module à optimiser
    if analysis["optimization_opportunities"]:
        module_to_optimize = analysis["optimization_opportunities"][0]["module"]
        module_path = f"modules/{module_to_optimize}/core.py"

        if Path(module_path).exists():
            opt_result = generative_ai.optimize_existing_code(module_path)
            if "error" not in opt_result:
                ark_logger.info(
                    f"✅ Module optimisé: {opt_result['original_path']}",
                    extra={"module": "scripts"},
                )
                ark_logger.info(
                    f"📦 Backup créé: {opt_result['backup_path']}", extra={"module": "scripts"}
                )
                ark_logger.info(
                    f"🔧 Optimisations: {opt_result['optimizations']}", extra={"module": "scripts"}
                )
            else:
                ark_logger.error(
                    f"❌ Erreur optimisation: {opt_result['error']}", extra={"module": "scripts"}
                )
        else:
            ark_logger.info(f"⚠️  Module {module_path} non trouvé", extra={"module": "scripts"})
    else:
        ark_logger.info(
            "✅ Aucune opportunité d'optimisation détectée", extra={"module": "scripts"}
        )

    # === Statut final ===
    ark_logger.info("\n6️⃣ Statut final du système...", extra={"module": "scripts"})
    status = generative_ai.get_status()

    ark_logger.info(
        f"🚀 Générations effectuées: {status['generation_count']}", extra={"module": "scripts"}
    )
    ark_logger.info(
        f"📝 Code généré: {status['generative_state']['code_generated']}",
        extra={"module": "scripts"},
    )
    ark_logger.info(
        f"🧪 Tests générés: {status['generative_state']['tests_generated']}",
        extra={"module": "scripts"},
    )
    ark_logger.info(
        f"🔧 Optimisations appliquées: {status['generative_state']['optimizations_applied']}",
        extra={"module": "scripts"},
    )
    ark_logger.info(
        f"📁 Fichiers générés: {status['generated_files']}", extra={"module": "scripts"}
    )

    # === Sauvegarde de l'état ===
    generative_ai.save_generative_state()
    ark_logger.info("\n✅ État sauvegardé", extra={"module": "scripts"})

    ark_logger.info("\n🎉 Démonstration terminée avec succès !", extra={"module": "scripts"})


def demo_quick():
    """Démonstration rapide"""
    ark_logger.info(
        "🚀 Démonstration rapide - Intelligence Générative", extra={"module": "scripts"}
    )
    ark_logger.info("=" * 50, extra={"module": "scripts"})

    generative_ai = GenerativeAI(mode="demo")

    # Analyse rapide
    analysis = generative_ai.analyze_codebase()
    ark_logger.info(f"📊 {len(analysis['modules'], extra={"module": "scripts"})} modules analysés")

    # Génération d'un module simple
    result = generative_ai.create_optimized_module("quick_demo", "Module de démonstration rapide")

    if "error" not in result:
        ark_logger.info(f"✅ Module généré: {result['module_path']}", extra={"module": "scripts"})
    else:
        ark_logger.error(f"❌ Erreur: {result['error']}", extra={"module": "scripts"})

    ark_logger.info("✅ Démonstration rapide terminée", extra={"module": "scripts"})


def demo_analysis():
    """Démonstration d'analyse uniquement"""
    ark_logger.info(
        "🔍 Démonstration d'analyse - Intelligence Générative", extra={"module": "scripts"}
    )
    ark_logger.info("=" * 50, extra={"module": "scripts"})

    generative_ai = GenerativeAI(mode="demo")
    analysis = generative_ai.analyze_codebase()

    ark_logger.info(f"📊 Modules analysés: {len(analysis['modules'], extra={"module": "scripts"})}")

    if analysis["modules"]:
        ark_logger.info("\n📋 Top 5 modules par complexité:", extra={"module": "scripts"})
        sorted_modules = sorted(
            analysis["modules"], key=lambda x: x.get("complexity", 0), reverse=True
        )
        for i, module in enumerate(sorted_modules[:5], 1):
            name = module.get("name", "Unknown")
            complexity = module.get("complexity", 0)
            ark_logger.info(
                f"  {i}. {name} - Complexité: {complexity}", extra={"module": "scripts"}
            )

    ark_logger.info(
        f"\n🔍 Patterns détectés: {len(analysis['patterns'], extra={"module": "scripts"})}"
    )
    for pattern in analysis["patterns"]:
        ark_logger.info(
            f"  - {pattern['type']}: {pattern['description']}", extra={"module": "scripts"}
        )

    ark_logger.info(
        f"\n🔧 Opportunités d'optimisation: {len(analysis['optimization_opportunities'], extra={"module": "scripts"})}"
    )
    for opp in analysis["optimization_opportunities"][:3]:
        ark_logger.info(f"  - {opp['module']}: {opp['description']}", extra={"module": "scripts"})

    ark_logger.info(
        f"\n🧪 Tests manquants: {len(analysis['missing_tests'], extra={"module": "scripts"})}"
    )
    for test in analysis["missing_tests"][:3]:
        ark_logger.info(f"  - {test['module']}: {test['description']}", extra={"module": "scripts"})


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
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="Démonstration Intelligence Générative")
    parser.add_argument("--mode", default="full", choices=["full", "quick", "analysis"])
    parser.add_argument("--output", help="Fichier de sortie pour les résultats")

    args = parser.parse_args()

    try:
        if args.mode == "full":
            await demo_generative_ai()
        elif args.mode == "quick":
            demo_quick()
        elif args.mode == "analysis":
            demo_analysis()

        ark_logger.info(
            "\n🌟 Intelligence Générative Avancée - Opérationnelle !", extra={"module": "scripts"}
        )

        format_generated()

    except KeyboardInterrupt:
        ark_logger.info(
            "\n⚠️  Démonstration interrompue par l'utilisateur", extra={"module": "scripts"}
        )
    except Exception as e:
        raise RuntimeError(f"Erreur demo generative AI: {e}") from e


if __name__ == "__main__":
    asyncio.run(main())
