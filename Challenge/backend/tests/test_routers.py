import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import Mock, AsyncMock, patch
from app.main import app


@pytest.mark.asyncio
async def test_get_all_beneficios():
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/beneficios") 
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "beneficios" in data
        assert "total" in data
        assert isinstance(data["beneficios"], list)


@pytest.mark.asyncio
async def test_get_beneficio_by_id_success():
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/beneficios/1")  
        
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.json()
            assert "id" in data


@pytest.mark.asyncio
async def test_get_beneficio_by_id_not_found():  
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/beneficios/999999")  #
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_all_beneficios_with_mock():
    
    mock_data = {
        "beneficios": [
            {"id": 1, "name": "Test Beneficio 1", "description": "Test desc", "status": "active"},
            {"id": 2, "name": "Test Beneficio 2", "description": "Test desc", "status": "active"}
        ],
        "total": 2
    }
    
    
    with patch('app.application.services.BeneficiosService.get_all_beneficios') as mock_service:
        from app.domain.models import BeneficiosList, Beneficio, BeneficioStatus
        
        beneficios = [
            Beneficio(id=1, name="Test 1", description="Desc 1", status=BeneficioStatus.ACTIVE),
            Beneficio(id=2, name="Test 2", description="Desc 2", status=BeneficioStatus.ACTIVE)
        ]
        mock_service.return_value = BeneficiosList(beneficios=beneficios, total=2)
        
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get("/api/beneficios")
            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 2
            assert len(data["beneficios"]) == 2


@pytest.mark.asyncio
async def test_get_beneficio_by_id_with_mock():
        
    with patch('app.application.services.BeneficiosService.get_beneficio_by_id') as mock_service:
        from app.domain.models import Beneficio, BeneficioStatus
        
        mock_beneficio = Beneficio(
            id=1, 
            name="Test Beneficio", 
            description="Test desc", 
            status=BeneficioStatus.ACTIVE
        )
        mock_service.return_value = mock_beneficio
        
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get("/api/beneficios/1")
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == 1
            assert data["name"] == "Test Beneficio"