import pytest
from pydantic import ValidationError
from app.infrastructure.schemas import BeneficioResponse, BeneficioListResponse
from app.domain.models import Beneficio, BeneficioStatus, BeneficiosList


class TestSchemaValidation:
    
    def test_beneficio_response_valid_data(self):
        """Test valid beneficio response creation"""
        beneficio = Beneficio(
            id=1,
            name="Test Beneficio",
            description="Test description",
            status=BeneficioStatus.ACTIVE,
            image="https://example.com/image.jpg"
        )
        
        response = BeneficioResponse.from_domain(beneficio)
        
        assert response.id == 1
        assert response.name == "Test Beneficio"
        assert response.status == "active"

    def test_beneficio_list_response_valid_data(self):
        """Test valid beneficio list response creation"""
        beneficios = [
            Beneficio(
                id=1,
                name="Test 1",
                description="Desc 1",
                status=BeneficioStatus.ACTIVE
            ),
            Beneficio(
                id=2,
                name="Test 2",
                description="Desc 2",
                status=BeneficioStatus.INACTIVE
            )
        ]
        
        beneficios_list = BeneficiosList(beneficios=beneficios, total=2)
        response = BeneficioListResponse.from_domain(beneficios_list)
        
        assert response.total == 2
        assert len(response.beneficios) == 2
        assert response.beneficios[0].id == 1
        assert response.beneficios[1].status == "inactive"

    def test_beneficio_domain_model_validation(self):
        """Test domain model validation"""
        # Valid beneficio
        beneficio = Beneficio(
            id=1,
            name="Test",
            description="Test desc",
            status=BeneficioStatus.ACTIVE
        )
        
        assert beneficio.is_active() is True
        
        # Inactive beneficio
        inactive_beneficio = Beneficio(
            id=2,
            name="Test",
            description="Test desc",
            status=BeneficioStatus.INACTIVE
        )
        
        assert inactive_beneficio.is_active() is False

    def test_empty_beneficios_list(self):
        """Test empty beneficios list handling"""
        empty_list = BeneficiosList(beneficios=[], total=0)
        response = BeneficioListResponse.from_domain(empty_list)
        
        assert response.total == 0
        assert len(response.beneficios) == 0