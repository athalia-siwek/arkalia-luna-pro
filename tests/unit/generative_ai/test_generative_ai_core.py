#!/usr/bin/env python3
"""
🧪 Tests unitaires pour GenerativeAI Core

Tests couvrant :
- Génération de code
- Analyse de base de code
- Templates de tests
- Intégration avec les modules existants
"""

import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, mock_open, patch

import pytest

# Ajout du path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.generative_ai.core import GenerativeAI


class TestGenerativeAI:
    """Tests pour le module GenerativeAI"""

    @pytest.fixture
    def generative_ai(self):
        """Fixture pour GenerativeAI"""
        return GenerativeAI()

    def test_generative_ai_initialization(self, generative_ai):
        """Test d'initialisation de GenerativeAI"""
        assert generative_ai is not None
        assert hasattr(generative_ai, "code_templates")
        assert hasattr(generative_ai, "test_templates")

    def test_load_code_templates(self, generative_ai):
        """Test de chargement des templates de code"""
        templates = generative_ai._load_code_templates()

        assert isinstance(templates, dict)
        assert "class_template" in templates
        assert "function_template" in templates
        assert "api_endpoint" in templates

    def test_load_test_templates(self, generative_ai):
        """Test de chargement des templates de tests"""
        templates = generative_ai._load_test_templates()

        assert isinstance(templates, dict)
        assert "unit_test" in templates
        assert "integration_test" in templates

    def test_analyze_codebase_basic(self, generative_ai):
        """Test d'analyse basique de la base de code"""
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.rglob") as mock_rglob,
        ):

            # Mock des fichiers de modules
            mock_files = [MagicMock(name="test_module.py"), MagicMock(name="another_module.py")]
            mock_rglob.return_value = mock_files

            analysis = generative_ai.analyze_codebase()

            assert isinstance(analysis, dict)
            assert "modules" in analysis
            assert "patterns" in analysis
            assert "optimization_opportunities" in analysis
            assert "missing_tests" in analysis

    def test_analyze_codebase_no_modules(self, generative_ai):
        """Test d'analyse avec aucun module"""
        with patch("pathlib.Path.exists", return_value=False):
            analysis = generative_ai.analyze_codebase()

            assert isinstance(analysis, dict)
            assert analysis["modules"] == []

    def test_analyze_module(self, generative_ai):
        """Test d'analyse d'un module individuel"""
        mock_file = MagicMock()
        mock_file.name = "test_module.py"
        mock_file.suffix = ".py"
        mock_file.read_text.return_value = """
class TestClass:
    def test_method(self):
        pass

def test_function():
    pass
"""

        module_info = generative_ai._analyze_module(mock_file)

        assert isinstance(module_info, dict)
        assert "name" in module_info
        assert "size" in module_info
        assert "complexity" in module_info

    def test_detect_code_patterns(self, generative_ai):
        """Test de détection de patterns dans le code"""
        modules = [
            {"name": "module1", "complexity": 15},
            {"name": "module2", "complexity": 5},
            {"name": "module3", "size": 2000},
        ]

        patterns = generative_ai._detect_code_patterns(modules)

        assert isinstance(patterns, list)
        # Vérification des patterns détectés
        pattern_types = [p["type"] for p in patterns]
        assert "high_complexity" in pattern_types or "code_splitting" in pattern_types

    def test_has_tests_true(self, generative_ai):
        """Test de vérification d'existence de tests (positif)"""
        with patch("pathlib.Path.exists", return_value=True):
            has_tests = generative_ai._has_tests("test_module")
            assert has_tests is True

    def test_has_tests_false(self, generative_ai):
        """Test de vérification d'existence de tests (négatif)"""
        with patch("pathlib.Path.exists", return_value=False):
            has_tests = generative_ai._has_tests("test_module")
            assert has_tests is False

    def test_find_optimization_opportunities(self, generative_ai):
        """Test de recherche d'opportunités d'optimisation"""
        modules = [
            {"name": "complex_module", "complexity": 20},
            {"name": "large_module", "size": 1500},
            {"name": "simple_module", "complexity": 5, "size": 100},
        ]

        opportunities = generative_ai._find_optimization_opportunities(modules)

        assert isinstance(opportunities, list)
        assert len(opportunities) > 0
        assert any("complexity_reduction" in opp["type"] for opp in opportunities)

    def test_find_missing_tests(self, generative_ai):
        """Test de recherche de tests manquants"""
        modules = [{"name": "module1"}, {"name": "module2"}, {"name": "module3"}]

        with patch.object(generative_ai, "_has_tests", return_value=False):
            missing_tests = generative_ai._find_missing_tests(modules)

            assert isinstance(missing_tests, list)
            assert len(missing_tests) == 3
            assert all("unit_tests" in test["type"] for test in missing_tests)

    def test_generate_code_class(self, generative_ai):
        """Test de génération de code pour une classe"""
        class_info = {"class_name": "TestClass", "module_name": "test_module"}

        code = generative_ai.generate_code("class", class_info)

        assert isinstance(code, str)
        assert "class TestClass" in code

    def test_generate_code_function(self, generative_ai):
        """Test de génération de code pour une fonction"""
        function_info = {
            "function_name": "test_function",
            "parameters": "param1, param2",
            "description": "Test function",
            "return_value": "None",
            "module_name": "test_module",
        }

        code = generative_ai.generate_code("function", function_info)

        assert isinstance(code, str)
        assert "def test_function" in code
        assert "param1, param2" in code

    def test_generate_test_unit(self, generative_ai):
        """Test de génération de test unitaire"""
        test_info = {
            "module_name": "test_module",
            "class_name": "TestClass",
            "function_name": "test_method",
        }

        test_code = generative_ai.generate_test("unit", test_info)

        assert isinstance(test_code, str)
        assert "def test_test_method" in test_code

    def test_generate_test_integration(self, generative_ai):
        """Test de génération de test d'intégration"""
        test_info = {
            "module_name": "api_module",
            "endpoint_name": "test_endpoint",
            "method": "GET",
            "endpoint_path": "test",
        }

        test_code = generative_ai.generate_test("integration", test_info)

        assert isinstance(test_code, str)
        assert "def test_test_endpoint_endpoint" in test_code

    def test_validate_generated_code(self, generative_ai):
        """Test de validation du code généré"""
        valid_code = """
def test_function():
    return "test"
"""

        is_valid = generative_ai.validate_generated_code(valid_code)
        assert is_valid is True

    def test_validate_generated_code_invalid(self, generative_ai):
        """Test de validation du code généré invalide"""
        invalid_code = """
def test_function(
    return "test"
"""

        is_valid = generative_ai.validate_generated_code(invalid_code)
        assert is_valid is False

    @pytest.mark.asyncio
    async def test_generate_code_async(self, generative_ai):
        """Test de génération de code asynchrone"""
        async_info = {"name": "async_function", "is_async": True}

        code = await generative_ai.generate_code_async("function", async_info)

        assert isinstance(code, str)
        assert "async def async_function" in code

    def test_get_code_statistics(self, generative_ai):
        """Test de récupération des statistiques de code"""
        stats = generative_ai.get_code_statistics()

        assert isinstance(stats, dict)
        assert "total_modules" in stats
        assert "total_lines" in stats
        assert "average_complexity" in stats

    def test_export_analysis_report(self, generative_ai):
        """Test d'export du rapport d'analyse"""
        mock_analysis = {"modules": [], "patterns": []}
        with (
            patch.object(generative_ai, "analyze_codebase", return_value=mock_analysis),
            patch("builtins.open", mock_open()) as mock_file,
        ):
            generative_ai.export_analysis_report("test_report.json")
            mock_file.assert_called_once_with("test_report.json", "w")

    def test_import_analysis_report(self, generative_ai):
        """Test d'import du rapport d'analyse"""
        mock_data = {"modules": [], "patterns": []}
        with (
            patch("builtins.open", mock_open(read_data=str(mock_data))),
            patch("json.load", return_value=mock_data),
        ):
            data = generative_ai.import_analysis_report("test_report.json")
            assert data == mock_data


