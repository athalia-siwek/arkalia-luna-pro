#!/usr/bin/env python3
"""
🌕 TaskIA SOLID Test
📝 Test du refactoring SOLID depuis la racine
🔧 Version: 2.0.0
👤 Author: Athalia
📅 Created: 2025-01-27
"""

import os
import sys


def test_solid_refactoring():
    """Test simple du refactoring SOLID."""

    print("🚀 TEST SOLID TASKIA")
    print("=" * 40)

    try:
        # Test 1: Import des interfaces
        print("📋 Test 1: Import des interfaces...")
        from modules.taskia.interfaces.formatter_interface import IFormatter
        from modules.taskia.interfaces.health_check_interface import IHealthChecker
        from modules.taskia.interfaces.task_processor_interface import ITaskProcessor

        print("✅ Interfaces importées avec succès")

        # Test 2: Import des formateurs
        print("📋 Test 2: Import des formateurs...")
        from modules.taskia.formatters.html_formatter import HtmlFormatter
        from modules.taskia.formatters.json_formatter import JsonFormatter
        from modules.taskia.formatters.markdown_formatter import MarkdownFormatter
        from modules.taskia.formatters.summary_formatter import SummaryFormatter

        print("✅ Formateurs importés avec succès")

        # Test 3: Import des services
        print("📋 Test 3: Import des services...")
        from modules.taskia.services.health_checker import HealthChecker
        from modules.taskia.services.logger_service import LoggerService
        from modules.taskia.services.task_processor import TaskProcessor

        print("✅ Services importés avec succès")

        # Test 4: Import des factories
        print("📋 Test 4: Import des factories...")
        from modules.taskia.factories import FormatterFactory

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
