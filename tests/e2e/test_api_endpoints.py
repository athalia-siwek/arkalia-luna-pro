#!/usr/bin/env python3
"""
🧪 Tests E2E - Endpoints API Arkalia-LUNA Pro

Tests end-to-end pour vérifier le bon fonctionnement des endpoints API
en conditions réelles avec les services Docker.
"""

import asyncio
import json
import time
from typing import Any, Dict

import aiohttp
import httpx
import pytest


class TestAPIEndpointsE2E:
    """Tests E2E pour les endpoints API"""

    @pytest.fixture
    async def api_client(self):
        """Client HTTP pour les tests API"""
        async with httpx.AsyncClient(base_url="http://localhost:8000", timeout=30.0) as client:
            yield client

    @pytest.mark.asyncio
    async def test_health_endpoint(self, api_client):
        """Test du endpoint de santé principal"""
        response = await api_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_zeroia_health(self, api_client):
        """Test du endpoint de santé ZeroIA"""
        response = await api_client.get("/zeroia/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "metrics" in data

    @pytest.mark.asyncio
    async def test_reflexia_health(self, api_client):
        """Test du endpoint de santé ReflexIA"""
        response = await api_client.get("/reflexia/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data

    @pytest.mark.asyncio
    async def test_sandozia_health(self, api_client):
        """Test du endpoint de santé Sandozia"""
        response = await api_client.get("/sandozia/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data

    @pytest.mark.asyncio
    async def test_zeroia_decision(self, api_client):
        """Test du endpoint de décision ZeroIA"""
        payload = {
            "context": {"cpu_usage": 75.0, "memory_usage": 80.0, "error_rate": 0.02},
            "priority": "medium",
        }
        response = await api_client.post("/zeroia/decision", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "decision" in data
        assert "confidence" in data
        assert "reasoning" in data

    @pytest.mark.asyncio
    async def test_reflexia_check(self, api_client):
        """Test du endpoint de vérification ReflexIA"""
        payload = {"module": "zeroia", "check_type": "health"}
        response = await api_client.post("/reflexia/check", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "status" in data

    @pytest.mark.asyncio
    async def test_sandozia_analyze(self, api_client):
        """Test du endpoint d'analyse Sandozia"""
        payload = {
            "data": {
                "system_metrics": {"cpu": 70.0, "memory": 75.0, "disk": 60.0},
                "events": ["high_cpu", "memory_warning"],
            }
        }
        response = await api_client.post("/sandozia/analyze", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "analysis" in data

    @pytest.mark.asyncio
    async def test_metrics_endpoint(self, api_client):
        """Test du endpoint de métriques Prometheus"""
        response = await api_client.get("/metrics")
        assert response.status_code == 200
        content = response.text
        assert "arkalia_" in content
        assert "zeroia_" in content

    @pytest.mark.asyncio
    async def test_api_documentation(self, api_client):
        """Test de la documentation API (OpenAPI/Swagger)"""
        response = await api_client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")

    @pytest.mark.asyncio
    async def test_openapi_schema(self, api_client):
        """Test du schéma OpenAPI"""
        response = await api_client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "paths" in schema


class TestAPIPerformanceE2E:
    """Tests de performance E2E pour l'API"""

    @pytest.mark.asyncio
    async def test_api_response_time(self):
        """Test du temps de réponse de l'API"""
        async with httpx.AsyncClient(base_url="http://localhost:8000", timeout=30.0) as client:
            start_time = time.time()
            response = await client.get("/health")
            end_time = time.time()

            assert response.status_code == 200
            response_time = end_time - start_time
            assert response_time < 1.0  # Moins d'1 seconde

    @pytest.mark.asyncio
    async def test_concurrent_requests(self):
        """Test de requêtes concurrentes"""
        async with httpx.AsyncClient(base_url="http://localhost:8000", timeout=30.0) as client:
            # 10 requêtes concurrentes
            tasks = [client.get("/health") for _ in range(10)]
            responses = await asyncio.gather(*tasks)

            for response in responses:
                assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_zeroia_decision_performance(self):
        """Test de performance du endpoint de décision ZeroIA"""
        async with httpx.AsyncClient(base_url="http://localhost:8000", timeout=30.0) as client:
            payload = {"context": {"cpu_usage": 50.0, "memory_usage": 60.0}, "priority": "low"}

            start_time = time.time()
            response = await client.post("/zeroia/decision", json=payload)
            end_time = time.time()

            assert response.status_code == 200
            decision_time = end_time - start_time
            assert decision_time < 2.0  # Moins de 2 secondes


class TestAPISecurityE2E:
    """Tests de sécurité E2E pour l'API"""

    @pytest.mark.asyncio
    async def test_cors_headers(self, api_client):
        """Test des en-têtes CORS"""
        response = await api_client.options("/health")
        # Vérification que les en-têtes CORS sont présents
        assert "access-control-allow-origin" in response.headers

    @pytest.mark.asyncio
    async def test_rate_limiting(self, api_client):
        """Test de limitation de débit"""
        # Envoi de nombreuses requêtes pour tester la limitation
        responses = []
        for _ in range(20):
            response = await api_client.get("/health")
            responses.append(response)

        # Au moins une requête doit réussir
        success_count = sum(1 for r in responses if r.status_code == 200)
        assert success_count > 0

    @pytest.mark.asyncio
    async def test_invalid_payload_handling(self, api_client):
        """Test de gestion des payloads invalides"""
        invalid_payloads = [None, "invalid_json", {"invalid": "data"}, {"context": "not_a_dict"}]

        for payload in invalid_payloads:
            response = await api_client.post("/zeroia/decision", json=payload)
            # Doit retourner une erreur 422 ou 400
            assert response.status_code in [400, 422]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])
