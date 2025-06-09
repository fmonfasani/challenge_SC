import pytest
from unittest.mock import AsyncMock
from app.application.services import BeneficiosService
from app.domain.models import Beneficio, BeneficioStatus

@pytest.fixture
def mock_repository():
    return AsyncMock()

@pytest.fixture
def service(mock_repository):
    return BeneficiosService(mock_repository)

@pytest.mark.asyncio
async def test_get_all_beneficios_success(service, mock_repository):
    
    beneficios_mock = [
        Beneficio(id=1, name="Test 1", description="Desc 1", status=BeneficioStatus.ACTIVE, image="img1.jpg"),
        Beneficio(id=2, name="Test 2", description="Desc 2", status=BeneficioStatus.INACTIVE, image="img2.jpg")
    ]
    mock_repository.get_all.return_value = beneficios_mock

    
    result = await service.get_all_beneficios()

    
    assert len(result.beneficios) == 2  
    assert result.total == 2  
    assert result.beneficios[0].name == "Test 1"
    mock_repository.get_all.assert_called_once()

@pytest.mark.asyncio
async def test_get_beneficio_by_id_found(service, mock_repository):
    
    beneficio_mock = Beneficio(id=1, name="Test", description="Desc", status=BeneficioStatus.ACTIVE, image="img.jpg")    
    mock_repository.get_by_id.return_value = beneficio_mock

    
    result = await service.get_beneficio_by_id(1)

    
    assert result is not None
    assert result.name == "Test"
    mock_repository.get_by_id.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_get_beneficio_by_id_not_found(service, mock_repository):
    
    mock_repository.get_by_id.return_value = None

    
    result = await service.get_beneficio_by_id(999)

    
    assert result is None
    mock_repository.get_by_id.assert_called_once_with(999)

@pytest.mark.asyncio
async def test_get_all_beneficios_exception(service, mock_repository):
    
    mock_repository.get_all.side_effect = Exception("API Error")

    
    with pytest.raises(Exception, match="API Error"):
        await service.get_all_beneficios()

@pytest.mark.asyncio
async def test_get_beneficio_by_id_exception(service, mock_repository):
    
    mock_repository.get_by_id.side_effect = Exception("Network Error")

    
    with pytest.raises(Exception, match="Network Error"):
        await service.get_beneficio_by_id(1)