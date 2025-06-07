# 🎨 Frontend - Beneficios Web App

Aplicación web para la consulta de beneficios. Consume los servicios expuestos por el backend y permite visualizar, buscar y gestionar favoritos.

## 🚀 Tecnologías
- React 18
- Vite
- Axios
- React Router DOM
- Tailwind CSS
- Lucide React (íconos)

## 📦 Estructura del proyecto

frontend/
├── src/
│ ├── main.jsx
│ ├── App.jsx
│ ├── components/
│ ├── services/
├── Dockerfile
├── package.json
├── vite.config.js
└── .env


## 🔗 Funcionalidades principales

- Listado de beneficios con búsqueda por nombre.
- Filtro por estado (activo/inactivo).
- Visualización de detalle de cada beneficio.
- Marcado de beneficios como favoritos (localStorage).
- Diseño completamente responsivo.
- Lazy Loading de imágenes.

## ⚙️ Instalación local

# Instalar dependencias
```bash
npm install
```
# Ejecutar servidor de desarrollo

```bash
npm run dev
```
Acceso:

Frontend disponible en: http://localhost:3000/beneficios

📄 Variables de entorno
El proyecto usa una variable para la URL del backend:

VITE_API_URL=http://localhost:8000/api

🐳 Docker
```bash
docker build -t beneficios-frontend .
docker run -p 3000:3000 beneficios-frontend
```
El frontend sirve la aplicación en http://localhost:3000.
