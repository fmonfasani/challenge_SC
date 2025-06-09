import os
import asyncio
import httpx
from typing import Optional, List, Dict, Any
import logging
from ..domain.ports import BeneficiosRepositoryPort
from ..domain.models import Beneficio, BeneficiosList, BeneficioStatus

logger = logging.getLogger(__name__)

class ExternalBeneficioRepository(BeneficiosRepositoryPort):
    def __init__(self):
        self.base_url = os.getenv("API_BASE_URL", "http://localhost:8000/api/mock")
        self.timeout = int(os.getenv("REQUEST_TIMEOUT", "10"))
        self.max_retries = int(os.getenv("MAX_RETRIES", "3"))

    async def _make_request(self, url: str, retries: int = 0) -> dict:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=self.timeout)
                response.raise_for_status()
                return response.json()
        except httpx.TimeoutException:
            if retries < self.max_retries:
                await asyncio.sleep(2 ** retries)
                return await self._make_request(url, retries + 1)
            raise
        except httpx.RequestError:
            if retries < self.max_retries:
                await asyncio.sleep(2 ** retries)
                return await self._make_request(url, retries + 1)
            raise

    def _to_domain_model(self, data: Dict[str, Any]) -> Beneficio:
        
        return Beneficio(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            status=BeneficioStatus(data.get("status", "inactive")),
            image=data.get("image"),
            full_description=data.get("fullDescription"),
            category=data.get("category"),
            valid_until=data.get("validUntil")
        )

    async def get_all(self) -> List[Beneficio]:
        
        url = f"{self.base_url}/beneficios"
        try:
            data = await self._make_request(url)
            
            if not isinstance(data, list):
                raise ValueError("Invalid response format: expected list")
            
            beneficios = []
            for item in data:
                try:
                    if item.get("id") and item.get("name"):
                        beneficios.append(self._to_domain_model(item))
                except Exception as e:
                    logger.warning(f"Skipping invalid beneficio: {e}")
            
            logger.info(f"Successfully retrieved {len(beneficios)} benefits")
            return beneficios
            
        except Exception as e:
            logger.error(f"Error fetching benefits: {str(e)}")
            raise

    async def get_by_id(self, beneficio_id: int) -> Optional[Beneficio]:
        
        url = f"{self.base_url}/beneficios/{beneficio_id}"
        try:
            data = await self._make_request(url)
            return self._to_domain_model(data)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
        except Exception as e:
            logger.error(f"Error fetching benefit {beneficio_id}: {str(e)}")
            raise

    async def health_check(self) -> dict:
        
        try:
            await self._make_request(f"{self.base_url}/beneficios")
            return {"status": "healthy", "api_url": self.base_url}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e), "api_url": self.base_url}