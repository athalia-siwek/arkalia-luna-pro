# 📋 tests/unit/test_taskia_core.py
"""
Tests unitaires pour le module taskia/core.py
Arkalia-LUNA v2.8.0 - Task Management System
"""

from unittest.mock import patch

import pytest

from modules.taskia.core import taskia_main


class TestTaskiaCore:
    """Tests pour le module taskia/core.py"""

    def test_taskia_main_function_exists(self):
        """Test que la fonction taskia_main existe"""
        assert taskia_main is not None
        assert callable(taskia_main)

    def test_taskia_main_basic_functionality(self):
        """Test de la fonctionnalité de base de taskia_main"""
        context = {"module": "zeroia", "status": "active", "data": "test_data"}

        result = taskia_main(context)
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0

    def test_taskia_main_empty_context(self):
        """Test avec contexte vide"""
        context = {}
        result = taskia_main(context)
        assert result is not None
        assert isinstance(result, str)

    def test_taskia_main_complex_context(self):
        """Test avec contexte complexe"""
        context = {
            "modules": {
                "zeroia": {"status": "active", "version": "v2.8.0"},
                "reflexia": {"status": "active", "version": "v2.8.0"},
                "sandozia": {"status": "inactive", "version": "v2.7.0"},
            },
            "system": {"cpu_usage": 75, "memory_usage": 60, "disk_usage": 45},
            "timestamp": "2024-01-15T10:30:00Z",
        }

        result = taskia_main(context)
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0

    def test_taskia_main_with_formatter_mock(self):
        """Test avec mock du formateur"""
        with patch("modules.taskia.core.format_summary") as mock_format:
            mock_format.return_value = "Mocked summary result"

            context = {"test": "data"}
            result = taskia_main(context)

            assert result == "Mocked summary result"
            mock_format.assert_called_once_with(context)

    def test_taskia_main_error_handling(self):
        """Test de gestion d'erreurs"""
        with patch("modules.taskia.core.format_summary") as mock_format:
            mock_format.side_effect = ValueError("Format error")

            context = {"test": "data"}
            with pytest.raises(ValueError):
                taskia_main(context)


class TestTaskiaCoreIntegration:
    """Tests d'intégration pour taskia/core.py"""

    def test_taskia_main_real_context(self):
        """Test avec contexte réel"""
        context = {
            "task": "system_analysis",
            "priority": "high",
            "parameters": {
                "modules": ["zeroia", "reflexia", "sandozia"],
                "metrics": ["cpu", "memory", "disk"],
            },
        }

        result = taskia_main(context)
        assert result is not None
        assert isinstance(result, str)

    def test_taskia_main_performance(self):
        """Test de performance"""
        import time

        context = {"test": "performance"}
        start_time = time.time()

        result = taskia_main(context)

        end_time = time.time()
        execution_time = end_time - start_time

        assert result is not None
        assert execution_time < 1.0  # Doit s'exécuter en moins d'1 seconde


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
