import pytest
import requests
from fastapi.testclient import TestClient

from modules.assistantia.core import app, get_query_ollama


def override_success(msg: str, model: str = "mistral") -> str:
    return msg


def override_timeout(*args, **kwargs):
    raise requests.exceptions.Timeout()


@pytest.fixture
def test_client():
    return TestClient(app)


def test_chat_post_ok(test_client):
    app.dependency_overrides[get_query_ollama] = lambda: override_success
    try:
        res = test_client.post("/chat", json={"message": "Hello"})
        # nosec: assert_used
        assert res.status_code == 200
        # nosec: assert_used
        assert res.json()["réponse"] == "Tu as dit : Hello"
    finally:
        app.dependency_overrides.clear()


def test_chat_post_empty(test_client):
    res = test_client.post("/chat", json={"message": ""})
    # nosec: assert_used
    assert res.status_code == 400
    # nosec: assert_used
    assert "Message vide" in res.json()["detail"]


def test_chat_post_bad_payload(test_client):
    res = test_client.post("/chat", json={"msg": "Hello"})
    # nosec: assert_used
    assert res.status_code == 422


def test_chat_post_timeout(test_client):
    app.dependency_overrides[get_query_ollama] = lambda: override_timeout
    try:
        res = test_client.post("/chat", json={"message": "Hello"})
        # nosec: assert_used
        assert res.status_code == 500
        # nosec: assert_used
        assert "délai" in res.json()["detail"].lower()
    finally:
        app.dependency_overrides.clear()
