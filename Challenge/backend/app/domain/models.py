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
            'nombre': self.name,  # Corregido: usar self.name
            'descripcion': self.description,  # Corregido: usar self.description
            'imagen': self.image,  # Corregido: usar self.image
            'activo': self.is_active(),  # Corregido: usar método is_active()
            'estado': self.status.value,  # Agregado: estado original
            'descripcion_completa': self.full_description,  # Agregado
            'categoria': self.category,  # Agregado
            'valido_hasta': self.valid_until  # Agregado
        }

    def is_active(self) -> bool:
        return self.status == BeneficioStatus.ACTIVE

@dataclass
class BeneficiosList:
    beneficios: List[Beneficio]
    total: int