# app/interfaces/routers.py

from fastapi import APIRouter, Path, Depends, Request
from slowapi.util import get_remote_address
from app.interfaces.schemas.schemas import BeneficioResponse, BeneficioListResponse
from app.application.services import BeneficiosService
from app.infrastructure.repositories import ExternalBeneficioRepository
from app.interfaces.middlewares import limiter  

# Dependency function
def get_beneficio_service() -> BeneficiosService:
    repository = ExternalBeneficioRepository()
    return BeneficiosService(repository)

router = APIRouter(prefix="/api/beneficios", tags=["beneficios"])

@router.get("", response_model=BeneficioListResponse)
@limiter.limit("10/minute")
async def get_beneficios(
    request: Request,
    service: BeneficiosService = Depends(get_beneficio_service)
):
    beneficios_list = await service.get_all_beneficios()
    return BeneficioListResponse.from_domain(beneficios_list)

@router.get("/{beneficio_id}", response_model=BeneficioResponse)
@limiter.limit("30/minute")
async def get_beneficio_by_id(
    request: Request,
    beneficio_id: int = Path(..., gt=0),
    service: BeneficiosService = Depends(get_beneficio_service)
):
    beneficio = await service.get_beneficio_by_id(beneficio_id)
    return BeneficioResponse.from_domain(beneficio)
