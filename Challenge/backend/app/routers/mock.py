from fastapi import APIRouter
from fastapi import HTTPException

from typing import List

router = APIRouter(
    prefix="/mock",
    tags=["Mock"]
)

# Fake data
FAKE_BENEFICIOS = [
    {
        "id": 1,
        "nombre": "Descuento en gimnasio",
        "descripcion": "20% de descuento en membresía mensual",
        "estado": "activo",
        "imagen": "https://via.placeholder.com/150"
    },
    {
        "id": 2,
        "nombre": "Descuento en cine",
        "descripcion": "2x1 en entradas de cine",
        "estado": "inactivo",
        "imagen": "https://via.placeholder.com/150"
    },
    {
        "id": 3,
        "nombre": "Descuento en restaurante",
        "descripcion": "15% de descuento en consumos",
        "estado": "activo",
        "imagen": "https://via.placeholder.com/150"
    }
]

@router.get("/beneficios")
async def get_mock_beneficios():
    return FAKE_BENEFICIOS

@router.get("/beneficios/{beneficio_id}")
async def get_beneficio_by_id(beneficio_id: int):
    beneficio = next((b for b in FAKE_BENEFICIOS if b["id"] == beneficio_id), None)
    if not beneficio:
        raise HTTPException(status_code=404, detail="Beneficio no encontrado")
    return beneficio