class TestGenerativeAIIntegration:
    """Tests d'intégration pour GenerativeAI"""

    @pytest.mark.asyncio
    async def test_full_code_generation_workflow(self):
        """Test du workflow complet de génération de code"""
        generative_ai = GenerativeAI()

        # 1. Analyse de la base de code
        analysis = generative_ai.analyze_codebase()

        # 2. Génération de code pour un module manquant
        module_info = {"class_name": "NewModule", "module_name": "new_module"}

        code = generative_ai.generate_code("class", module_info)

        # 3. Génération de tests
        test_info = {
            "module_name": "new_module",
            "class_name": "NewModule",
            "function_name": "process_data",
        }

        test_code = generative_ai.generate_test("unit", test_info)

        # Vérifications
        assert "class NewModule" in code
        assert "def test_process_data" in test_code

    @pytest.mark.asyncio
    async def test_integration_with_existing_modules(self):
        """Test d'intégration avec les modules existants"""
        generative_ai = GenerativeAI()

        # Simulation d'analyse des modules existants
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.rglob") as mock_rglob,
        ):

            mock_files = [MagicMock(name="zeroia.py"), MagicMock(name="reflexia.py")]
            mock_rglob.return_value = mock_files

            analysis = generative_ai.analyze_codebase()

            # Génération de tests pour les modules existants
            for module in analysis["modules"]:
                if module.get("name"):
                    test_info = {
                        "module_name": module["name"],
                        "class_name": "TestClass",
                        "function_name": "test_method",
                    }

                    test_code = generative_ai.generate_test("unit", test_info)
                    assert "def test_test_method" in test_code


