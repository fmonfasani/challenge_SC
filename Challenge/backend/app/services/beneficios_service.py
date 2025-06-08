import os
import httpx
from fastapi import HTTPException
from app.schemas.beneficio import BeneficioListResponse, BeneficioResponse, normalize_beneficio_data
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class BeneficiosService:
    def __init__(self):
        self.base_url = os.getenv("API_BASE_URL", "http://localhost:8000/api/mock")
            
    async def get_all_beneficios(self):
        url = f"{self.base_url}/beneficios"
        logger.info(f"Requesting all beneficios from {url}")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10)
                response.raise_for_status()
                beneficios_data = response.json()
                beneficios = [normalize_beneficio_data(b) for b in beneficios_data]
                return BeneficioListResponse(beneficios=beneficios, total=len(beneficios))
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(status_code=404, detail="Beneficio no encontrado")
            raise HTTPException(status_code=502, detail="Error externo")
        except Exception as e:
            logger.error(f"Unexpected error while fetching beneficios: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def get_beneficio_by_id(self, beneficio_id: int):
        url = f"{self.base_url}/beneficios/{beneficio_id}"
        logger.info(f"Requesting beneficio {beneficio_id} from {url}")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10)
                response.raise_for_status()
                beneficio_data = response.json()
                return BeneficioResponse(**normalize_beneficio_data(beneficio_data))
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(status_code=404, detail="Beneficio no encontrado")
            raise HTTPException(status_code=502, detail="Error externo")
        except Exception as e:
            logger.error(f"Unexpected error while fetching beneficio {beneficio_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

# Crea la instancia aquí y exportala
beneficios_service = BeneficiosService()
