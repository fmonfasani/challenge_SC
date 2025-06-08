import pytest
from httpx import AsyncClient
from app.main import app  # Asegurate que sea la ruta correcta a tu FastAPI app

@pytest.mark.asyncio
async def test_get_all_mock_beneficios():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/mock/beneficios")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0  # Esperamos al menos algunos beneficios
    assert "name" in data[0]
    assert "description" in data[0]
    assert "status" in data[0]

@pytest.mark.asyncio
async def test_get_mock_beneficio_by_id_success():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/mock/beneficios/1")  # ID que sabemos que existe
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    assert "fullDescription" in data

@pytest.mark.asyncio
async def test_get_mock_beneficio_by_id_not_found():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/mock/beneficios/9999")  # ID que no existe
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Beneficio no encontrado"
