#!/usr/bin/env python3
"""
🧪 Test de la nouvelle architecture modulaire ZeroIA

Teste les 4 nouveaux modules :
- Decision Engine
- State Manager  
- Metrics Manager
- Coordinator
"""

import json
import logging
import time
from pathlib import Path

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_decision_engine():
    """Test du Decision Engine"""
    logger.info("🧠 Test Decision Engine...")
    
    try:
        from modules.zeroia.decision_engine import DecisionEngine
        
        engine = DecisionEngine()
        
        # Test création contexte par défaut
        context = engine.create_default_context_enhanced()
        assert "status" in context
        assert "modules" in context
        logger.info("✅ Contexte par défaut créé")
        
        # Test analyse de contexte
        analysis = engine.analyze_context(context)
        assert "cpu" in analysis
        assert "ram" in analysis
        logger.info("✅ Analyse de contexte OK")
        
        # Test prise de décision
        decision, score = engine.decide_protected(context)
        assert isinstance(decision, str)
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0
        logger.info(f"✅ Décision prise: {decision} (score: {score:.2f})")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur Decision Engine: {e}")
        return False

def test_state_manager():
    """Test du State Manager"""
    logger.info("📊 Test State Manager...")
    
    try:
        from modules.zeroia.state_manager import StateManager
        
        manager = StateManager()
        
        # Test persistance d'état
        test_decision = "test_decision"
        test_score = 0.85
        test_context = {"status": {"cpu": 50, "ram": 60}, "system_status": "test"}
        
        manager.persist_state_enhanced(test_decision, test_score, test_context)
        logger.info("✅ État persisté")
        
        # Test mise à jour dashboard
        manager.update_dashboard_enhanced(test_decision, test_score, test_context)
        logger.info("✅ Dashboard mis à jour")
        
        # Test chargement état
        current_state = manager.load_current_state()
        assert "last_decision" in current_state
        logger.info("✅ État chargé")
        
        # Test résumé dashboard
        dashboard_summary = manager.get_dashboard_summary()
        assert "total_decisions" in dashboard_summary
        logger.info("✅ Résumé dashboard OK")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur State Manager: {e}")
        return False

def test_metrics_manager():
    """Test du Metrics Manager"""
    logger.info("📈 Test Metrics Manager...")
    
    try:
        from modules.zeroia.metrics import (
            update_zeroia_metrics, 
            get_zeroia_metrics, 
            generate_prometheus_metrics,
            get_metrics_summary
        )
        
        # Test mise à jour métriques
        update_zeroia_metrics("test_operation", "success", 0.5, cognitive_score=0.8, decision_type="test")
        logger.info("✅ Métriques mises à jour")
        
        # Test récupération métriques
        metrics = get_zeroia_metrics()
        assert "arkalia_module_name" in metrics
        assert "uptime_seconds" in metrics
        assert "cognitive_score" in metrics
        logger.info("✅ Métriques récupérées")
        
        # Test métriques Prometheus
        prometheus_metrics = generate_prometheus_metrics()
        assert "zeroia_uptime_seconds" in prometheus_metrics
        assert "zeroia_cognitive_score" in prometheus_metrics
        logger.info("✅ Métriques Prometheus générées")
        
        # Test résumé métriques
        summary = get_metrics_summary()
        assert "module" in summary
        assert "status" in summary
        logger.info("✅ Résumé métriques OK")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur Metrics Manager: {e}")
        return False

def test_coordinator():
    """Test du Coordinator"""
    logger.info("🎯 Test Coordinator...")
    
    try:
        from modules.zeroia.coordinator import ZeroIACoordinator
        
        coordinator = ZeroIACoordinator()
        
        # Test statut initial
        status = coordinator.get_status()
        assert "module" in status
        assert "status" in status
        logger.info("✅ Statut initial OK")
        
        # Test cycle unique
        decision, score = coordinator.run_single_cycle()
        assert isinstance(decision, str)
        assert isinstance(score, float)
        logger.info(f"✅ Cycle unique: {decision} (score: {score:.2f})")
        
        # Test statut après cycle
        status_after = coordinator.get_status()
        assert status_after["cycle_count"] > 0
        logger.info("✅ Statut après cycle OK")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur Coordinator: {e}")
        return False

def test_compatibility_functions():
    """Test des fonctions de compatibilité"""
    logger.info("🔄 Test fonctions de compatibilité...")
    
    try:
        from modules.zeroia.coordinator import (
            reason_loop_enhanced_with_recovery,
            get_circuit_status,
            get_error_recovery_status,
            get_degradation_status
        )
        
        # Test fonction principale
        decision, score = reason_loop_enhanced_with_recovery()
        assert isinstance(decision, str)
        assert isinstance(score, float)
        logger.info(f"✅ Fonction principale: {decision} (score: {score:.2f})")
        
        # Test statuts
        circuit_status = get_circuit_status()
        error_status = get_error_recovery_status()
        degradation_status = get_degradation_status()
        
        assert isinstance(circuit_status, dict)
        assert isinstance(error_status, dict)
        assert isinstance(degradation_status, dict)
        
        logger.info("✅ Fonctions de compatibilité OK")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur fonctions compatibilité: {e}")
        return False

def main():
    """Test principal"""
    logger.info("🚀 Démarrage tests architecture modulaire ZeroIA")
    
    tests = [
        ("Decision Engine", test_decision_engine),
        ("State Manager", test_state_manager),
        ("Metrics Manager", test_metrics_manager),
        ("Coordinator", test_coordinator),
        ("Compatibilité", test_compatibility_functions),
    ]
    
    results = {}
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n{'='*50}")
        logger.info(f"🧪 Test: {test_name}")
        logger.info(f"{'='*50}")
        
        start_time = time.time()
        success = test_func()
        duration = time.time() - start_time
        
        results[test_name] = {
            "success": success,
            "duration": duration,
        }
        
        if success:
            passed += 1
            logger.info(f"✅ {test_name}: SUCCÈS ({duration:.2f}s)")
        else:
            logger.error(f"❌ {test_name}: ÉCHEC ({duration:.2f}s)")
    
    # Résumé final
    logger.info(f"\n{'='*50}")
    logger.info("📊 RÉSUMÉ DES TESTS")
    logger.info(f"{'='*50}")
    
    for test_name, result in results.items():
        status = "✅ SUCCÈS" if result["success"] else "❌ ÉCHEC"
        logger.info(f"{test_name}: {status} ({result['duration']:.2f}s)")
    
    logger.info(f"\n🎯 Résultat global: {passed}/{total} tests réussis")
    
    if passed == total:
        logger.info("🎉 Tous les tests sont passés ! Architecture modulaire OK")
        return True
    else:
        logger.error(f"⚠️ {total - passed} test(s) ont échoué")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 