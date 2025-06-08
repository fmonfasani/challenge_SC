import pytest
import respx
import httpx
from app.services.beneficios_service import BeneficiosService
from fastapi import HTTPException

# Mock de datos de prueba
fake_beneficios = [
    {
        "id": 1,
        "name": "Beneficio Mock",
        "description": "Descripción del beneficio",
        "image": "https://via.placeholder.com/150",
        "status": "active",
        "fullDescription": "Descripción completa del beneficio",
        "category": "Deporte",
        "validUntil": "2025-12-31"
    }
]

fake_beneficio = fake_beneficios[0]

@pytest.mark.asyncio
async def test_get_all_beneficios_success():
    service = BeneficiosService()
    with respx.mock:
        respx.get(f"{service.base_url}beneficios").mock(return_value=httpx.Response(200, json=fake_beneficios))
        response = await service.get_all_beneficios()
        assert response.total == 1
        assert response.beneficios[0].id == 1

@pytest.mark.asyncio
async def test_get_beneficio_by_id_success():
    service = BeneficiosService()
    with respx.mock:
        respx.get(f"{service.base_url}beneficios/1").mock(return_value=httpx.Response(200, json=fake_beneficio))
        response = await service.get_beneficio_by_id(1)
        assert response.id == 1
        assert response.name == "Beneficio Mock"

@pytest.mark.asyncio
async def test_get_beneficio_by_id_not_found():
    service = BeneficiosService()
    with respx.mock:
        respx.get(f"{service.base_url}beneficios/9999").mock(return_value=httpx.Response(404))
        with pytest.raises(HTTPException) as excinfo:
            await service.get_beneficio_by_id(9999)
        assert excinfo.value.status_code == 404
