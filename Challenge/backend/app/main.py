import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .interfaces.middlewares import setup_middleware
from .interfaces.routers import router as beneficios_router
from .interfaces.routers import mock_router

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="Beneficios API",
    description="Clean Architecture API for Beneficios Management",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
setup_middleware(app)

# Routers
app.include_router(beneficios_router)
app.include_router(mock_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Beneficios API is running", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "beneficios-api",
        "version": "1.0.0",
        "environment": os.getenv("ENV", "development")
    }