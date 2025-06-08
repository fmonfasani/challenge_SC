import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
class TestBeneficiosIntegration:
    
    async def test_get_all_beneficios_integration(self):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/beneficios")
            assert response.status_code == 200
            data = response.json()
            assert "beneficios" in data
            assert "total" in data
            assert isinstance(data["beneficios"], list)

    async def test_get_beneficio_by_id_integration(self):
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Test with mock data
            response = await client.get("/api/beneficios/1")
            if response.status_code == 200:
                data = response.json()
                assert data["id"] == 1
                assert "name" in data
                assert "description" in data

    async def test_invalid_beneficio_id_integration(self):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/beneficios/0")
            assert response.status_code == 422  # Validation error

    async def test_health_endpoint(self):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"