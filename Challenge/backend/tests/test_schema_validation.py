import pytest
from pydantic import ValidationError
from app.interfaces.schemas.schemas import BeneficioResponse, BeneficioListResponse

class TestSchemaValidation:
    def test_beneficio_response_valid_data(self):
        # Arrange
        valid_data = {
            "id": 1,
            "nombre": "Descuento Gym",
            "descripcion": "10% de descuento en mensualidad",
            "categoria": "fitness"
        }
        
        # Act
        beneficio = BeneficioResponse(**valid_data)
        
        # Assert
        assert beneficio.id == 1
        assert beneficio.nombre == "Descuento Gym"
        assert beneficio.descripcion == "10% de descuento en mensualidad"
        assert beneficio.categoria == "fitness"

    def test_beneficio_list_response_valid_data(self):
        # Arrange
        valid_data = {
            "beneficios": [
                {
                    "id": 1,
                    "nombre": "Descuento Gym",
                    "descripcion": "10% descuento",
                    "categoria": "fitness"
                }
            ],
            "total": 1
        }
        
        # Act
        response = BeneficioListResponse(**valid_data)
        
        # Assert
        assert len(response.beneficios) == 1
        assert response.total == 1

    def test_empty_beneficios_list(self):
        # Arrange
        valid_data = {
            "beneficios": [],
            "total": 0
        }
        
        # Act
        response = BeneficioListResponse(**valid_data)
        
        # Assert
        assert len(response.beneficios) == 0
        assert response.total == 0