from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging

class BeneficioBase(BaseModel):
    id: int
    nombre: str
    descripcion: str
    estado: str
    imagen: Optional[str]

class BeneficioResponse(BeneficioBase):
    pass

class BeneficioListResponse(BaseModel):
    beneficios: List[BeneficioResponse]
    total: int

def normalize_beneficio_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": raw_data.get("id"),
        "nombre": raw_data.get("nombre"),
        "descripcion": raw_data.get("descripcion"),
        "estado": raw_data.get("estado", "inactivo"),
        "imagen": raw_data.get("imagen"),
    }
