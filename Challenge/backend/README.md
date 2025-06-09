# 📚 Backend - Beneficios API

Este módulo expone una API REST para la gestión de beneficios. Actúa como intermediario entre un frontend y una API externa.

## 🚀 Tecnologías

- Python 3.12
- FastAPI
- Pydantic
- HTTPX (para consumo de APIs externas)
- Uvicorn (ASGI Server)
- Pytest (testing)

Beneficios API - Clean Architecture
API REST minimalista que actúa como intermediario para la API de beneficios de SportClub, implementando Clean Architecture.

🏗️ Arquitectura
app/
├── domain/ # Entidades y reglas de negocio
│ ├── models.py # Modelos de dominio
│ └── ports.py # Interfaces/Contratos
├── application/ # Casos de uso
│ └── services.py # Servicios de aplicación
└── infrastructure/ # Detalles técnicos
├── repositories.py # Implementación de repositorios
├── schemas.py # Modelos de API
├── routers.py # Endpoints
└── middleware.py # Middleware personalizado

Inversión de dependencias: Dominio no depende de infraestructura
Separación de responsabilidades: Cada capa tiene una responsabilidad específica
Testabilidad: Fácil testing mediante interfaces
Escalabilidad: Fácil agregar nuevas fuentes de datos

🚀 Instalación y Ejecución
Local
bash# Instalar dependencias
make install

# Copiar variables de entorno

cp .env.example .env

# Ejecutar en modo desarrollo

make dev
Docker
bash# Construir imagen
make docker-build

# Ejecutar contenedor

make docker-run
📋 Endpoints
MétodoEndpointDescripciónGET/api/beneficiosLista todos los beneficiosGET/api/beneficios/{id}Obtiene beneficio por IDGET/healthHealth checkGET/docsDocumentación automática
🧪 Testing
bash# Tests completos con cobertura
make test

# Solo tests unitarios

pytest tests/test_beneficios_service.py -v

# Tests de integración

pytest tests/test_integration.py -
