from pydantic import BaseModel, Field
from typing import Optional, List
from app.domain.models import Beneficio, BeneficiosList


class BeneficioResponse(BaseModel):
    id: int
    name: str
    description: str
    status: str
    image: Optional[str] = None
    fullDescription: Optional[str] = Field(None, alias="full_description")
    category: Optional[str] = None
    validUntil: Optional[str] = Field(None, alias="valid_until")

    class Config:
        allow_population_by_field_name = True

    @classmethod
    def from_domain(cls, beneficio: Beneficio) -> "BeneficioResponse":
        """Convierte del modelo de dominio al schema de respuesta"""
        return cls(
            id=beneficio.id,
            name=beneficio.name,
            description=beneficio.description,
            status=beneficio.status.value,
            image=beneficio.image,
            fullDescription=beneficio.full_description,
            category=beneficio.category,
            validUntil=beneficio.valid_until
        )


class BeneficioListResponse(BaseModel):
    beneficios: List[BeneficioResponse]
    total: int

    @classmethod
    def from_domain(cls, beneficios_list: BeneficiosList) -> "BeneficioListResponse":
        """Convierte del modelo de dominio al schema de respuesta"""
        return cls(
            beneficios=[BeneficioResponse.from_domain(b) for b in beneficios_list.beneficios],
            total=beneficios_list.total
        )


class ErrorResponse(BaseModel):
    """Schema para respuestas de error"""
    detail: str
    status_code: int