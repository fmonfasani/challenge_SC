import pytest
from unittest.mock import Mock, AsyncMock, patch
import aiohttp
from app.application.services import BeneficioService
from app.domain.models import Beneficio


class TestBeneficiosService:

    @pytest.fixture
    def mock_repository(self):
        """Mock repository for testing"""
        return Mock()

    @pytest.fixture  
    def service(self, mock_repository):
        """Service with mocked repository"""
        return BeneficioService(repository=mock_repository)

    @pytest.mark.asyncio
    async def test_get_all_beneficios_success(self, service, mock_repository):
        # Arrange
        expected_beneficios = [
            {"id": 1, "name": "Test Beneficio 1"},
            {"id": 2, "name": "Test Beneficio 2"}
        ]
        mock_repository.get_all_beneficios = AsyncMock(return_value=expected_beneficios)
        
        # Act
        result = await service.get_all_beneficios()
        
        # Assert
        assert result == expected_beneficios
        mock_repository.get_all_beneficios.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_beneficio_by_id_success(self, service, mock_repository):
        # Arrange
        beneficio_id = 1
        expected_beneficio = {"id": 1, "name": "Test Beneficio"}
        mock_repository.get_beneficio_by_id = AsyncMock(return_value=expected_beneficio)
        
        # Act
        result = await service.get_beneficio_by_id(beneficio_id)
        
        # Assert
        assert result == expected_beneficio
        mock_repository.get_beneficio_by_id.assert_called_once_with(beneficio_id)

    @pytest.mark.asyncio
    async def test_get_beneficio_by_id_not_found(self, service, mock_repository):
        # Arrange
        beneficio_id = 999
        mock_repository.get_beneficio_by_id = AsyncMock(return_value=None)
        
        # Act
        result = await service.get_beneficio_by_id(beneficio_id)
        
        # Assert
        assert result is None
        mock_repository.get_beneficio_by_id.assert_called_once_with(beneficio_id)

    @pytest.mark.asyncio
    async def test_get_beneficio_by_id_invalid_id(self, service, mock_repository):
        # Arrange
        invalid_id = "invalid"
        
        # Act & Assert
        with pytest.raises(ValueError):
            await service.get_beneficio_by_id(invalid_id)

    @pytest.mark.asyncio
    async def test_timeout_error_with_retries(self, service, mock_repository):
        # Arrange
        mock_repository.get_all_beneficios = AsyncMock(
            side_effect=aiohttp.ServerTimeoutError("Timeout")
        )
        
        # Act & Assert
        with pytest.raises(aiohttp.ServerTimeoutError):
            await service.get_all_beneficios()

    @pytest.mark.asyncio
    async def test_server_error_502(self, service, mock_repository):
        # Arrange
        mock_repository.get_all_beneficios = AsyncMock(
            side_effect=aiohttp.ClientResponseError(
                request_info=Mock(),
                history=(),
                status=502
            )
        )
        
        # Act & Assert
        with pytest.raises(aiohttp.ClientResponseError):
            await service.get_all_beneficios()

    @pytest.mark.asyncio
    async def test_invalid_response_format(self, service, mock_repository):
        # Arrange
        mock_repository.get_all_beneficios = AsyncMock(return_value="invalid_format")
        
        # Act
        result = await service.get_all_beneficios()
        
        # Assert
        assert result == "invalid_format"  # Service should handle or validate

    @pytest.mark.asyncio
    async def test_empty_beneficios_list(self, service, mock_repository):
        # Arrange
        mock_repository.get_all_beneficios = AsyncMock(return_value=[])
        
        # Act
        result = await service.get_all_beneficios()
        
        # Assert
        assert result == []

    @pytest.mark.asyncio
    async def test_malformed_beneficio_data(self, service, mock_repository):
        # Arrange
        malformed_data = [{"id": 1}]  # Missing required fields
        mock_repository.get_all_beneficios = AsyncMock(return_value=malformed_data)
        
        # Act
        result = await service.get_all_beneficios()
        
        # Assert
        assert result == malformed_data

    @pytest.mark.asyncio
    async def test_health_check_healthy(self, service, mock_repository):
        # Arrange
        mock_repository.health_check = AsyncMock(return_value={"status": "healthy"})
        
        # Act
        result = await service.health_check()
        
        # Assert
        assert result["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_health_check_unhealthy(self, service, mock_repository):
        # Arrange
        mock_repository.health_check = AsyncMock(return_value={"status": "unhealthy"})
        
        # Act
        result = await service.health_check()
        
        # Assert
        assert result["status"] == "unhealthy"

    @pytest.mark.asyncio
    async def test_connection_error_with_retries(self, service, mock_repository):
        # Arrange
        mock_repository.get_all_beneficios = AsyncMock(
            side_effect=aiohttp.ClientConnectionError("Connection failed")
        )
        
        # Act & Assert
        with pytest.raises(aiohttp.ClientConnectionError):
            await service.get_all_beneficios()

    @pytest.mark.asyncio
    async def test_rate_limiting_429(self, service, mock_repository):
        # Arrange
        mock_repository.get_all_beneficios = AsyncMock(
            side_effect=aiohttp.ClientResponseError(
                request_info=Mock(),
                history=(),
                status=429
            )
        )
        
        # Act & Assert
        with pytest.raises(aiohttp.ClientResponseError):
            await service.get_all_beneficios()


class TestBeneficiosIntegration:
    
    @pytest.mark.asyncio
    async def test_full_flow_success(self):
        # Arrange
        mock_repository = Mock()
        mock_repository.get_beneficio_by_id = AsyncMock(
            return_value={"id": 1, "name": "Test Beneficio"}
        )
        service = BeneficioService(repository=mock_repository)
        
        # Act
        result = await service.get_beneficio_by_id(1)
        
        # Assert
        assert result["id"] == 1
        assert result["name"] == "Test Beneficio"