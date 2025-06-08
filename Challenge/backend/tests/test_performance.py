import pytest
import asyncio
import time
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
class TestPerformance:
    
    async def test_concurrent_requests(self):
        """Test handling of concurrent requests"""
        async def make_request():
            async with AsyncClient(app=app, base_url="http://test") as client:
                return await client.get("/api/beneficios")
        
        start_time = time.time()
        tasks = [make_request() for _ in range(10)]
        responses = await asyncio.gather(*tasks)
        end_time = time.time()
        
        # All requests should succeed
        for response in responses:
            assert response.status_code == 200
        
        # Should complete within reasonable time
        assert end_time - start_time < 5  # 5 seconds max for 10 concurrent requests

    async def test_response_time(self):
        """Test individual response time"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            start_time = time.time()
            response = await client.get("/api/beneficios")
            end_time = time.time()
            
            assert response.status_code == 200
            assert end_time - start_time < 2  # 2 seconds max

    async def test_rate_limiting(self):
        """Test rate limiting functionality"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Make rapid requests to trigger rate limit
            responses = []
            for _ in range(15):  # More than the 10/minute limit
                response = await client.get("/api/beneficios")
                responses.append(response.status_code)
            
            # Should have some rate limited responses (429)
            assert any(status == 429 for status in responses[-5:])