import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import beneficios
from app.routers import mock


logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Beneficios API",
    description="API para gestión de beneficios usando Clean Architecture",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(beneficios.router, prefix="/api")
app.include_router(mock.router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Beneficios API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "beneficios-api", "version": "1.0.0"}
