# tests/test_routers.py

import pytest
from httpx import AsyncClient
from fastapi import FastAPI, HTTPException
from app.interfaces.routers import router  # Importás tu router real
from app.application.services import BeneficioService
from app.domain.models import Beneficio

# Creamos una app de test y montamos el router
app = FastAPI()
app.include_router(router)

# Mock del servicio
class MockBeneficioService:
    async def get_all_beneficios(self):
        return [
            Beneficio(
                id=1,
                name="Mocked Beneficio",
                description="Descripción de prueba",
                image="https://via.placeholder.com/150",
                status="active",
                full_description="Full description",
                category="Deporte",
                valid_until="2025-12-31"
            )
        ]

    async def get_beneficio_by_id(self, beneficio_id: int):
        if beneficio_id == 9999:
            raise HTTPException(status_code=404, detail="Beneficio no encontrado")
        return Beneficio(
            id=beneficio_id,
            name=f"Mocked Beneficio {beneficio_id}",
            description="Descripción de prueba",
            image="https://via.placeholder.com/150",
            status="active",
            full_description="Full description",
            category="Deporte",
            valid_until="2025-12-31"
        )

# Override de la dependencia
from app.interfaces.routers import get_beneficio_service

app.dependency_overrides[get_beneficio_service] = lambda: MockBeneficioService()

# 🚀 Test: obtener todos los beneficios
@pytest.mark.asyncio
async def test_get_all_beneficios():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/beneficios")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["beneficios"], list)
    assert len(data["beneficios"]) == 1
    assert data["beneficios"][0]["id"] == 1
    assert data["beneficios"][0]["name"] == "Mocked Beneficio"

# 🚀 Test: obtener un beneficio por ID (éxito)
@pytest.mark.asyncio
async def test_get_beneficio_by_id_success():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/beneficios/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Mocked Beneficio 1"

# 🚀 Test: obtener un beneficio por ID (no encontrado)
@pytest.mark.asyncio
async def test_get_beneficio_by_id_not_found():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/beneficios/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Beneficio no encontrado"
