import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


class TestBeneficiosIntegration:
    
    @pytest.mark.asyncio
    async def test_get_all_beneficios_integration(self):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/beneficios")
            assert response.status_code == 200
            assert isinstance(response.json(), list)

    @pytest.mark.asyncio  
    async def test_get_beneficio_by_id_integration(self):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/beneficios/1")
            assert response.status_code in [200, 404]
            if response.status_code == 200:
                assert "id" in response.json()

    @pytest.mark.asyncio
    async def test_invalid_beneficio_id_integration(self):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/beneficios/invalid")
            assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_health_endpoint(self):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/health")
            assert response.status_code == 200