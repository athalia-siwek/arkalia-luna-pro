import pytest
from httpx import ASGITransport, AsyncClient

from modules.assistantia.core import app

pytestmark = pytest.mark.asyncio


@pytest.mark.asyncio
async def test_chat_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/chat", json={"message": "Bonjour"})
        assert response.status_code == 200
        data = response.json()
        assert "réponse" in data
        assert isinstance(data["réponse"], str)
        assert len(data["réponse"]) > 3


@pytest.mark.asyncio
async def test_post_chat_empty_payload():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/chat", json={})
        assert response.status_code == 422
