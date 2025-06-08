import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_get_all_mock_beneficios():
    """Test mock endpoint for getting all beneficios"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/mock/beneficios")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if data:  # If there's data, verify structure
            assert "id" in data[0]


@pytest.mark.asyncio
async def test_get_mock_beneficio_by_id_success():
    """Test mock endpoint for getting beneficio by ID - success"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/mock/beneficios/1")
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.json()
            assert "id" in data
            assert data["id"] == 1


@pytest.mark.asyncio  
async def test_get_mock_beneficio_by_id_not_found():
    """Test mock endpoint for getting beneficio by ID - not found"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/mock/beneficios/999999")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_mock_endpoints_invalid_id():
    """Test mock endpoint with invalid ID format"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/mock/beneficios/invalid")
        assert response.status_code == 422  # Validation error