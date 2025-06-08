import pytest
from fastapi.testclient import TestClient
from app.main import app

def test_get_all_mock_beneficios():
    client = TestClient(app)
    response = client.get("/mock/beneficios")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_mock_beneficio_by_id_success():
    client = TestClient(app)
    response = client.get("/mock/beneficios/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "nombre" in data

def test_get_mock_beneficio_by_id_not_found():
    client = TestClient(app)
    response = client.get("/mock/beneficios/999")
    assert response.status_code == 404
