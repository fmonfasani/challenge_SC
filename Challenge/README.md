# Modulo de beneficios Sport Club

# Benefits Frontend

Aplicación frontend para la gestión de beneficios corporativos.

## Características

- **Framework**: React 18 + TypeScript + Vite
- **Estilos**: Tailwind CSS
- **Funcionalidades**:
  - Lista de beneficios con paginación
  - Búsqueda y filtros por estado
  - Lazy loading de imágenes
  - Sistema de favoritos (LocalStorage)
  - Vista detallada de beneficios
  - Diseño responsivo
  - Docker ready

## Instalación y Desarrollo

### Desarrollo local

```bash
# Instalar dependencias
npm install

# Ejecutar en modo desarrollo
npm run dev

# Construir para producción
npm run build

# Vista previa de producción
npm run preview
```

### Docker

```bash
# Construir imagen
npm run docker:build

# Ejecutar contenedor
npm run docker:run
```

La aplicación estará disponible en http://localhost:3000

## Estructura del Proyecto

```
src/
├── components/           # Componentes React
├── services/            # Servicios (API, LocalStorage)
├── types/               # Tipos TypeScript
├── utils/               # Utilidades
├── App.tsx              # Componente principal
├── main.tsx             # Punto de entrada
└── index.css            # Estilos globales
```

## API Integration

Para conectar con una API real, modifica el archivo `src/services/api.ts`:

```typescript
const API_BASE_URL = process.env.VITE_API_URL || "http://localhost:8000/api";

export const benefitsApi = {
  getAll: () => fetch(`${API_BASE_URL}/benefits`).then((res) => res.json()),
  getById: (id: number) =>
    fetch(`${API_BASE_URL}/benefits/${id}`).then((res) => res.json()),
};
```

## Configuración de Entorno
