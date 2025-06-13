# Beneficios SportClub

## Instalación y Ejecución

**Backend:**
### clean and reset
Para realizar bien el procedimiento es conveniente borrar si existe algunos datos antiguos o de otro projecto
```bash
desactivate
rm -rf -m venv .venv

```
### RUN: 
```bash
cd backend
python -m venv .venv
.venv/bin/activate  # Windows: source .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

**IMPORTANTE - Variables de entorno:** Editar `backend/.env`:

Este proyecto cuenta con dos modalidades para poder analizar:

1 - Una opción utiliza datos hardcodeados para probar directamente la vista renderizada
    del frontend.
    En esta opción, tenemos datos de los beneficios hardcodeados tanto en el front como en
    el back, cuando no se puede comunicar a la API del backend, se renderiza los datos
    hardcodeados del frontend, si la conexión es exitosa a la API del backend, se renderiza
    los datos de beneficios hardcodeados pero de la API del backend.

    En el caso de que no haya conexión con la API del backend, probablemente sea un error
    de la variable de entorno. Asimismo agregué una ayuda visual para ver si estamos
    conectados o no a la API del Backend, cuando aparece 🟢 API Backend o 🟡 Datos Mock
    en la parte superior derecha, te indica si se conecta o no a la API, tanto en la opción
    1 como en la 2.

2 - La otra se conecta a la URL proporcionada en las instrucciones del Challenge para trabajar
    la API de SP (SportClub).

### Para la opción 1 tenemos que modificar los datos .env del backend de esta manera:
    API_BASE_URL=http://localhost:8000/api/mock/

### Para probar la API de SportClub, simplemente se usa la URL del challenge:
    API_BASE_URL=https://api-beneficios.dev.sportclub.com.ar/api/

**Ejecutar backend:**
Opcion rápida (con Make)
```bash
make dev
```
Opcion normal:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Instalación y Ejecución del frontend

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Tests:**
```bash
# Backend
cd backend && pytest tests/ -v --cov=app

# Frontend linting
cd frontend && npm run lint
```

### Test con la documentación de Openapi

    Gracias a los Schemas y decoradores con Fast API se puede documentar y haces test al CRUD de manera sencilla, 
    para acceder a la documentacion vamos al endpoint http://localhost:8000/docs y realizamos los siguientes test:

- GET /api/beneficios → Click "Try it out" → "Execute"
- GET /api/beneficios/{id} → Poner ID (ej: 1) → "Execute"
- GET /health → Health check
- GET /api/mock/beneficios → Mock data

**Docker**

Esta opción representa una tercera alternativa para evaluar el proyecto. Permite analizar
la aplicación mediante despliegue local con Docker o utilizando las imágenes ya subidas al repositorio.
Es la opción más rápida para evaluar el proyecto, especialmente con las imágenes preconstruidas
que están disponibles públicamente para ejecutar desde cualquier terminal.

```bash
# Desarrollo: Frontend -> Backend mock
docker-compose up

# Producción: Frontend -> API SportClub directa
docker-compose -f docker-compose.prod.yml up
```

Abrir http://localhost:3000 en el navegador. La aplicación funciona con datos mock si la API del challenge
no responde.

**Build local (si prefieres):**
```bash
docker-compose up --build
```

## Imágenes preconstruidas listas de Docker 

### Desarrollo:
```bash
ghcr.io/fmonfasani/sportclub-backend + frontend
docker-compose up
```

### Producción: 

Solo frontend -> API SportClub directa  
```bash
docker-compose -f docker-compose.prod.yml up
```

Acceso: Frontend http://localhost:3000 | API http://localhost:8000/docs

**Nota:** La aplicación incluye fallback automático a datos mock si la API externa no responde.

---

## Descripción Técnica

### Arquitectura Backend
Implementa Clean Architecture con FastAPI separando domain, application e infrastructure. 
El servicio actúa como intermediario entre el frontend y la API externa de SportClub, 
con fallback automático a datos mock.

**Tecnologías:**
- Python 3.12, FastAPI, Pydantic
- Testing: pytest, pytest-cov, respx
- Logging nativo, HTTPX para requests
- Docker, rate limiting

**Endpoints:**
- `GET /api/beneficios` - Lista todos los beneficios
- `GET /api/beneficios/{id}` - Beneficio específico  
- `GET /health` - Health check
- `GET /docs` - Documentación OpenAPI

### Arquitectura Frontend
Aplicación React con TypeScript usando componentes funcionales y hooks. 
Implementa lazy loading, paginación y sistema de favoritos persistente.

**Tecnologías:**
- React 19, TypeScript, Vite
- Tailwind CSS para estilos
- React Router para navegación
- LocalStorage para favoritos

**Funcionalidades:**
- Lista paginada de beneficios
- Búsqueda y filtros por estado
- Vista detallada en modal
- Sistema de favoritos
- Lazy loading de imágenes
- Diseño responsive

### Testing y Calidad
Backend con tests unitarios, integración y manejo de errores. 
Frontend con ESLint y validación TypeScript.

### Despliegue
Configuración dual: desarrollo con backend mock local, 
producción conectando directamente a API SportClub.

