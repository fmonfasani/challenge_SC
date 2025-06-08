from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class BeneficioBase(BaseModel):
    id: int = Field(..., gt=0, description="ID único del beneficio")
    name: str = Field(..., min_length=1, max_length=200, description="Nombre del beneficio")
    description: str = Field(..., min_length=1, max_length=500, description="Descripción breve")
    status: str = Field(..., description="Estado del beneficio")
    image: Optional[str] = Field(None, description="URL de la imagen")
    
    @validator('status')
    def validate_status(cls, v):
        allowed_statuses = ['active', 'inactive']
        if v not in allowed_statuses:
            logger.warning(f"Invalid status '{v}', defaulting to 'inactive'")
            return 'inactive'
        return v
    
    @validator('image')
    def validate_image_url(cls, v):
        if v and not (v.startswith('http://') or v.startswith('https://')):
            logger.warning(f"Invalid image URL '{v}', setting to None")
            return None
        return v

class BeneficioDetalle(BeneficioBase):
    fullDescription: Optional[str] = Field(None, description="Descripción completa")
    category: Optional[str] = Field(None, description="Categoría del beneficio")
    validUntil: Optional[str] = Field(None, description="Fecha de vencimiento")

class BeneficioResponse(BeneficioDetalle):
    """Response model para un beneficio individual"""
    pass

class BeneficioListResponse(BaseModel):
    """Response model para lista de beneficios"""
    beneficios: List[BeneficioBase]
    total: int = Field(..., ge=0, description="Total de beneficios")
    
    class Config:
        json_encoders = {
            # Puedes agregar encoders personalizados aquí si es necesario
        }

def normalize_beneficio_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normaliza los datos recibidos de la API externa
    Maneja inconsistencias y campos faltantes
    """
    try:
        normalized = {
            "id": raw_data.get("id"),
            "name": raw_data.get("name", ""),
            "description": raw_data.get("description", ""),
            "status": raw_data.get("status", "inactive"),
            "image": raw_data.get("image"),
            "fullDescription": raw_data.get("fullDescription"),
            "category": raw_data.get("category"),
            "validUntil": raw_data.get("validUntil")
        }
        
        # Log para debugging
        logger.debug(f"Normalized beneficio data for ID {normalized['id']}")
        
        return normalized
        
    except Exception as e:
        logger.error(f"Error normalizing beneficio data: {e}")
        raise ValueError(f"Failed to normalize beneficio data: {e}")

def validate_beneficio_list(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Valida y filtra una lista de beneficios
    Remueve elementos inválidos y los registra
    """
    valid_beneficios = []
    
    for item in data:
        try:
            if not item.get("id"):
                logger.warning("Beneficio without ID found, skipping")
                continue
                
            if not item.get("name"):
                logger.warning(f"Beneficio {item.get('id')} without name, skipping")
                continue
                
            normalized = normalize_beneficio_data(item)
            valid_beneficios.append(normalized)
            
        except Exception as e:
            logger.error(f"Failed to validate beneficio {item.get('id', 'unknown')}: {e}")
            continue
    
    logger.info(f"Validated {len(valid_beneficios)} out of {len(data)} beneficios")
    return valid_beneficios