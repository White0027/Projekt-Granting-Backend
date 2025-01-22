import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_reference_classification(db_session):
    async with AsyncClient(app=app, base_url="http://localhost:8125") as client:
        # Použití správných přihlašovacích údajů
        response = await client.post("/oauth/login3", json={"username": "test", "password": "test"})
        assert response.status_code == 200
        data = await response.json()
        assert data["message"] == "Logged in successfully"
        assert "token" in data

        # Test invalid credentials
        response = await client.post("/oauth/login3", json={"username": "wrong", "password": "wrong"})
        assert response.status_code == 401
        data = await response.json()
        assert data["detail"] == "Invalid credentials"