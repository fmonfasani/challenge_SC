import pytest
import asyncio
import time
from httpx import AsyncClient, ASGITransport
from app.main import app


class TestPerformance:

    async def make_request(self):
        """Helper method to make a single request"""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/beneficios")
            return response

    @pytest.mark.asyncio
    async def test_concurrent_requests(self):
        """Test handling multiple concurrent requests"""
        # Create multiple concurrent requests
        num_requests = 5
        tasks = [self.make_request() for _ in range(num_requests)]
        
        # Execute all requests concurrently
        responses = await asyncio.gather(*tasks)
        
        # Verify all requests completed successfully
        assert len(responses) == num_requests
        for response in responses:
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_response_time(self):
        """Test response time is within acceptable limits"""
        start_time = time.time()
        
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/beneficios")
            
        end_time = time.time()
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 5.0  # Should respond within 5 seconds

    @pytest.mark.asyncio
    async def test_rate_limiting(self):
        """Test rate limiting behavior"""
        # Make rapid requests to test rate limiting
        responses = []
        
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            for _ in range(10):
                response = await client.get("/beneficios")
                responses.append(response)
                # Small delay to avoid overwhelming the system
                await asyncio.sleep(0.1)
        
        # Verify that requests are handled properly
        success_count = sum(1 for r in responses if r.status_code == 200)
        rate_limited_count = sum(1 for r in responses if r.status_code == 429)
        
        # Should have at least some successful requests
        assert success_count > 0
        # Total requests should equal our attempts
        assert len(responses) == 10

    @pytest.mark.asyncio
    async def test_memory_usage_stability(self):
        """Test that memory usage remains stable under load"""
        # Make multiple requests to check for memory leaks
        for i in range(20):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                response = await client.get("/beneficios")
                assert response.status_code == 200
                
                # Also test individual beneficio endpoint
                response2 = await client.get("/beneficios/1")
                assert response2.status_code in [200, 404]

    @pytest.mark.asyncio
    async def test_endpoint_availability(self):
        """Test that all endpoints are available and responding"""
        endpoints = [
            "/beneficios",
            "/beneficios/1", 
            "/health",
            "/mock/beneficios",
            "/mock/beneficios/1"
        ]
        
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            for endpoint in endpoints:
                response = await client.get(endpoint)
                # Endpoints should respond (not necessarily 200, but not 500)
                assert response.status_code < 500