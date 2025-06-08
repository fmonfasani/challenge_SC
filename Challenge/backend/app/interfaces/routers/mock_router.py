# app/interfaces/routers/mock_router.py

from fastapi import APIRouter, HTTPException, Path
from typing import List, Dict, Any

# Router para endpoints mock
mock_router = APIRouter(prefix="/mock", tags=["mock"])

# Datos mock para testing
MOCK_BENEFICIOS = [
    {
        "id": 1,
        "name": "Descuento Gimnasio",
        "description": "20% de descuento en gimnasios afiliados",
        "image": "https://via.placeholder.com/150",
        "status": "active",
        "fullDescription": "Obtén un 20% de descuento en más de 100 gimnasios afiliados en toda la ciudad. Válido para membresías anuales y mensuales.",
        "category": "Deporte",
        "validUntil": "2025-12-31"
    },
    {
        "id": 2,
        "name": "Descuento Restaurantes",
        "description": "15% de descuento en restaurantes seleccionados",
        "image": "https://via.placeholder.com/150",
        "status": "active",
        "fullDescription": "Disfruta de un 15% de descuento en más de 50 restaurantes seleccionados. No válido en bebidas alcohólicas.",
        "category": "Gastronomía",
        "validUntil": "2025-12-31"
    },
    {
        "id": 3,
        "name": "Descuento Cine",
        "description": "2x1 en entradas de cine los miércoles",
        "image": "https://via.placeholder.com/150",
        "status": "inactive",
        "fullDescription": "Promoción 2x1 en entradas de cine todos los miércoles en cines participantes. No válido en estrenos.",
        "category": "Entretenimiento",
        "validUntil": "2025-06-30"
    }
]

@mock_router.get("/beneficios", response_model=List[Dict[str, Any]])
async def get_mock_beneficios():
    """
    Endpoint mock para obtener todos los beneficios
    """
    return MOCK_BENEFICIOS

@mock_router.get("/beneficios/{beneficio_id}", response_model=Dict[str, Any])
async def get_mock_beneficio_by_id(
    beneficio_id: int = Path(..., gt=0, description="ID del beneficio")
):
    """
    Endpoint mock para obtener un beneficio por ID
    """
    beneficio = next((b for b in MOCK_BENEFICIOS if b["id"] == beneficio_id), None)
    
    if not beneficio:
        raise HTTPException(status_code=404, detail="Beneficio no encontrado")
    
    return beneficio