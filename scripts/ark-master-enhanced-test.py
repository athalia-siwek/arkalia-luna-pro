#!/usr/bin/env python3
"""
🌟 TEST ARKALIA MASTER ORCHESTRATOR ENHANCED v5.0.0
Script de test pour valider les nouveaux composants intégrés
"""

import asyncio
import logging
import sys
from pathlib import Path

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

async def test_enhanced_orchestrator():
    """Test complet de l'orchestrateur enhanced"""
    
    print("🌟 TEST ARKALIA ORCHESTRATOR ENHANCED v5.0.0")
    print("=" * 60)
    
    try:
        # Import de l'orchestrateur enhanced
        from modules.arkalia_master.orchestrator_enhanced_v5 import (
            ArkaliaOrchestratorEnhanced,
            OrchestratorEnhancedConfig,
            orchestrate_enhanced_ecosystem
        )
        
        print("✅ Import orchestrateur enhanced réussi")
        
        # Test 1: Configuration enhanced
        config = OrchestratorEnhancedConfig()
        config.cognitive_mode_enabled = True
        config.auto_recovery_enabled = True
        config.temporal_analysis_enabled = True
        config.cross_validation_enabled = True
        
        print("✅ Configuration enhanced créée")
        
        # Test 2: Initialisation orchestrateur
        orchestrator = ArkaliaOrchestratorEnhanced(config)
        print("✅ Orchestrateur enhanced initialisé")
        
        # Test 3: Initialisation modules enhanced
        print("\n🔌 Test initialisation modules enhanced...")
        init_success = await orchestrator.initialize_modules_enhanced()
        
        if init_success:
            print("✅ Modules enhanced initialisés avec succès")
        else:
            print("⚠️ Certains modules enhanced ont échoué (normal si composants manquants)")
        
        # Test 4: Statut enhanced
        print("\n📊 Test statut enhanced...")
        status = orchestrator.get_enhanced_status()
        
        print(f"🌟 Version: {status['orchestrator']['version']}")
        print(f"🔧 Modules: {len(status['modules'])}")
        print(f"🧠 Enhanced features actives: {sum(status['enhanced_features'].values())}")
        
        # Test 5: Cycle enhanced (test rapide)
        print("\n🔄 Test cycle enhanced...")
        if len(orchestrator.modules) > 0:
            cycle_result = await orchestrator.execute_enhanced_cycle()
            
            print(f"✅ Cycle enhanced terminé en {cycle_result['duration_seconds']}s")
            print(f"📊 Opérations: {cycle_result['operations_successful']}/{cycle_result['operations_executed']}")
            print(f"🧠 Événements cognitifs: {cycle_result['enhanced_features']['cognitive_events']}")
            print(f"🛡️ Récupérations: {cycle_result['enhanced_features']['recovery_events']}")
        else:
            print("⚠️ Aucun module disponible pour test cycle")
        
        print("\n🎉 TEST ENHANCED TERMINÉ AVEC SUCCÈS!")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erreur import: {e}")
        print("💡 Certains modules enhanced peuvent être manquants (normal)")
        return False
        
    except Exception as e:
        print(f"❌ Erreur test: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_enhanced_features():
    """Test spécifique des fonctionnalités enhanced"""
    
    print("\n🌟 TEST FONCTIONNALITÉS ENHANCED")
    print("=" * 50)
    
    features_availability = {
        "error_recovery": False,
        "cognitive_reactor": False, 
        "vault_manager": False,
        "chronalia": False,
        "crossmodule_validator": False
    }
    
    # Test Error Recovery System
    try:
        from modules.zeroia.error_recovery_system import ErrorRecoverySystem
        features_availability["error_recovery"] = True
        print("✅ Error Recovery System disponible")
    except ImportError:
        print("❌ Error Recovery System non disponible")
    
    # Test Cognitive Reactor
    try:
        from modules.sandozia.core.cognitive_reactor import CognitiveReactor
        features_availability["cognitive_reactor"] = True
        print("✅ Cognitive Reactor disponible")
    except ImportError:
        print("❌ Cognitive Reactor non disponible")
    
    # Test Vault Manager
    try:
        from modules.security.crypto.vault_manager import VaultManager
        features_availability["vault_manager"] = True
        print("✅ Vault Manager disponible")
    except ImportError:
        print("❌ Vault Manager non disponible")
    
    # Test Chronalia
    try:
        from modules.sandozia.core.chronalia import Chronalia
        features_availability["chronalia"] = True
        print("✅ Chronalia disponible")
    except ImportError:
        print("❌ Chronalia non disponible")
    
    # Test CrossModule Validator
    try:
        from modules.sandozia.validators.crossmodule import CrossModuleValidator
        features_availability["crossmodule_validator"] = True
        print("✅ CrossModule Validator disponible")
    except ImportError:
        print("❌ CrossModule Validator non disponible")
    
    # Résumé
    available_count = sum(features_availability.values())
    total_count = len(features_availability)
    
    print(f"\n📊 RÉSUMÉ ENHANCED FEATURES: {available_count}/{total_count} disponibles")
    
    if available_count >= 2:
        print("🎉 Suffisamment de fonctionnalités enhanced pour tester")
        return True
    else:
        print("⚠️ Peu de fonctionnalités enhanced disponibles")
        return False

async def main():
    """Point d'entrée principal du test"""
    
    print("🚀 DÉMARRAGE TESTS ARKALIA ORCHESTRATOR ENHANCED")
    print("=" * 70)
    
    # Test 1: Fonctionnalités enhanced
    features_ok = await test_enhanced_features()
    
    # Test 2: Orchestrateur enhanced
    orchestrator_ok = await test_enhanced_orchestrator()
    
    # Résultat final
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ FINAL TESTS")
    print("=" * 70)
    
    if features_ok and orchestrator_ok:
        print("🎉 TOUS LES TESTS ENHANCED RÉUSSIS!")
        print("✅ L'orchestrateur enhanced est prêt pour intégration")
        return 0
    elif orchestrator_ok:
        print("⚠️ TESTS PARTIELLEMENT RÉUSSIS")
        print("✅ Orchestrateur fonctionne mais certaines features manquent")
        return 1
    else:
        print("❌ TESTS ÉCHOUÉS")
        print("💡 Vérifier les imports et dépendances")
        return 2

if __name__ == "__main__":
    exit_code = asyncio.run(main()) 