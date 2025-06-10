# Beneficios SportClub

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

Backend con >90% cobertura incluyendo tests unitarios, integración y manejo de errores. Frontend con ESLint y validación TypeScript.

### Despliegue

Configuración dual: desarrollo con backend mock local, producción conectando directamente a API SportClub.

**Imágenes Docker listas:**

```bash
# Desarrollo: ghcr.io/fmonfasani/sportclub-backend + frontend
docker-compose up

# Producción: Solo frontend -> API SportClub directa
docker-compose -f docker-compose.prod.yml up
```
