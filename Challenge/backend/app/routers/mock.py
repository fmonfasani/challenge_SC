from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/mock",
    tags=["Mock"]
)

FAKE_BENEFICIOS = [
    {
        "id": 1,
        "name": "Seguro de Salud Premium",
        "description": "Cobertura médica completa para ti y tu familia",
        "image": "https://www.salus-seguros.com/resize/2024/seguros-salud-pymes.jpg",
        "status": "active",
        "fullDescription": "Seguro de salud con cobertura nacional e internacional...",
        "category": "Salud",
        "validUntil": "2024-12-31"
    },
    {
        "id": 2,
        "name": "Descuento en Gimnasios",
        "description": "50% de descuento en membresías",
        "image": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=300&fit=crop",
        "status": "active",
        "fullDescription": "Accede a más de 200 gimnasios...",
        "category": "Bienestar",
        "validUntil": "2024-12-31"
    },
    {
        "id": 7,
        "name": "Ámbito Pinturerías",
        "description": "10% de descuento en pinturas y accesorios",
        "image": "https://eks-production-01-api-beneficios.s3.us-east-1.amazonaws.com/SportClub-desde-Abril-2024-ALIANZAS-_3_.webp_1745370650480",
        "status": "active",
        "fullDescription": "Obtén descuentos exclusivos en pinturas, barnices y todos los productos de decoración para tu hogar.",
        "category": "Hogar",
        "validUntil": "2025-12-31"
    },
    {
        "id": 8,
        "name": "Auto Seguro",
        "description": "Protege tu vehículo con blindaje imperceptible",
        "image": "https://eks-production-01-api-beneficios.s3.us-east-1.amazonaws.com/autoseguro.webp_1738863959919",
        "status": "active",
        "fullDescription": "Blindaje vehicular de última generación, ahora accesible para todos. Disfruta seguridad sin comprometer el diseño.",
        "category": "Seguridad",
        "validUntil": "2025-12-31"
    },
    {
        "id": 9,
        "name": "Elie Autoservicios",
        "description": "15% de descuento en compras mayores a $10.000",
        "image": "https://eks-production-01-api-beneficios.s3.us-east-1.amazonaws.com/SportClub-desde-Abril-2024-ALIANZAS.webp_1745290278078",
        "status": "active",
        "fullDescription": "Descuentos exclusivos en autoservicios de todo el país, en alimentos y productos esenciales.",
        "category": "Alimentación",
        "validUntil": "2025-12-31"
    },
    {
        "id": 10,
        "name": "FarmaPlus",
        "description": "Descuento del 20% en medicamentos",
        "image": "https://eks-production-01-api-beneficios.s3.us-east-1.amazonaws.com/Dise%C3%83%C2%B1o-sin-t%C3%83%C2%ADtulo.webp_1746884873909",
        "status": "active",
        "fullDescription": "Beneficio válido en medicamentos de venta libre y recetados en todas las farmacias FarmaPlus.",
        "category": "Salud",
        "validUntil": "2025-12-31"
    },
    {
        "id": 11,
        "name": "Grill West",
        "description": "2x1 en parrilladas los fines de semana",
        "image": "https://eks-production-01-api-beneficios.s3.us-east-1.amazonaws.com/Dise%C3%83%C2%B1o-sin-t%C3%83%C2%ADtulo.webp_1746495741002",
        "status": "active",
        "fullDescription": "Disfruta de las mejores carnes a la parrilla con este beneficio especial los sábados y domingos.",
        "category": "Gastronomía",
        "validUntil": "2025-12-31"
    },
    {
        "id": 12,
        "name": "Rocky",
        "description": "20% de descuento en indumentaria deportiva",
        "image": "https://eks-production-01-api-beneficios.s3.us-east-1.amazonaws.com/Dise%C3%83%C2%B1o-sin-t%C3%83%C2%ADtulo-_1_.webp_1746882705385",
        "status": "active",
        "fullDescription": "Equipate con ropa y accesorios deportivos de alta calidad para tus entrenamientos diarios.",
        "category": "Deportes",
        "validUntil": "2025-12-31"
    },
    {
        "id": 13,
        "name": "Dental Total",
        "description": "Consultas odontológicas sin cargo",
        "image": "https://eks-production-01-api-beneficios.s3.us-east-1.amazonaws.com/SportClub-desde-Abril-2024-ALIANZAS.webp_1745460437335",
        "status": "active",
        "fullDescription": "Consulta odontológica inicial gratuita y descuentos en tratamientos posteriores en toda la red Dental Total.",
        "category": "Salud",
        "validUntil": "2025-12-31"
    },
    {
        "id": 14,
        "name": "TotalEnergies",
        "description": "Descuento en combustibles premium",
        "image": "https://eks-production-01-api-beneficios.s3.us-east-1.amazonaws.com/SportClub-desde-Abril-2024-ALIANZAS-_2_.webp_1742236156596",
        "status": "active",
        "fullDescription": "Carga tu vehículo con combustibles premium con un 10% de descuento en estaciones TotalEnergies adheridas.",
        "category": "Transporte",
        "validUntil": "2025-12-31"
    }
]

@router.get("/beneficios")
async def get_mock_beneficios():
    return FAKE_BENEFICIOS

@router.get("/beneficios/{beneficio_id}")
async def get_mock_beneficio_by_id(beneficio_id: int):
    beneficio = next((b for b in FAKE_BENEFICIOS if b["id"] == beneficio_id), None)
    if not beneficio:
        raise HTTPException(status_code=404, detail="Beneficio no encontrado")
    return beneficio
