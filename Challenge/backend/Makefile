# Makefile simple para el Challenge
.PHONY: help dev test docker clean

# Variables
IMAGE_NAME = sportclub-beneficios-api

help:
	@echo "🚀 Comandos del Challenge:"
	@echo "  make dev     - Ejecutar servidor (localhost:8000)"
	@echo "  make test    - Ejecutar tests"
	@echo "  make docker  - Build + Run Docker"
	@echo "  make clean   - Limpiar archivos temporales"

# Servidor de desarrollo
dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Tests
test:
	pytest tests/ -v --cov=app

# Docker completo (build + run)
docker:
	docker build -t $(IMAGE_NAME) .
	docker run -p 8000:8000 --env-file .env $(IMAGE_NAME)

# Limpieza
clean:
	rm -rf __pycache__ .pytest_cache htmlcov .coverage
	find . -name "*.pyc" -delete