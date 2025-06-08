import httpx
import logging
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from app.schemas.beneficio import BeneficioListResponse, BeneficioResponse, normalize_beneficio_data

load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BeneficiosService:
    def __init__(self):
        self.base_url = os.getenv("API_BASE_URL", "http://localhost:8000/api/mock/beneficios")

    async def get_all_beneficios(self):
        logger.info(f"Requesting all beneficios from {self.base_url}")
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.base_url, timeout=10)
                response.raise_for_status()
                logger.info(f"Response [status {response.status_code}]: {response.text[:500]}")  # Log primeras 500 chars
                beneficios_data = response.json()
                beneficios = [normalize_beneficio_data(b) for b in beneficios_data]
                return BeneficioListResponse(beneficios=beneficios, total=len(beneficios))
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error while fetching beneficios: {e.response.status_code} - {e.response.text}")
                raise HTTPException(status_code=e.response.status_code, detail="Error externo")
            except Exception as e:
                logger.error(f"Unexpected error while fetching beneficios: {str(e)}")
                raise HTTPException(status_code=500, detail="Internal Server Error")

    async def get_beneficio_by_id(self, beneficio_id: int):
        url = f"{self.base_url}/{beneficio_id}"
        logger.info(f"Requesting beneficio {beneficio_id} from {url}")
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=10)
                if response.status_code == 404:
                    logger.warning(f"Beneficio {beneficio_id} not found")
                    raise HTTPException(status_code=404, detail="Beneficio no encontrado")
                response.raise_for_status()
                logger.info(f"Response [status {response.status_code}]: {response.text[:500]}")
                beneficio_data = response.json()
                return BeneficioResponse(**normalize_beneficio_data(beneficio_data))
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error while fetching beneficio {beneficio_id}: {e.response.status_code} - {e.response.text}")
                raise HTTPException(status_code=e.response.status_code, detail="Error externo")
            except Exception as e:
                logger.error(f"Unexpected error while fetching beneficio {beneficio_id}: {str(e)}")
                raise HTTPException(status_code=500, detail="Internal Server Error")

beneficios_service = BeneficiosService()
