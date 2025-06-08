import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestErrorHandling:
    """Tests críticos para manejo de errores según el challenge"""
    
    @patch('app.application.services.BeneficiosService.get_all_beneficios')
    def test_api_down_error_handling(self, mock_service):
        """Test: Manejar API caída"""
        mock_service.side_effect = Exception("API caída")
        
        response = client.get("/api/beneficios")
        assert response.status_code == 500
        assert "API caída" in response.json()["detail"]

    @patch('app.application.services.BeneficiosService.get_beneficio_by_id')  
    def test_timeout_error_handling(self, mock_service):
        """Test: Manejar timeouts"""
        mock_service.side_effect = Exception("Timeout")
        
        response = client.get("/api/beneficios/1")
        assert response.status_code == 500
        assert "Timeout" in response.json()["detail"]

    def test_health_endpoint(self):
        """Test: Health check funciona"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"