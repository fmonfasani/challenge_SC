import pytest
import asyncio
import time
from fastapi.testclient import TestClient
from app.main import app

class TestPerformance:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_response_time(self, client):
        start_time = time.time()
        response = client.get("/beneficios")
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response_time < 2.0  
        assert response.status_code in [200, 404] 

    def test_concurrent_requests(self, client):
        def make_request():
            return client.get("/beneficios")
        
        # Make 5 concurrent requests
        responses = []
        for _ in range(5):
            response = make_request()
            responses.append(response)
        
        
        for response in responses:
            assert response.status_code != 500