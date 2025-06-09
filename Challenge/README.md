# Beneficios SportClub

## Instalación y Ejecución

**Backend:**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

**IMPORTANTE - Variables de entorno:** Editar `backend/.env`:

```
# Para usar mock local (recomendado):
API_BASE_URL=http://localhost:8000/api/mock/

# Para usar API real:
API_BASE_URL=https://api-beneficios.dev.sportclub.com.ar/api/
```

**Ejecutar backend:**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

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

**Docker:**

```bash
docker-compose up --build
```

Acceso: Frontend http://localhost:3000 | API http://localhost:8000/docs

---

## Descripción Técnica

### Arquitectura Backend

Implementa Clean Architecture con FastAPI separando domain, application e infrastructure. El servicio actúa como intermediario entre el frontend y la API externa de SportClub, con fallback automático a datos mock.

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

Aplicación React con TypeScript usando componentes funcionales y hooks. Implementa lazy loading, paginación y sistema de favoritos persistente.

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

Backend con tests unitarios, integración y manejo de errores. Frontend con ESLint y validación TypeScript.

### Despliegue

Ambas aplicaciones dockerizadas con docker-compose. Configuración via variables de entorno. Health checks implementados.
