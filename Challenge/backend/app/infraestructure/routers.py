from fastapi import APIRouter, Path, Depends
from slowapi import Limiter
from slowapi.util import get_remote_address
from .schemas import BeneficioResponse, BeneficioListResponse
from ..application.services import BeneficioService
from ..infrastructure.repositories import ExternalBeneficioRepository

# Dependencies
async def get_beneficio_service() -> BeneficioService:
    repository = ExternalBeneficioRepository()
    return BeneficioService(repository)

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/api/beneficios", tags=["beneficios"])


@router.get("", response_model=BeneficioListResponse)
@limiter.limit("10/minute")
async def get_beneficios(
    request,
    service: BeneficioService = Depends(get_beneficio_service)
):
    beneficios_list = await service.get_all_beneficios()
    return BeneficioListResponse.from_domain(beneficios_list)


@router.get("/{beneficio_id}", response_model=BeneficioResponse)
@limiter.limit("30/minute")
async def get_beneficio_by_id(
    request,
    beneficio_id: int = Path(..., gt=0),
    service: BeneficioService = Depends(get_beneficio_service)
):
    beneficio = await service.get_beneficio_by_id(beneficio_id)
    return BeneficioResponse.from_domain(beneficio)