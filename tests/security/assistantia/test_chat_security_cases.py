from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from modules.assistantia.core import app

client = TestClient(app)


def test_chat_sql_injection_like():
    """Teste la protection contre les tentatives d'injection SQL-like"""
    payload = {"message": "'; DROP TABLE users; --"}
    with patch("modules.assistantia.core.real_query_ollama", return_value="Message sécurisé"):
        response = client.post("/chat", json=payload)
        assert response.status_code == 200
        assert "réponse" in response.json()
