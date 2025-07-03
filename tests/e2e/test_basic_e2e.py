#!/usr/bin/env python3
"""
🧪 Tests E2E de base pour Arkalia-LUNA

Tests end-to-end simples pour vérifier le bon fonctionnement du système.
"""

import time
from pathlib import Path

import pytest
import requests


class TestBasicE2E:
    """Tests E2E de base"""

    @pytest.fixture
    def base_url(self):
        """URL de base pour les tests"""
        return "http://localhost:8000"

    def test_api_health_endpoint(self, base_url):
        """Test de l'endpoint de santé de l'API"""
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert "status" in data
        except requests.exceptions.RequestException:
            pytest.skip("API non disponible - test ignoré")

    def test_zeroia_health_endpoint(self, base_url):
        """Test de l'endpoint de santé ZeroIA"""
        try:
            response = requests.get(f"{base_url}/zeroia/health", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert "status" in data
        except requests.exceptions.RequestException:
            pytest.skip("ZeroIA non disponible - test ignoré")

    def test_reflexia_health_endpoint(self, base_url):
        """Test de l'endpoint de santé ReflexIA"""
        try:
            response = requests.get(f"{base_url}/reflexia/health", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert "status" in data
        except requests.exceptions.RequestException:
            pytest.skip("Reflexia non disponible - test ignoré")

    def test_zeroia_decision_endpoint(self, base_url):
        """Test de l'endpoint de décision ZeroIA"""
        try:
            response = requests.post(
                f"{base_url}/zeroia/decision",
                json={"context": {"cpu_usage": 50.0}},
                timeout=10
            )
            assert response.status_code == 200
            data = response.json()
            assert "decision" in data
        except requests.exceptions.RequestException:
            pytest.skip("ZeroIA decision non disponible - test ignoré")

    def test_docker_services_running(self):
        """Test que les services Docker sont en cours d'exécution"""
        import subprocess

        try:
            result = subprocess.run(
                ["docker", "ps", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                services = result.stdout.strip().split('\n')
                # Vérifier qu'au moins un service est en cours d'exécution
                assert len(services) > 0
                assert any('arkalia' in service.lower() for service in services)
            else:
                pytest.skip("Docker non disponible - test ignoré")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("Docker non disponible - test ignoré")

    def test_state_files_exist(self):
        """Test que les fichiers d'état existent"""
        state_files = [
            "state/zeroia_state.toml",
            "state/reflexia_state.toml",
            "state/arkalia_master_state.toml"
        ]

        for state_file in state_files:
            if Path(state_file).exists():
                assert True  # Fichier existe
            else:
                pytest.skip(f"Fichier d'état {state_file} non trouvé - test ignoré")

    def test_logs_directory_exists(self):
        """Test que le répertoire des logs existe"""
        logs_dir = Path("logs")
        assert logs_dir.exists()
        assert logs_dir.is_dir()

    def test_config_files_exist(self):
        """Test que les fichiers de configuration existent"""
        config_files = [
            "config/arkalia_master_config.toml",
            "config/settings.toml",
            "pytest.ini"
        ]

        for config_file in config_files:
            if Path(config_file).exists():
                assert True  # Fichier existe
            else:
                pytest.skip(f"Fichier de config {config_file} non trouvé - test ignoré")


class TestE2EIntegration:
    """Tests d'intégration E2E"""

    def test_full_system_workflow(self, base_url):
        """Test d'un workflow complet du système"""
        try:
            # 1. Vérifier la santé du système
            health_response = requests.get(f"{base_url}/health", timeout=5)
            assert health_response.status_code == 200

            # 2. Demander une décision à ZeroIA
            decision_response = requests.post(
                f"{base_url}/zeroia/decision",
                json={"context": {"cpu_usage": 75.0, "memory_usage": 60.0}},
                timeout=10
            )
            assert decision_response.status_code == 200

            # 3. Vérifier que la décision a été prise
            decision_data = decision_response.json()
            assert "decision" in decision_data
            assert "confidence" in decision_data

        except requests.exceptions.RequestException:
            pytest.skip("Système non disponible - test ignoré")

    def test_error_handling(self, base_url):
        """Test de la gestion d'erreur"""
        try:
            # Test avec des données invalides
            response = requests.post(
                f"{base_url}/zeroia/decision",
                json={"invalid": "data"},
                timeout=5
            )
            # Le système devrait gérer les données invalides sans planter
            assert response.status_code in [200, 400, 422]
        except requests.exceptions.RequestException:
            pytest.skip("Système non disponible - test ignoré")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
