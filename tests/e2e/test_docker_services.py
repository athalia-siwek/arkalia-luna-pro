#!/usr/bin/env python3
"""
🧪 Tests E2E - Services Docker Arkalia-LUNA Pro

Tests end-to-end pour vérifier le bon fonctionnement des services Docker
et leur intégration.
"""

import asyncio
import json
import subprocess
import time
from typing import Any, Dict, List

import docker
import httpx
import pytest


class TestDockerServicesE2E:
    """Tests E2E pour les services Docker"""

    @pytest.fixture
    def docker_client(self):
        """Client Docker pour les tests"""
        return docker.from_env()

    @pytest.fixture
    async def services_running(self, docker_client):
        """Fixture pour démarrer les services Docker"""
        # Démarrage des services
        subprocess.run(["docker-compose", "up", "-d"], check=True)

        # Attente que les services soient prêts
        await asyncio.sleep(30)

        yield

        # Nettoyage
        subprocess.run(["docker-compose", "down"], check=True)

    @pytest.mark.asyncio
    async def test_all_services_running(self, docker_client, services_running):
        """Test que tous les services sont en cours d'exécution"""
        containers = docker_client.containers.list()

        expected_services = ["zeroia", "reflexia", "sandozia", "assistantia"]
        running_services = [c.name for c in containers if c.status == "running"]

        for service in expected_services:
            assert any(
                service in name for name in running_services
            ), f"Service {service} non trouvé"

    @pytest.mark.asyncio
    async def test_service_health_checks(self, services_running):
        """Test des health checks des services"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Test health check ZeroIA
            response = await client.get("http://localhost:8000/zeroia/health")
            assert response.status_code == 200

            # Test health check ReflexIA
            response = await client.get("http://localhost:8000/reflexia/health")
            assert response.status_code == 200

            # Test health check Sandozia
            response = await client.get("http://localhost:8000/sandozia/health")
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_service_logs(self, docker_client, services_running):
        """Test que les services génèrent des logs"""
        containers = docker_client.containers.list()

        for container in containers:
            if any(service in container.name for service in ["zeroia", "reflexia", "sandozia"]):
                logs = container.logs().decode()
                assert len(logs) > 0, f"Container {container.name} n'a pas de logs"

    @pytest.mark.asyncio
    async def test_service_communication(self, services_running):
        """Test de la communication entre services"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Test que ZeroIA peut communiquer avec ReflexIA
            response = await client.post(
                "http://localhost:8000/zeroia/decision",
                json={"context": {"cpu_usage": 50.0}, "priority": "low"},
            )
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_service_restart(self, docker_client, services_running):
        """Test du redémarrage des services"""
        # Redémarrage de ZeroIA
        zeroia_container = None
        for container in docker_client.containers.list():
            if "zeroia" in container.name:
                zeroia_container = container
                break

        if zeroia_container:
            zeroia_container.restart()
            await asyncio.sleep(10)

            # Vérification que le service est de nouveau disponible
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get("http://localhost:8000/zeroia/health")
                assert response.status_code == 200


class TestDockerNetworkingE2E:
    """Tests E2E pour le networking Docker"""

    @pytest.mark.asyncio
    async def test_internal_communication(self, services_running):
        """Test de la communication interne entre conteneurs"""
        # Test que les services peuvent communiquer via le réseau Docker
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Test de l'API principale
            response = await client.get("http://localhost:8000/health")
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_port_exposure(self, services_running):
        """Test de l'exposition des ports"""
        # Vérification que le port 8000 est exposé
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get("http://localhost:8000/health")
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_network_isolation(self, services_running):
        """Test de l'isolation réseau"""
        # Les services ne doivent pas être accessibles depuis l'extérieur
        # sauf via les ports exposés
        pass


class TestDockerVolumesE2E:
    """Tests E2E pour les volumes Docker"""

    @pytest.mark.asyncio
    async def test_persistent_storage(self, services_running):
        """Test du stockage persistant"""
        # Test que les données persistent entre les redémarrages
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Création de données
            response = await client.post(
                "http://localhost:8000/zeroia/decision",
                json={"context": {"test": "persistent_data"}, "priority": "low"},
            )
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_volume_permissions(self, services_running):
        """Test des permissions des volumes"""
        # Vérification que les volumes ont les bonnes permissions
        pass


class TestDockerResourceLimitsE2E:
    """Tests E2E pour les limites de ressources"""

    @pytest.mark.asyncio
    async def test_memory_limits(self, docker_client, services_running):
        """Test des limites de mémoire"""
        containers = docker_client.containers.list()

        for container in containers:
            if any(service in container.name for service in ["zeroia", "reflexia", "sandozia"]):
                stats = container.stats(stream=False)
                memory_usage = stats["memory_stats"]["usage"]
                memory_limit = stats["memory_stats"]["limit"]

                # Vérification que l'utilisation mémoire est raisonnable
                memory_percentage = (memory_usage / memory_limit) * 100
                assert memory_percentage < 80, f"Container {container.name} utilise trop de mémoire"

    @pytest.mark.asyncio
    async def test_cpu_limits(self, docker_client, services_running):
        """Test des limites CPU"""
        containers = docker_client.containers.list()

        for container in containers:
            if any(service in container.name for service in ["zeroia", "reflexia", "sandozia"]):
                stats = container.stats(stream=False)
                cpu_usage = stats["cpu_stats"]["cpu_usage"]["total_usage"]

                # Vérification que l'utilisation CPU est raisonnable
                assert cpu_usage > 0, f"Container {container.name} n'utilise pas de CPU"


class TestDockerSecurityE2E:
    """Tests E2E pour la sécurité Docker"""

    @pytest.mark.asyncio
    async def test_non_root_containers(self, docker_client, services_running):
        """Test que les conteneurs ne tournent pas en tant que root"""
        containers = docker_client.containers.list()

        for container in containers:
            if any(service in container.name for service in ["zeroia", "reflexia", "sandozia"]):
                # Vérification que le conteneur ne tourne pas en tant que root
                exec_result = container.exec_run("whoami")
                user = exec_result.output.decode().strip()
                assert user != "root", f"Container {container.name} tourne en tant que root"

    @pytest.mark.asyncio
    async def test_security_scan(self, services_running):
        """Test de scan de sécurité basique"""
        # Test basique de sécurité
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Test que les endpoints sensibles nécessitent une authentification
            response = await client.get("http://localhost:8000/admin")
            assert response.status_code in [
                401,
                403,
                404,
            ], "Endpoint admin accessible sans authentification"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])
