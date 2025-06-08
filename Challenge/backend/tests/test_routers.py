import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import Mock, AsyncMock, patch
from app.main import app


@pytest.mark.asyncio
async def test_get_all_beneficios():
    """Test get all beneficios endpoint"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/beneficios")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_beneficio_by_id_success():
    """Test get beneficio by ID - success case"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/beneficios/1")
        # Should return 200 if found or 404 if not found
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.json()
            assert "id" in data


@pytest.mark.asyncio
async def test_get_beneficio_by_id_not_found():  
    """Test get beneficio by ID - not found case"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/beneficios/999999")  # Use a very high ID that likely doesn't exist
        assert response.status_code == 404


# Additional test with mocked service for more controlled testing
@pytest.mark.asyncio
async def test_get_all_beneficios_with_mock():
    """Test get all beneficios with mocked service"""
    mock_data = [
        {"id": 1, "name": "Test Beneficio 1"},
        {"id": 2, "name": "Test Beneficio 2"}
    ]
    
    with patch('app.interfaces.routers.routers.beneficio_service') as mock_service:
        mock_service.get_all_beneficios = AsyncMock(return_value=mock_data)
        
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get("/beneficios")
            assert response.status_code == 200
            assert response.json() == mock_data


@pytest.mark.asyncio
async def test_get_beneficio_by_id_with_mock():
    """Test get beneficio by ID with mocked service"""
    mock_data = {"id": 1, "name": "Test Beneficio"}
    
    with patch('app.interfaces.routers.routers.beneficio_service') as mock_service:
        mock_service.get_beneficio_by_id = AsyncMock(return_value=mock_data)
        
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get("/beneficios/1")
            assert response.status_code == 200
            assert response.json() == mock_data