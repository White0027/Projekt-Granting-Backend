import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_reference_classification():
    async with AsyncClient(app=app, base_url="http://localhost:8125") as client:
        response = await client.post("/oauth/login3", json={"username": "test", "password": "test"})
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Login successful"

        # Test invalid credentials
        response = await client.post("/oauth/login3", json={"username": "wrong", "password": "wrong"})
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Invalid credentials"