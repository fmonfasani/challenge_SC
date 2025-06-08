from pydantic import BaseModel, Field
from typing import Optional, List
from ..domain.models import Beneficio, BeneficiosList


class BeneficioResponse(BaseModel):
    id: int
    name: str
    description: str
    status: str
    image: Optional[str] = None
    fullDescription: Optional[str] = Field(None, alias="full_description")
    category: Optional[str] = None
    validUntil: Optional[str] = Field(None, alias="valid_until")

    @classmethod
    def from_domain(cls, beneficio: Beneficio) -> "BeneficioResponse":
        return cls(
            id=beneficio.id,
            name=beneficio.name,
            description=beneficio.description,
            status=beneficio.status.value,
            image=beneficio.image,
            full_description=beneficio.full_description,
            category=beneficio.category,
            valid_until=beneficio.valid_until
        )


class BeneficioListResponse(BaseModel):
    beneficios: List[BeneficioResponse]
    total: int

    @classmethod
    def from_domain(cls, beneficios_list: BeneficiosList) -> "BeneficioListResponse":
        return cls(
            beneficios=[BeneficioResponse.from_domain(b) for b in beneficios_list.beneficios],
            total=beneficios_list.total
        )