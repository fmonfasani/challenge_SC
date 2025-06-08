import pytest
from fastapi.testclient import TestClient
from app.main import app

class TestBeneficiosIntegration:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_get_all_beneficios_integration(self, client):
        response = client.get("/beneficios")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_beneficio_by_id_integration(self, client):
        response = client.get("/beneficios/1")
        assert response.status_code in [200, 404]  # Either found or not found is valid

    def test_invalid_beneficio_id_integration(self, client):
        response = client.get("/beneficios/invalid")
        assert response.status_code == 422  # Validation error

    def test_health_endpoint(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data