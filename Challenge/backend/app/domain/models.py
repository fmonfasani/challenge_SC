from dataclasses import dataclass
from typing import Optional, List
from enum import Enum

class BeneficioStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

@dataclass
class Beneficio:
    id: int
    name: str
    description: str
    status: BeneficioStatus
    image: Optional[str] = None
    full_description: Optional[str] = None
    category: Optional[str] = None
    valid_until: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'nombre': self.name,  
            'descripcion': self.description, 
            'imagen': self.image,  
            'activo': self.is_active(),  
            'estado': self.status.value, 
            'descripcion_completa': self.full_description,  
            'categoria': self.category,  
            'valido_hasta': self.valid_until  
        }

    def is_active(self) -> bool:
        return self.status == BeneficioStatus.ACTIVE

@dataclass
class BeneficiosList:
    beneficios: List[Beneficio]
    total: int