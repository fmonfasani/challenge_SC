# app/interfaces/routers/routers.py

from fastapi import APIRouter, Path, Depends, Request, HTTPException
from slowapi.util import get_remote_address
from app.interfaces.schemas.schemas import BeneficioResponse, BeneficioListResponse, ErrorResponse
from app.application.services import BeneficiosService
from app.infrastructure.repositories import ExternalBeneficioRepository
from app.interfaces.middlewares import limiter  

# Dependency function
def get_beneficio_service() -> BeneficiosService:
    repository = ExternalBeneficioRepository()
    return BeneficiosService(repository)

router = APIRouter(prefix="/api/beneficios", tags=["beneficios"])

@router.get("", response_model=BeneficioListResponse, responses={
    500: {"model": ErrorResponse, "description": "Error interno del servidor"}
})
@limiter.limit("10/minute")
async def get_beneficios(
    request: Request,
    service: BeneficiosService = Depends(get_beneficio_service)
):
    """Obtiene todos los beneficios disponibles"""
    try:
        beneficios_list = await service.get_all_beneficios()
        return BeneficioListResponse.from_domain(beneficios_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo beneficios: {str(e)}")

@router.get("/{beneficio_id}", response_model=BeneficioResponse, responses={
    404: {"model": ErrorResponse, "description": "Beneficio no encontrado"},
    500: {"model": ErrorResponse, "description": "Error interno del servidor"}
})
@limiter.limit("30/minute")
async def get_beneficio_by_id(
    request: Request,
    beneficio_id: int = Path(..., gt=0, description="ID del beneficio"),
    service: BeneficiosService = Depends(get_beneficio_service)
):
    """Obtiene un beneficio específico por su ID"""
    try:
        beneficio = await service.get_beneficio_by_id(beneficio_id)
        if beneficio is None:
            raise HTTPException(status_code=404, detail="Beneficio no encontrado")
        return BeneficioResponse.from_domain(beneficio)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo beneficio: {str(e)}")