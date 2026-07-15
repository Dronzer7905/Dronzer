from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Adds essential OWASP recommended security headers to all HTTP responses.
    """
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)

        # HSTS (Strict-Transport-Security)
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"
        # Clickjacking protection
        response.headers["X-Frame-Options"] = "DENY"
        # XSS filtering
        response.headers["X-XSS-Protection"] = "1; mode=block"
        # Prevent information leakage
        response.headers["Server"] = "DronzerGateway"
        # Content Security Policy (Strict API Policy)
        response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none';"

        return response
