import pytest
from pydantic import ValidationError
from app.interfaces.schemas.schemas import BeneficioResponse, BeneficioListResponse

class TestSchemaValidation:
    def test_beneficio_response_valid_data(self):
        
        valid_data = {
            "id": 1,
            "name": "Descuento Gym",  
            "description": "10% de descuento en mensualidad",  
            "status": "active",  
            "category": "fitness"
        }       
        
        beneficio = BeneficioResponse(**valid_data)        
        
        assert beneficio.id == 1
        assert beneficio.name == "Descuento Gym"
        assert beneficio.description == "10% de descuento en mensualidad"
        assert beneficio.category == "fitness"
        assert beneficio.status == "active"

    def test_beneficio_list_response_valid_data(self):
        
        valid_data = {
            "beneficios": [
                {
                    "id": 1,
                    "name": "Descuento Gym",  
                    "description": "10% descuento",  
                    "status": "active",  
                    "category": "fitness"
                }
            ],
            "total": 1
        }
        
        # Act
        response = BeneficioListResponse(**valid_data)
        
        # Assert
        assert len(response.beneficios) == 1
        assert response.total == 1
        assert response.beneficios[0].name == "Descuento Gym"

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

    def test_beneficio_response_missing_required_fields(self):
        # Arrange - Datos inválidos (falta campo requerido)
        invalid_data = {
            "id": 1,
            "name": "Test"
            
        }
        
        # Act & Assert
        with pytest.raises(ValidationError):
            BeneficioResponse(**invalid_data)