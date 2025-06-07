# 📚 Backend - Beneficios API

Este módulo expone una API REST para la gestión de beneficios. Actúa como intermediario entre un frontend y una API externa.

## 🚀 Tecnologías
- Python 3.12
- FastAPI
- Pydantic
- HTTPX (para consumo de APIs externas)
- Uvicorn (ASGI Server)
- Pytest (testing)

## 📦 Estructura del proyecto

backend/
├── app/
│ ├── main.py
│ ├── routers/
│ ├── schemas/
│ ├── services/
├── tests/
├── Dockerfile
├── requirements.txt
└── pytest.ini


## 🔗 Endpoints disponibles

- `GET /api/beneficios` — Lista todos los beneficios.
- `GET /api/beneficios/{id}` — Muestra el detalle de un beneficio.

## ⚙️ Instalación local

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Levantar el servidor
uvicorn app.main:app --reload
Acceso:

API disponible en: http://localhost:8000/docs (Swagger UI)

🧪 Ejecutar tests

pytest --cov=app --cov-report=term-missing

docker build -t beneficios-backend .
docker run -p 8000:8000 beneficios-backend


