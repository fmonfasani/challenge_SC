# app/interfaces/middlewares/middlewares.py

import time
import logging
from fastapi import Request, Response
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

logger = logging.getLogger(__name__)

# Rate limiter instance
limiter = Limiter(key_func=get_remote_address)

async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    
    # Process request
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} - {process_time:.3f}s")
    
    # Add custom response headers
    response.headers["X-Process-Time"] = str(process_time)
    return response

# ✅ Función agregada que faltaba
def setup_middlewares(app):
    """
    Setup all middlewares for the FastAPI app.
    """
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.middleware("http")(logging_middleware)

# ✅ Alias para compatibilidad con main.py
setup_middleware = setup_middlewares