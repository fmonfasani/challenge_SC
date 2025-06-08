import pytest
import asyncio
from unittest.mock import AsyncMock

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_async():
    """Helper fixture for async mocks"""
    return AsyncMock()