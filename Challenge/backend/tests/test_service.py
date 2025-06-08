import pytest
from unittest.mock import AsyncMock, Mock
from fastapi import HTTPException
from app.application.services import BeneficiosService
from app.domain.models import Beneficio

class TestBeneficiosService:
    @pytest.fixture
    def mock_repository(self):
        return AsyncMock()
    
    @pytest.fixture
    def service(self, mock_repository):
        return BeneficiosService(mock_repository)

    @pytest.mark.asyncio
    async def test_get_all_beneficios_success(self, service, mock_repository):
        # Arrange
        expected_beneficios = [
            Beneficio(id=1, nombre="Descuento Gym", descripcion="10% descuento", categoria="fitness"),
            Beneficio(id=2, nombre="Descuento Spa", descripcion="15% descuento", categoria="wellness")
        ]
        mock_repository.get_all.return_value = expected_beneficios
        
        # Act
        result = await service.get_all_beneficios()
        
        # Assert
        assert result == expected_beneficios
        mock_repository.get_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_beneficio_by_id_success(self, service, mock_repository):
        # Arrange
        beneficio_id = 1
        expected_beneficio = Beneficio(id=1, nombre="Descuento Gym", descripcion="10% descuento", categoria="fitness")
        mock_repository.get_by_id.return_value = expected_beneficio
        
        # Act
        result = await service.get_beneficio_by_id(beneficio_id)
        
        # Assert
        assert result == expected_beneficio
        mock_repository.get_by_id.assert_called_once_with(beneficio_id)

    @pytest.mark.asyncio
    async def test_get_beneficio_by_id_not_found(self, service, mock_repository):
        # Arrange
        beneficio_id = 999
        mock_repository.get_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await service.get_beneficio_by_id(beneficio_id)
        
        assert exc_info.value.status_code == 404
        assert "not found" in str(exc_info.value.detail).lower()

    @pytest.mark.asyncio
    async def test_get_beneficio_by_id_invalid_id(self, service, mock_repository):
        # Arrange
        invalid_ids = [0, -1, -5]
        
        for invalid_id in invalid_ids:
            # Act & Assert
            with pytest.raises(HTTPException) as exc_info:
                await service.get_beneficio_by_id(invalid_id)
            
            assert exc_info.value.status_code == 400
            assert "invalid" in str(exc_info.value.detail).lower()

    @pytest.mark.asyncio
    async def test_connection_error_handling(self, service, mock_repository):
        # Arrange
        mock_repository.get_all.side_effect = Exception("Connection failed")
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await service.get_all_beneficios()
        
        assert exc_info.value.status_code == 500

    @pytest.mark.asyncio
    async def test_health_check(self, service, mock_repository):
        # Arrange
        mock_repository.health_check.return_value = True
        
        # Act
        result = await service.health_check()
        
        # Assert
        assert result is True
        mock_repository.health_check.assert_called_once()
