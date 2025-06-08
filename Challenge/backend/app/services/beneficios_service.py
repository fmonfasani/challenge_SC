import httpx
from fastapi import HTTPException
from app.schemas.beneficio import BeneficioListResponse, BeneficioResponse, normalize_beneficio_data
import os
from dotenv import load_dotenv

load_dotenv()

class BeneficiosService:
    def __init__(self):
        # self.base_url = "https://api-beneficios.dev.sportclub.com.ar/api/beneficios" # esto es el endpoint original
        self.base_url = os.getenv("API_BASE_URL", "http://localhost:8000/api/mock/beneficios")

            
    async def get_all_beneficios(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url)
            if response.status_code != 200:
               raise HTTPException(status_code=502, detail="Error externo")
            beneficios_data = response.json()
            beneficios = [normalize_beneficio_data(b) for b in beneficios_data]
            return BeneficioListResponse(beneficios=beneficios, total=len(beneficios))

    async def get_beneficio_by_id(self, beneficio_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/{beneficio_id}")
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Beneficio no encontrado")
            if response.status_code != 200:
                raise HTTPException(status_code=502, detail="Error externo")
            beneficio_data = response.json()
            return BeneficioResponse(**normalize_beneficio_data(beneficio_data))

beneficios_service = BeneficiosService()
