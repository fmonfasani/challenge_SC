import pytest
import httpx
import respx
from fastapi import HTTPException
from app.application.services import BeneficioService, ExternalAPIError
from app.interfaces.schemas import BeneficioResponse, BeneficioListResponse

# Datos de prueba
MOCK_BENEFICIO = {
    "id": 1,
    "name": "Test Beneficio",
    "description": "Test description",
    "image": "https://example.com/image.jpg",
    "status": "active",
    "fullDescription": "Full test description",
    "category": "Test",
    "validUntil": "2024-12-31"
}

MOCK_BENEFICIOS_LIST = [
    MOCK_BENEFICIO,
    {
        "id": 2,
        "name": "Test Beneficio 2",
        "description": "Test description 2",
        "image": "https://example.com/image2.jpg",
        "status": "inactive",
        "fullDescription": "Full test description 2",
        "category": "Test2",
        "validUntil": "2024-12-31"
    }
]

class TestBeneficiosService:
    @pytest.fixture
    def service(self):
        return BeneficioService()
    
    @pytest.mark.asyncio
    async def test_get_all_beneficios_success(self, service):
        """Test exitoso para obtener todos los beneficios"""
        with respx.mock:
            respx.get(f"{service.base_url}/beneficios").mock(
                return_value=httpx.Response(200, json=MOCK_BENEFICIOS_LIST)
            )
            
            result = await service.get_all_beneficios()
            
            assert isinstance(result, BeneficioListResponse)
            assert result.total == 2
            assert len(result.beneficios) == 2
            assert result.beneficios[0].id == 1
            assert result.beneficios[0].name == "Test Beneficio"
            assert result.beneficios[1].id == 2
    
    @pytest.mark.asyncio
    async def test_get_beneficio_by_id_success(self, service):
        """Test exitoso para obtener beneficio por ID"""
        with respx.mock:
            respx.get(f"{service.base_url}/beneficios/1").mock(
                return_value=httpx.Response(200, json=MOCK_BENEFICIO)
            )
            
            result = await service.get_beneficio_by_id(1)
            
            assert isinstance(result, BeneficioResponse)
            assert result.id == 1
            assert result.name == "Test Beneficio"
            assert result.status == "active"
    
    @pytest.mark.asyncio
    async def test_get_beneficio_by_id_not_found(self, service):
        """Test para beneficio no encontrado"""
        with respx.mock:
            respx.get(f"{service.base_url}/beneficios/999").mock(
                return_value=httpx.Response(404, json={"detail": "Not found"})
            )
            
            with pytest.raises(HTTPException) as exc_info:
                await service.get_beneficio_by_id(999)
            
            assert exc_info.value.status_code == 404
            assert "Beneficio no encontrado" in exc_info.value.detail
    
    @pytest.mark.asyncio
    async def test_get_beneficio_by_id_invalid_id(self, service):
        """Test para ID inválido"""
        with pytest.raises(HTTPException) as exc_info:
            await service.get_beneficio_by_id(0)
        
        assert exc_info.value.status_code == 400
        assert "ID de beneficio inválido" in exc_info.value.detail
        
        with pytest.raises(HTTPException) as exc_info:
            await service.get_beneficio_by_id(-1)
        
        assert exc_info.value.status_code == 400
        
    @pytest.mark.asyncio
    async def test_timeout_error_with_retries(self, service):
        """Test para timeout con reintentos"""
        with respx.mock:
            respx.get(f"{service.base_url}/beneficios").mock(
                side_effect=httpx.TimeoutException("Timeout")
            )
            
            with pytest.raises(HTTPException) as exc_info:
                await service.get_all_beneficios()
            
            # Debería intentar max_retries + 1 veces
            assert exc_info.value.status_code == 500
    
    @pytest.mark.asyncio
    async def test_server_error_502(self, service):
        """Test para error 500 del servidor externo"""
        with respx.mock:
            respx.get(f"{service.base_url}/beneficios").mock(
                return_value=httpx.Response(500, json={"error": "Internal error"})
            )
            
            with pytest.raises(HTTPException) as exc_info:
                await service.get_all_beneficios()
            
            assert exc_info.value.status_code == 502
            assert "Error del servidor externo" in exc_info.value.detail
    
    @pytest.mark.asyncio
    async def test_invalid_response_format(self, service):
        """Test para formato de respuesta inválido"""
        with respx.mock:
            # Respuesta no es lista para get_all_beneficios
            respx.get(f"{service.base_url}/beneficios").mock(
                return_value=httpx.Response(200, json={"error": "not a list"})
            )
            
            with pytest.raises(HTTPException) as exc_info:
                await service.get_all_beneficios()
            
            assert exc_info.value.status_code == 502
            assert "Formato de datos inválido" in exc_info.value.detail
    
    @pytest.mark.asyncio
    async def test_empty_beneficios_list(self, service):
        """Test para lista vacía de beneficios"""
        with respx.mock:
            respx.get(f"{service.base_url}/beneficios").mock(
                return_value=httpx.Response(200, json=[])
            )
            
            result = await service.get_all_beneficios()
            
            assert isinstance(result, BeneficioListResponse)
            assert result.total == 0
            assert len(result.beneficios) == 0
    
    @pytest.mark.asyncio
    async def test_malformed_beneficio_data(self, service):
        """Test para datos malformados de beneficio"""
        malformed_data = [
            {"id": 1},  # Sin campos requeridos
            {"name": "Test"},  # Sin ID
            {"id": "invalid", "name": "Test", "description": "Test"}  # ID inválido
        ]
        
        with respx.mock:
            respx.get(f"{service.base_url}/beneficios").mock(
                return_value=httpx.Response(200, json=malformed_data)
            )
            
            result = await service.get_all_beneficios()
            
            # Debería filtrar los datos inválidos
            assert result.total == 0  # Todos los datos son inválidos
    
    @pytest.mark.asyncio
    async def test_health_check_healthy(self, service):
        """Test para health check exitoso"""
        with respx.mock:
            respx.get(f"{service.base_url}/beneficios").mock(
                return_value=httpx.Response(200, json=[])
            )
            
            result = await service.health_check()
            
            assert result["status"] == "healthy"
            assert result["api_url"] == service.base_url
    
    @pytest.mark.asyncio
    async def test_health_check_unhealthy(self, service):
        """Test para health check fallido"""
        with respx.mock:
            respx.get(f"{service.base_url}/beneficios").mock(
                side_effect=httpx.TimeoutException("Timeout")
            )
            
            result = await service.health_check()
            
            assert result["status"] == "unhealthy"
            assert "error" in result
    
    @pytest.mark.asyncio
    async def test_connection_error_with_retries(self, service):
        """Test para error de conexión con reintentos"""
        with respx.mock:
            respx.get(f"{service.base_url}/beneficios").mock(
                side_effect=httpx.ConnectError("Connection failed")
            )
            
            with pytest.raises(HTTPException) as exc_info:
                await service.get_all_beneficios()
            
            assert exc_info.value.status_code == 500
    
    @pytest.mark.asyncio
    async def test_rate_limiting_429(self, service):
        """Test para rate limiting (429)"""
        with respx.mock:
            respx.get(f"{service.base_url}/beneficios/1").mock(
                return_value=httpx.Response(429, json={"error": "Rate limited"})
            )
            
            with pytest.raises(HTTPException) as exc_info:
                await service.get_beneficio_by_id(1)
            
            assert exc_info.value.status_code == 429

# Tests de integración
class TestBeneficiosIntegration:
    @pytest.mark.asyncio
    async def test_full_flow_success(self):
        """Test de flujo completo exitoso"""
        service = BeneficioService()
        
        with respx.mock:
            # Mock para lista
            respx.get(f"{service.base_url}/beneficios").mock(
                return_value=httpx.Response(200, json=MOCK_BENEFICIOS_LIST)
            )
            
            # Mock para detalle
            respx.get(f"{service.base_url}/beneficios/1").mock(
                return_value=httpx.Response(200, json=MOCK_BENEFICIO)
            )
            
            # Test lista
            list_result = await service.get_all_beneficios()
            assert list_result.total == 2
            
            # Test detalle
            detail_result = await service.get_beneficio_by_id(1)
            assert detail_result.id == 1
            assert detail_result.name == "Test Beneficio"

# Fixtures adicionales para datos de prueba
@pytest.fixture
def mock_beneficio_data():
    return MOCK_BENEFICIO.copy()

@pytest.fixture  
def mock_beneficios_list():
    return MOCK_BENEFICIOS_LIST.copy()
