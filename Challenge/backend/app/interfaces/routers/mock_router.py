# Challenge/backend/app/interfaces/routers/mock_router.py

from fastapi import APIRouter, HTTPException, Path
from typing import List, Dict, Any


mock_router = APIRouter(prefix="/mock", tags=["mock"])

# Moock para probar la conexion entre le backend y el frontend, 
# Para la URL de la API real, ajustar el endpoint en el frontend
MOCK_BENEFICIOS = [
    {
        "id": 1,
        "name": "Farmacia VitaPlus",
        "description": "25% OFF en medicamentos de venta libre",
        "image": "https://images.pexels.com/photos/4385547/pexels-photo-4385547.jpeg?auto=compress&cs=tinysrgb&w=400",
        "status": "active",
        "fullDescription": "Obtén un 25% de descuento en todos los medicamentos de venta libre. Válido para analgésicos, vitaminas, suplementos y productos de cuidado personal. No válido con otras promociones.",
        "category": "Salud",
        "validUntil": "2025-08-31",
        "codigo": "VITA25"
    },
    {
        "id": 2,
        "name": "Hotel Sunset Paradise",
        "description": "40% OFF en reservas de fin de semana + desayuno gratis",
        "image": "https://images.pexels.com/photos/271618/pexels-photo-271618.jpeg?auto=compress&cs=tinysrgb&w=400",
        "status": "active",
        "fullDescription": "Disfruta de un 40% de descuento en habitaciones para fines de semana, incluye desayuno buffet gratuito para dos personas. Válido de viernes a domingo.",
        "category": "Turismo",
        "validUntil": "2025-09-30",
        "codigo": "SUNSET40"
    },
    {
        "id": 3,
        "name": "Agencia Viajes Mundo",
        "description": "$200 USD de descuento en paquetes internacionales",
        "image": "https://images.pexels.com/photos/1008155/pexels-photo-1008155.jpeg?auto=compress&cs=tinysrgb&w=400",
        "status": "active",
        "fullDescription": "Descuento de $200 USD aplicable a cualquier paquete turístico internacional con valor mínimo de $1500 USD. Incluye vuelos y hospedaje.",
        "category": "Viajes",
        "validUntil": "2025-12-31",
        "codigo": "MUNDO200"
    },
    {
        "id": 4,
        "name": "Tienda Fashion Center",
        "description": "2x1 en toda la colección de verano",
        "image": "https://images.pexels.com/photos/1488463/pexels-photo-1488463.jpeg?auto=compress&cs=tinysrgb&w=400",
        "status": "active",
        "fullDescription": "Promoción 2x1 en toda la colección de verano. Llevate dos prendas y paga solo una. Aplica en camisetas, shorts, vestidos y accesorios de temporada.",
        "category": "Moda",
        "validUntil": "2025-07-31",
        "codigo": "SUMMER2X1"
    },
    {
        "id": 5,
        "name": "Restaurante Bella Vita",
        "description": "30% OFF en cenas para parejas + copa de vino gratis",
        "image": "https://images.pexels.com/photos/1581384/pexels-photo-1581384.jpeg?auto=compress&cs=tinysrgb&w=400",
        "status": "active",
        "fullDescription": "Descuento del 30% en nuestro menú romántico para parejas, incluye una copa de vino de la casa por persona. Válido de martes a jueves.",
        "category": "Gastronomía",
        "validUntil": "2025-10-31",
        "codigo": "BELLA30"
    },
    {
        "id": 6,
        "name": "Supermercado Fresh Market",
        "description": "15% OFF en compras mayores a $100 + delivery gratis",
        "image": "https://images.pexels.com/photos/2292919/pexels-photo-2292919.jpeg?auto=compress&cs=tinysrgb&w=400",
        "status": "active",
        "fullDescription": "15% de descuento en compras superiores a $100, incluye delivery gratuito a domicilio. Válido todos los lunes del mes.",
        "category": "Supermercado",
        "validUntil": "2025-08-31",
        "codigo": "FRESH15"
    },
    {
        "id": 7,
        "name": "PetShop Amigos Peludos",
        "description": "35% OFF en alimentos para mascotas + juguete gratis",
        "image": "https://images.pexels.com/photos/1851164/pexels-photo-1851164.jpeg?auto=compress&cs=tinysrgb&w=400",
        "status": "active",
        "fullDescription": "35% de descuento en todos los alimentos para perros y gatos, incluye un juguete gratis por compra. Válido en marcas premium y estándar.",
        "category": "Mascotas",
        "validUntil": "2025-09-15",
        "codigo": "PELUDOS35"
    },
    {
        "id": 8,
        "name": "Clínica Veterinaria AnimalCare",
        "description": "50% OFF en consulta + vacunas básicas incluidas",
        "image": "https://images.pexels.com/photos/5731849/pexels-photo-5731849.jpeg?auto=compress&cs=tinysrgb&w=400",
        "status": "active",
        "fullDescription": "Primera consulta veterinaria con 50% de descuento, incluye vacunas básicas (antirrábica y múltiple). Válido para nuevos pacientes.",
        "category": "Veterinaria",
        "validUntil": "2025-12-31",
        "codigo": "CARE50"
    },
    {
        "id": 9,
        "name": "Spa & Wellness Relax",
        "description": "3x2 en tratamientos faciales + masaje de 30min gratis",
        "image": "https://images.pexels.com/photos/3985363/pexels-photo-3985363.jpeg?auto=compress&cs=tinysrgb&w=400",
        "status": "active",
        "fullDescription": "Promoción 3x2 en todos nuestros tratamientos faciales, incluye masaje relajante de 30 minutos sin costo adicional. Válido fines de semana.",
        "category": "Bienestar",
        "validUntil": "2025-11-30",
        "codigo": "RELAX3X2"
    },
    {
        "id": 10,
        "name": "Librería Cultural Books",
        "description": "20% OFF en libros + marcapáginas personalizado gratis",
        "image": "https://images.pexels.com/photos/159866/books-book-pages-read-literature-159866.jpeg?auto=compress&cs=tinysrgb&w=400",
        "status": "active",
        "fullDescription": "20% de descuento en toda nuestra colección de libros, incluye un marcapáginas personalizado con tu nombre. Válido en ficción, no ficción y académicos.",
        "category": "Cultura",
        "validUntil": "2025-07-31",
        "codigo": "BOOKS20"
    },
    {
        "id": 11,
        "name": "Gimnasio FitLife",
        "description": "60% OFF primer mes + evaluación nutricional gratis",
        "image": "https://images.pexels.com/photos/1552242/pexels-photo-1552242.jpeg?auto=compress&cs=tinysrgb&w=400",
        "status": "active",
        "fullDescription": "60% de descuento en tu primer mes de membresía, incluye evaluación nutricional completa y plan de entrenamiento personalizado. Solo nuevos miembros.",
        "category": "Deporte",
        "validUntil": "2025-10-31",
        "codigo": "FIT60"
    },
    {
        "id": 12,
        "name": "Cafetería Aroma Coffee",
        "description": "Compra 5 cafés y el 6to es gratis + postre incluido",
        "image": "https://images.pexels.com/photos/302899/pexels-photo-302899.jpeg?auto=compress&cs=tinysrgb&w=400",
        "status": "active",
        "fullDescription": "Tarjeta de fidelidad: acumula 5 cafés y el sexto es completamente gratis, incluye un postre de nuestra selección. Sin fecha de vencimiento.",
        "category": "Gastronomía",
        "validUntil": "2025-12-31",
        "codigo": "AROMA6"
    },
    {
        "id": 13,
        "name": "Dentista Smile Clinic",
        "description": "Limpieza dental gratuita + consulta incluida",
        "image": "https://images.pexels.com/photos/6627334/pexels-photo-6627334.jpeg?auto=compress&cs=tinysrgb&w=400",
        "status": "inactive",
        "fullDescription": "Limpieza dental profesional completamente gratuita, incluye consulta y revisión general. Válido para nuevos pacientes únicamente.",
        "category": "Salud",
        "validUntil": "2025-06-30",
        "codigo": "SMILE_FREE"
    },
    {
        "id": 14,
        "name": "Electrónica TechZone",
        "description": "25% OFF en smartphones + funda protectora gratis",
        "image": "https://images.pexels.com/photos/1618000/pexels-photo-1618000.jpeg?auto=compress&cs=tinysrgb&w=400",
        "status": "inactive",
        "fullDescription": "25% de descuento en toda la línea de smartphones, incluye funda protectora y vidrio templado sin costo adicional. Garantía extendida disponible.",
        "category": "Tecnología",
        "validUntil": "2025-05-31",
        "codigo": "TECH25"
    },
    {
        "id": 15,
        "name": "Auto Servicio Premium",
        "description": "Cambio de aceite + revisión general por $50",
        "image": "https://images.pexels.com/photos/3807501/pexels-photo-3807501.jpeg?auto=compress&cs=tinysrgb&w=400",
        "status": "inactive",
        "fullDescription": "Servicio completo de cambio de aceite sintético premium más revisión general de 15 puntos por solo $50. Incluye filtro de aceite y mano de obra.",
        "category": "Automotriz",
        "validUntil": "2025-04-30",
        "codigo": "AUTO50"
    }
]

@mock_router.get("/beneficios", response_model=List[Dict[str, Any]])
async def get_mock_beneficios():
    """
    Endpoint mock para obtener todos los beneficios realistas
    """
    return MOCK_BENEFICIOS

@mock_router.get("/beneficios/{beneficio_id}", response_model=Dict[str, Any])
async def get_mock_beneficio_by_id(
    beneficio_id: int = Path(..., gt=0, description="ID del beneficio")
):
    """
    Endpoint mock para obtener un beneficio por ID
    """
    beneficio = next((b for b in MOCK_BENEFICIOS if b["id"] == beneficio_id), None)
    
    if not beneficio:
        raise HTTPException(status_code=404, detail="Beneficio no encontrado")
    
    return beneficio