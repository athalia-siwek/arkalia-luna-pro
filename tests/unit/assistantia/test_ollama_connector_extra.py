import pytest
import requests

from modules.assistantia.utils import ollama_connector


def test_query_ollama_function_exists():
    assert hasattr(ollama_connector, "query_ollama")


def test_query_ollama_invalid_model():
    with pytest.raises(ValueError):
        ollama_connector.query_ollama("prompt", model="model-inconnu")


def test_query_ollama_bad_model():
    with pytest.raises(ValueError):
        ollama_connector.query_ollama("prompt", model="inconnu")


def test_query_ollama_empty_prompt():
    response = ollama_connector.query_ollama("", model="mistral")
    assert isinstance(response, str)
    assert response == "[⚠️ Réponse IA vide]"  # ou un autre message d'erreur approprié


def test_query_ollama_valid_prompt():
    response = ollama_connector.query_ollama("Hello", model="mistral")
    assert isinstance(response, str)
    assert response != "[⚠️ Réponse IA vide]"


def test_query_ollama_network_error(monkeypatch):
    def mock_post(*args, **kwargs):
        raise requests.exceptions.ConnectionError

    monkeypatch.setattr("requests.post", mock_post)

    response = ollama_connector.query_ollama("Hello", model="mistral")
    assert "Erreur IA" in response


def test_query_ollama_timeout(monkeypatch):
    def mock_post(*args, **kwargs):
        raise requests.exceptions.Timeout

    monkeypatch.setattr("requests.post", mock_post)

    response = ollama_connector.query_ollama("Hello", model="mistral")
    assert "Erreur IA" in response


def test_query_ollama_http_error(monkeypatch):
    class MockResponse:
        def __init__(self, status_code):
            self.status_code = status_code
            self.text = "Error"

        def json(self):
            return {}

    def mock_post(*args, **kwargs):
        return MockResponse(500)

    monkeypatch.setattr("requests.post", mock_post)

    response = ollama_connector.query_ollama("Hello", model="mistral")
    assert "Erreur IA" in response
