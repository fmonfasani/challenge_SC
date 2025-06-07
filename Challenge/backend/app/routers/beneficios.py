from fastapi import APIRouter, Path, HTTPException
from app.services.beneficios_service import beneficios_service
from app.schemas.beneficio import BeneficioResponse, BeneficioListResponse

router = APIRouter(prefix="/beneficios", tags=["beneficios"])

@router.get("", response_model=BeneficioListResponse)
async def get_beneficios():
    return await beneficios_service.get_all_beneficios()

@router.get("/{beneficio_id}", response_model=BeneficioResponse)
async def get_beneficio_by_id(beneficio_id: int = Path(..., gt=0)):
    return await beneficios_service.get_beneficio_by_id(beneficio_id)
