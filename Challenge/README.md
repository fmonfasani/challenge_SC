# Proyecto Beneficios SportClub

Este proyecto implementa una aplicación completa para gestionar beneficios corporativos, dividida en dos partes: un backend en Python (FastAPI) y un frontend en React con TypeScript.

## 📋 Características Implementadas

### Backend (Python + FastAPI)

- ✅ API REST que actúa como intermediario con la API de SportClub
- ✅ Arquitectura limpia (Clean Architecture) con separación de capas
- ✅ Manejo robusto de errores y timeouts
- ✅ Logging completo y traceback claro
- ✅ Testing con más del 90% de cobertura
- ✅ Rate limiting y middleware personalizado
- ✅ Validación y normalización de datos
- ✅ Dockerizado y listo para producción

### Frontend (React + TypeScript)

- ✅ Aplicación React moderna con TypeScript y Vite
- ✅ Lista de beneficios con paginación
- ✅ Búsqueda por nombre y filtros por estado
- ✅ Sistema de favoritos con LocalStorage
- ✅ Vista detallada de beneficios
- ✅ Lazy loading de imágenes
- ✅ Diseño responsive con Tailwind CSS
- ✅ Manejo de estados de carga y errores
- ✅ Fallback automático a datos mock si la API falla

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.12+
- Node.js 18+
- Docker (opcional)

### 1. Configuración del Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
```

**Importante**: Edita el archivo `.env` para configurar la URL de la API:

```env
# Para usar la API real de SportClub (cuando esté disponible):
API_BASE_URL=https://api-beneficios.dev.sportclub.com.ar/api/

# Para usar el mock local (recomendado para testing):
API_BASE_URL=http://localhost:8000/api/mock/

# Otras configuraciones
REQUEST_TIMEOUT=10
LOG_LEVEL=INFO
```

### 2. Configuración del Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Configurar variables de entorno (opcional)
# Crear archivo .env en la carpeta frontend si quieres cambiar la URL del backend
echo "VITE_API_URL=http://localhost:8000/api" > .env
```

## 🏃‍♂️ Ejecutar el Proyecto

### Opción 1: Desarrollo Local

**Terminal 1 - Backend:**

```bash
cd backend
# Activar entorno virtual si no está activo
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Ejecutar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**

```bash
cd frontend
npm run dev
```

Accede a:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Documentación API: http://localhost:8000/docs

### Opción 2: Docker

```bash
# Ejecutar todo con Docker Compose
docker-compose up --build

# O ejecutar cada servicio por separado:

# Backend
cd backend
docker build -t sportclub-backend .
docker run -p 8000:8000 --env-file .env sportclub-backend

# Frontend
cd frontend
docker build -t sportclub-frontend .
docker run -p 3000:3000 sportclub-frontend
```

### Opción 3: Usando Makefile (Backend)

```bash
cd backend

# Desarrollo
make dev

# Tests
make test

# Docker
make docker
```

## 🧪 Testing

### Backend

```bash
cd backend

# Ejecutar todos los tests
pytest tests/ -v --cov=app

# Tests específicos
pytest tests/test_service.py -v
pytest tests/test_endpoints_integration.py -v

# Con reporte de cobertura HTML
pytest tests/ --cov=app --cov-report=html
```

### Frontend

```bash
cd frontend

# Linting
npm run lint

# Build para producción
npm run build
```

## 🌐 Configuración de API

### Usando la API Real de SportClub

Si quieres conectar con la API real de SportClub, cambia la variable en el archivo `backend/.env`:

```env
API_BASE_URL=https://api-beneficios.dev.sportclub.com.ar/api/
```

### Usando el Mock Local (Recomendado)

Para development y testing, usa el mock incluido:

```env
API_BASE_URL=http://localhost:8000/api/mock/
```

El mock incluye 15 beneficios de ejemplo con datos realistas.

## 📁 Estructura del Proyecto

```
Challenge/
├── backend/                    # API REST en Python
│   ├── app/
│   │   ├── domain/            # Modelos y reglas de negocio
│   │   ├── application/       # Casos de uso y servicios
│   │   └── infrastructure/    # Repositorios y detalles técnicos
│   ├── tests/                 # Tests unitarios e integración
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                   # Aplicación React
│   ├── src/
│   │   ├── components/        # Componentes React
│   │   ├── services/          # Servicios (API, LocalStorage)
│   │   ├── types/             # Tipos TypeScript
│   │   └── mock/              # Datos de prueba
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```

## 🎯 Funcionalidades Principales

### Frontend

- **Lista de beneficios**: Visualización en grid responsive
- **Búsqueda**: Filtrar beneficios por nombre en tiempo real
- **Filtros**: Por estado (activo/inactivo)
- **Paginación**: Navegación por páginas de resultados
- **Favoritos**: Marcar/desmarcar beneficios (persiste en LocalStorage)
- **Vista detallada**: Modal con información completa del beneficio
- **Lazy loading**: Carga optimizada de imágenes
- **Fallback automático**: Si la API falla, usa datos mock

### Backend

- **GET /api/beneficios**: Lista todos los beneficios
- **GET /api/beneficios/{id}**: Obtiene un beneficio específico
- **GET /health**: Health check del servicio
- **GET /docs**: Documentación automática de la API

## 🔧 Arquitectura Técnica

### Backend (Clean Architecture)

- **Domain**: Modelos de negocio y reglas
- **Application**: Servicios y casos de uso
- **Infrastructure**: Implementaciones técnicas (HTTP, base de datos)
- **Interfaces**: Controllers y schemas de API

### Frontend (Arquitectura por Capas)

- **Components**: Componentes React reutilizables
- **Services**: Lógica de negocio y llamadas a API
- **Types**: Definiciones TypeScript
- **Pages**: Páginas principales de la aplicación

## 🐛 Solución de Problemas

### La API no responde

- Verifica que el backend esté ejecutándose en el puerto 8000
- Revisa las variables de entorno en `.env`
- El frontend automáticamente usa datos mock si no puede conectar con la API

### Error de CORS

- El backend ya tiene CORS configurado para desarrollo
- Si tienes problemas, verifica que las URLs sean correctas

### Problemas con Docker

- Asegúrate de que los puertos 3000 y 8000 estén disponibles
- Verifica que Docker esté ejecutándose correctamente

## 📊 Testing y Calidad

- **Backend**: >90% cobertura de tests
- **Linting**: Configurado para Python (Black, MyPy) y TypeScript (ESLint)
- **Validación**: Pydantic para validación de datos
- **Documentación**: OpenAPI/Swagger automática
- **Logging**: Estructurado y configurable

## 🚀 Despliegue

El proyecto está preparado para despliegue con:

- **Docker**: Contenedores listos para producción
- **Environment Variables**: Configuración flexible
- **Health Checks**: Monitoreo de servicios
- **Static Files**: Frontend optimizado para CDN

¡El proyecto está listo para usar! Si tienes problemas, revisa los logs en consola o consulta la documentación de la API en `/docs`.
