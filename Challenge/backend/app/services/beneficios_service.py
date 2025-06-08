import os
import asyncio
from typing import Optional
import httpx
from fastapi import HTTPException
from app.schemas.beneficio import (
    BeneficioListResponse, 
    BeneficioResponse, 
    normalize_beneficio_data,
    validate_beneficio_list
)
import logging
from dotenv import load_dotenv
import traceback

load_dotenv()

logger = logging.getLogger(__name__)

class BeneficiosServiceError(Exception):
    """Excepción personalizada para errores del servicio"""
    pass

class ExternalAPIError(BeneficiosServiceError):
    """Error al comunicarse con la API externa"""
    pass

class BeneficiosService:
    def __init__(self):
        self.base_url = os.getenv("API_BASE_URL", "http://localhost:8000/api/mock")
        self.timeout = int(os.getenv("API_TIMEOUT", "10"))
        self.max_retries = int(os.getenv("MAX_RETRIES", "3"))
        
        logger.info(f"BeneficiosService initialized with base_url: {self.base_url}")
    
    async def _make_request(self, url: str, retries: int = 0) -> dict:
        """
        Realiza una petición HTTP con manejo de reintentos y errores
        """
        try:
            async with httpx.AsyncClient() as client:
                logger.debug(f"Making request to {url} (attempt {retries + 1})")
                
                response = await client.get(
                    url, 
                    timeout=self.timeout,
                    headers={"User-Agent": "BeneficiosService/1.0"}
                )
                
                response.raise_for_status()
                data = response.json()
                
                logger.debug(f"Successful response from {url}")
                return data
                
        except httpx.TimeoutException as e:
            logger.warning(f"Timeout error for {url}: {e}")
            if retries < self.max_retries:
                await asyncio.sleep(2 ** retries)  # Exponential backoff
                return await self._make_request(url, retries + 1)
            raise ExternalAPIError("API timeout after retries")
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} for {url}: {e}")
            if e.response.status_code == 404:
                raise HTTPException(status_code=404, detail="Beneficio no encontrado")
            elif e.response.status_code >= 500:
                raise HTTPException(status_code=502, detail="Error del servidor externo")
            else:
                raise HTTPException(status_code=e.response.status_code, detail="Error en API externa")
                
        except httpx.RequestError as e:
            logger.error(f"Request error for {url}: {e}")
            if retries < self.max_retries:
                await asyncio.sleep(2 ** retries)
                return await self._make_request(url, retries + 1)
            raise ExternalAPIError("Error de conectividad con API externa")
            
        except Exception as e:
            logger.error(f"Unexpected error for {url}: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail="Error interno del servidor")
    
    async def get_all_beneficios(self) -> BeneficioListResponse:
        """
        Obtiene todos los beneficios de la API externa
        """
        url = f"{self.base_url}/beneficios"
        logger.info(f"Fetching all beneficios from {url}")
        
        try:
            raw_data = await self._make_request(url)
            
            # Validar que sea una lista
            if not isinstance(raw_data, list):
                logger.error(f"Expected list, got {type(raw_data)}")
                raise HTTPException(status_code=502, detail="Formato de datos inválido")
            
            # Validar y normalizar datos
            validated_data = validate_beneficio_list(raw_data)
            
            if not validated_data:
                logger.warning("No valid beneficios found")
                return BeneficioListResponse(beneficios=[], total=0)
            
            # Crear objetos de respuesta
            beneficios = [BeneficioResponse(**item) for item in validated_data]
            
            logger.info(f"Successfully fetched {len(beneficios)} beneficios")
            return BeneficioListResponse(beneficios=beneficios, total=len(beneficios))
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in get_all_beneficios: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail="Error interno del servidor")
    
    async def get_beneficio_by_id(self, beneficio_id: int) -> BeneficioResponse:
        """
        Obtiene un beneficio específico por ID
        """
        if beneficio_id <= 0:
            raise HTTPException(status_code=400, detail="ID de beneficio inválido")
        
        url = f"{self.base_url}/beneficios/{beneficio_id}"
        logger.info(f"Fetching beneficio {beneficio_id} from {url}")
        
        try:
            raw_data = await self._make_request(url)
            
            # Validar que tenga estructura básica
            if not isinstance(raw_data, dict) or not raw_data.get("id"):
                logger.error(f"Invalid beneficio data structure: {raw_data}")
                raise HTTPException(status_code=502, detail="Datos de beneficio inválidos")
            
            # Normalizar y validar
            normalized_data = normalize_beneficio_data(raw_data)
            beneficio = BeneficioResponse(**normalized_data)
            
            logger.info(f"Successfully fetched beneficio {beneficio_id}")
            return beneficio
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in get_beneficio_by_id({beneficio_id}): {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail="Error interno del servidor")
    
    async def health_check(self) -> dict:
        """
        Verifica el estado de la API externa
        """
        try:
            url = f"{self.base_url}/beneficios"
            await self._make_request(url)
            return {"status": "healthy", "api_url": self.base_url}
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "unhealthy", "error": str(e)}

# Instancia singleton del servicio
beneficios_service = BeneficiosService()