class TestGenerativeAIRobustness:
    """Tests de robustesse pour GenerativeAI"""

    def test_handle_large_codebase(self):
        """Test de gestion d'une grande base de code"""
        generative_ai = GenerativeAI()

        # Simulation d'une grande base de code
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.rglob") as mock_rglob,
        ):

            # Création de nombreux fichiers mock
            mock_files = [MagicMock(name=f"module_{i}.py") for i in range(1000)]
            mock_rglob.return_value = mock_files

            # L'analyse ne devrait pas planter
            analysis = generative_ai.analyze_codebase()

            assert isinstance(analysis, dict)
            assert len(analysis["modules"]) <= 1000

    def test_handle_corrupted_files(self):
        """Test de gestion de fichiers corrompus"""
        generative_ai = GenerativeAI()

        mock_file = MagicMock()
        mock_file.name = "corrupted.py"
        mock_file.read_text.side_effect = UnicodeDecodeError("utf-8", b"", 0, 1, "corrupted")

        # L'analyse devrait gérer l'erreur gracieusement
        module_info = generative_ai._analyze_module(mock_file)

        assert isinstance(module_info, dict)
        assert "error" in module_info

    def test_handle_missing_templates(self):
        """Test de gestion de templates manquants"""
        generative_ai = GenerativeAI()

        # Test avec des templates manquants
        with patch.object(generative_ai, "_load_code_templates", return_value={}):
            code = generative_ai.generate_code("class", {"name": "Test"})

            # Devrait retourner un code par défaut
            assert isinstance(code, str)
            assert len(code) > 0

    def test_handle_invalid_template_data(self):
        """Test de gestion de données de template invalides"""
        generative_ai = GenerativeAI()

        # Test avec des données invalides
        invalid_info = None

        code = generative_ai.generate_code("class", invalid_info)

        # Devrait gérer l'erreur gracieusement
        assert isinstance(code, str)

    def test_performance_optimization(self):
        """Test d'optimisation des performances"""
        generative_ai = GenerativeAI()

        import time

        start_time = time.time()

        # Génération de nombreux tests
        for i in range(100):
            test_info = {
                "module_name": f"module_{i}",
                "class_name": f"Class_{i}",
                "function_name": f"method_{i}",
            }
            generative_ai.generate_test("unit", test_info)

        end_time = time.time()
        generation_time = end_time - start_time

        # La génération devrait être rapide (< 10 secondes)
        assert generation_time < 10.0

    def test_memory_usage_optimization(self):
        """Test d'optimisation de l'utilisation mémoire"""
        generative_ai = GenerativeAI()

        import os

        import psutil

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        # Génération intensive
        for i in range(1000):
            test_info = {
                "module_name": f"module_{i}",
                "class_name": f"Class_{i}",
                "function_name": f"method_{i}",
            }
            generative_ai.generate_test("unit", test_info)

        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory

        # L'augmentation mémoire devrait être raisonnable (< 100MB)
        assert memory_increase < 100 * 1024 * 1024


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
