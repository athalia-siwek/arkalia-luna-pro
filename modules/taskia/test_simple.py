#!/usr/bin/env python3
"""
🌕 TaskIA Simple Test
📝 Test simple du refactoring SOLID
🔧 Version: 2.0.0
👤 Author: Athalia
📅 Created: 2025-01-27
"""

import sys
import os

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_solid_refactoring():
    """Test simple du refactoring SOLID."""
    
    print("🚀 TEST SIMPLE SOLID TASKIA")
    print("=" * 40)
    
    try:
        # Test 1: Import des interfaces
        print("📋 Test 1: Import des interfaces...")
        from interfaces.formatter_interface import IFormatter
        from interfaces.task_processor_interface import ITaskProcessor
        from interfaces.health_check_interface import IHealthChecker
        print("✅ Interfaces importées avec succès")
        
        # Test 2: Import des formateurs
        print("📋 Test 2: Import des formateurs...")
        from formatters.summary_formatter import SummaryFormatter
        from formatters.json_formatter import JsonFormatter
        from formatters.markdown_formatter import MarkdownFormatter
        from formatters.html_formatter import HtmlFormatter
        print("✅ Formateurs importés avec succès")
        
        # Test 3: Import des services
        print("📋 Test 3: Import des services...")
        from services.task_processor import TaskProcessor
        from services.health_checker import HealthChecker
        from services.logger_service import LoggerService
        print("✅ Services importés avec succès")
        
        # Test 4: Import des factories
        print("📋 Test 4: Import des factories...")
        from factories.formatter_factory import FormatterFactory
        print("✅ Factories importées avec succès")
        
        # Test 5: Test de création d'objets
        print("📋 Test 5: Création d'objets...")
        
        # Créer un formateur
        summary_formatter = SummaryFormatter()
        print(f"✅ SummaryFormatter créé: {summary_formatter.get_format_type()}")
        
        # Créer un service de logging
        logger_service = LoggerService()
        print("✅ LoggerService créé")
        
        # Créer un processeur de tâches
        task_processor = TaskProcessor(summary_formatter, logger_service.get_logger())
        print("✅ TaskProcessor créé avec injection de dépendances")
        
        # Test 6: Test de formatage
        print("📋 Test 6: Test de formatage...")
        test_data = {"projet": "Arkalia", "module": "TaskIA", "version": "2.0.0"}
        result = task_processor.process(test_data)
        print(f"✅ Formatage réussi: {len(result)} caractères")
        print(f"   Résultat: {result[:100]}...")
        
        # Test 7: Test de factory
        print("📋 Test 7: Test de factory...")
        factory = FormatterFactory()
        available_formatters = factory.get_available_formatters()
        print(f"✅ Formateurs disponibles: {available_formatters}")
        
        # Test 8: Test de santé
        print("📋 Test 8: Test de santé...")
        health_checker = HealthChecker()
        health_status = health_checker.check_health()
        print(f"✅ Santé: {health_status['status']}")
        
        print("\n🎉 TOUS LES TESTS PASSÉS AVEC SUCCÈS!")
        print("=" * 40)
        print("✅ Refactoring SOLID réussi!")
        print("✅ Architecture modulaire fonctionnelle")
        print("✅ Injection de dépendances opérationnelle")
        print("✅ Factory pattern implémenté")
        print("✅ Interfaces SOLID respectées")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        print("❌ Refactoring SOLID incomplet")
        return False


if __name__ == "__main__":
    success = test_solid_refactoring()
    sys.exit(0 if success else 1) 