from typing import Optional
from fastapi import HTTPException
from ..domain.ports import BeneficioRepository
from ..domain.models import Beneficio, BeneficiosList


class BeneficioService:
    def __init__(self, repository: BeneficioRepository):
        self._repository = repository

    async def get_all_beneficios(self) -> BeneficiosList:
        try:
            return await self._repository.get_all()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching beneficios: {str(e)}")

    async def get_beneficio_by_id(self, beneficio_id: int) -> Beneficio:
        if beneficio_id <= 0:
            raise HTTPException(status_code=400, detail="Invalid beneficio ID")
        
        try:
            beneficio = await self._repository.get_by_id(beneficio_id)
            if not beneficio:
                raise HTTPException(status_code=404, detail="Beneficio not found")
            return beneficio
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching beneficio: {str(e)}")

    async def health_check(self) -> dict:
        return await self._repository.health_check()
class ExternalAPIError(Exception):
    "Error al comunicarse con la API externa"
    pass