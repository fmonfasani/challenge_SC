# tests/test_endpoints_integration.py
import pytest
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestBeneficiosEndpoints:
    
    @patch('app.infrastructure.repositories.BeneficiosRepository.get_all_beneficios')
    def test_get_beneficios_success(self, mock_get_all):
        """Test exitoso del endpoint GET /api/beneficios"""
        # Arrange
        mock_beneficios = [
            {
                "id": 1,
                "nombre": "Beneficio 1",
                "descripcion": "Descripción del beneficio 1",
                "imagen": "https://example.com/imagen1.jpg",
                "estado": "activo"
            },
            {
                "id": 2,
                "nombre": "Beneficio 2", 
                "descripcion": "Descripción del beneficio 2",
                "imagen": "https://example.com/imagen2.jpg",
                "estado": "inactivo"
            }
        ]
        mock_get_all.return_value = mock_beneficios
        
        # Act
        response = client.get("/api/beneficios")
        
        # Assert
        assert response.status_code == 200
        assert response.json() == mock_beneficios
        mock_get_all.assert_called_once()