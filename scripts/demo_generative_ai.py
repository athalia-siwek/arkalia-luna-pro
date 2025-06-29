#!/usr/bin/env python3
"""
🚀 Démonstration Intelligence Générative Avancée - Arkalia-LUNA v2.8.0
======================================================================

Script de démonstration pour tester les capacités d'auto-génération de code.
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path

# Ajouter le répertoire modules au path
sys.path.insert(0, str(Path(__file__).parent.parent / "modules"))

from generative_ai.core import GenerativeAI

async def demo_generative_ai():
    """Démonstration complète de l'Intelligence Générative"""
    print("🚀 Démonstration Intelligence Générative Avancée")
    print("=" * 60)
    
    # === Initialisation ===
    print("\n1️⃣ Initialisation du système génératif...")
    generative_ai = GenerativeAI(mode="demo")
    
    if not generative_ai.enabled:
        print("❌ Intelligence Générative désactivée")
        return
    
    print("✅ Système génératif initialisé")
    
    # === Analyse de la base de code ===
    print("\n2️⃣ Analyse de la base de code...")
    analysis = generative_ai.analyze_codebase()
    
    print(f"📊 Modules analysés: {len(analysis['modules'])}")
    print(f"🔍 Patterns détectés: {len(analysis['patterns'])}")
    print(f"🔧 Opportunités d'optimisation: {len(analysis['optimization_opportunities'])}")
    print(f"🧪 Tests manquants: {len(analysis['missing_tests'])}")
    
    # === Génération de code ===
    print("\n3️⃣ Génération de code automatique...")
    
    # Créer un module optimisé
    module_result = generative_ai.create_optimized_module(
        "demo_optimizer",
        "Module de démonstration pour l'optimisation automatique"
    )
    
    if "error" not in module_result:
        print(f"✅ Module généré: {module_result['module_path']}")
        print(f"✅ Tests générés: {module_result['test_path']}")
    else:
        print(f"❌ Erreur génération: {module_result['error']}")
    
    # === Génération d'endpoint API ===
    print("\n4️⃣ Génération d'endpoint API...")
    
    api_code = generative_ai.generate_code("api_endpoint", {
        "model_name": "DemoRequest",
        "endpoint_name": "demo_processing",
        "fields": "data: str\npriority: int = 1",
        "method": "post",
        "endpoint_path": "demo/process",
        "function_name": "process_demo_data",
        "endpoint_description": "Traite les données de démonstration"
    })
    
    print("✅ Endpoint API généré:")
    print("-" * 40)
    print(api_code)
    print("-" * 40)
    
    # === Optimisation de code existant ===
    print("\n5️⃣ Optimisation de code existant...")
    
    # Chercher un module à optimiser
    if analysis["optimization_opportunities"]:
        module_to_optimize = analysis["optimization_opportunities"][0]["module"]
        module_path = f"modules/{module_to_optimize}/core.py"
        
        if Path(module_path).exists():
            opt_result = generative_ai.optimize_existing_code(module_path)
            if "error" not in opt_result:
                print(f"✅ Module optimisé: {opt_result['original_path']}")
                print(f"📦 Backup créé: {opt_result['backup_path']}")
                print(f"🔧 Optimisations: {opt_result['optimizations']}")
            else:
                print(f"❌ Erreur optimisation: {opt_result['error']}")
        else:
            print(f"⚠️  Module {module_path} non trouvé")
    else:
        print("✅ Aucune opportunité d'optimisation détectée")
    
    # === Statut final ===
    print("\n6️⃣ Statut final du système...")
    status = generative_ai.get_status()
    
    print(f"🚀 Générations effectuées: {status['generation_count']}")
    print(f"📝 Code généré: {status['generative_state']['code_generated']}")
    print(f"🧪 Tests générés: {status['generative_state']['tests_generated']}")
    print(f"🔧 Optimisations appliquées: {status['generative_state']['optimizations_applied']}")
    print(f"📁 Fichiers générés: {status['generated_files']}")
    
    # === Sauvegarde de l'état ===
    generative_ai.save_generative_state()
    print("\n✅ État sauvegardé")
    
    print("\n🎉 Démonstration terminée avec succès !")

def demo_quick():
    """Démonstration rapide"""
    print("🚀 Démonstration rapide - Intelligence Générative")
    print("=" * 50)
    
    generative_ai = GenerativeAI(mode="demo")
    
    # Analyse rapide
    analysis = generative_ai.analyze_codebase()
    print(f"📊 {len(analysis['modules'])} modules analysés")
    
    # Génération d'un module simple
    result = generative_ai.create_optimized_module(
        "quick_demo",
        "Module de démonstration rapide"
    )
    
    if "error" not in result:
        print(f"✅ Module généré: {result['module_path']}")
    else:
        print(f"❌ Erreur: {result['error']}")
    
    print("✅ Démonstration rapide terminée")

def demo_analysis():
    """Démonstration d'analyse uniquement"""
    print("🔍 Démonstration d'analyse - Intelligence Générative")
    print("=" * 50)
    
    generative_ai = GenerativeAI(mode="demo")
    analysis = generative_ai.analyze_codebase()
    
    print(f"📊 Modules analysés: {len(analysis['modules'])}")
    
    if analysis['modules']:
        print("\n📋 Top 5 modules par complexité:")
        sorted_modules = sorted(analysis['modules'], key=lambda x: x.get('complexity', 0), reverse=True)
        for i, module in enumerate(sorted_modules[:5], 1):
            print(f"  {i}. {module.get('name', 'Unknown')} - Complexité: {module.get('complexity', 0)}")
    
    print(f"\n🔍 Patterns détectés: {len(analysis['patterns'])}")
    for pattern in analysis['patterns']:
        print(f"  - {pattern['type']}: {pattern['description']}")
    
    print(f"\n🔧 Opportunités d'optimisation: {len(analysis['optimization_opportunities'])}")
    for opp in analysis['optimization_opportunities'][:3]:
        print(f"  - {opp['module']}: {opp['description']}")
    
    print(f"\n🧪 Tests manquants: {len(analysis['missing_tests'])}")
    for test in analysis['missing_tests'][:3]:
        print(f"  - {test['module']}: {test['description']}")

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
        
        print("\n🌟 Intelligence Générative Avancée - Opérationnelle !")
        
    except KeyboardInterrupt:
        print("\n⚠️  Démonstration interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors de la démonstration: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 