import time
from collections import defaultdict
import logging

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

logger = logging.getLogger("dronzer.api.middleware.rate_limit")

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Enterprise-grade in-memory sliding window rate limiter.
    Ensures that high-volume API requests do not overwhelm the Gateway infrastructure.
    """
    def __init__(self, app, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        # Determine the client identifier (IP or API Key from headers)
        client_ip = request.client.host if request.client else "unknown"
        api_key = request.headers.get("Authorization", "").replace("Bearer ", "")
        client_id = api_key if api_key else client_ip

        now = time.time()
        
        # Clean up old timestamps outside the sliding window
        cutoff = now - self.window_seconds
        self.requests[client_id] = [t for t in self.requests[client_id] if t > cutoff]

        if len(self.requests[client_id]) >= self.max_requests:
            logger.warning(f"Rate limit exceeded for client {client_id}")
            return JSONResponse(
                status_code=429,
                content={
                    "error": {
                        "code": "rate_limit_exceeded",
                        "message": f"Too many requests. Limit is {self.max_requests} requests per {self.window_seconds}s."
                    }
                }
            )

        # Allow request and record timestamp
        self.requests[client_id].append(now)
        response = await call_next(request)
        return response
