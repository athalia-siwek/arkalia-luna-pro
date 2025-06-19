import pytest
from httpx import AsyncClient

from server import app


@pytest.mark.asyncio
async def test_root_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert response.json()["message"] == "Arkalia-LUNA API active"


@pytest.mark.asyncio
async def test_chat_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/chat", json={"message": "Bonjour"})
        assert response.status_code == 200
        assert "réponse" in response.json()
