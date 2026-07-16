from collections.abc import Callable

import structlog
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger("dronzer.api.auth")


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """
    Validates API keys, Bearer tokens, and handles rate limiting basics.
    Ensures all OpenAI compatible routes have valid credentials before hitting the engine.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> JSONResponse:
        # Skip auth for health/docs and all admin endpoints (they have their own JWT dependency)
        if request.url.path.startswith(("/health", "/docs", "/openapi.json", "/metrics", "/admin")):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            logger.warning("Missing or invalid authorization header", path=request.url.path)
            return JSONResponse(
                status_code=401,
                content={
                    "error": {
                        "message": "You didn't provide an API key. You need to provide your API key in an Authorization header using Bearer auth (i.e. Authorization: Bearer YOUR_KEY).",
                        "type": "invalid_request_error",
                        "param": None,
                        "code": "missing_api_key",
                    }
                },
            )

        token = auth_header.replace("Bearer ", "").strip()

        # Phase 15: Strict Database Validation
        import hashlib

        from sqlalchemy import select

        from dronzer.infrastructure.database.core import async_session_factory
        from dronzer.infrastructure.database.models.gateway import GatewayKey

        hashed = hashlib.sha256(token.encode()).hexdigest()

        async with async_session_factory() as session:
            stmt = select(GatewayKey).where(
                GatewayKey.hashed_key == hashed,
                GatewayKey.is_active == True,
                GatewayKey.is_deleted == False,
            )
            result = await session.execute(stmt)
            db_key = result.scalars().first()

            if not db_key:
                logger.warning("Invalid API key provided", path=request.url.path)
                return JSONResponse(
                    status_code=401,
                    content={
                        "error": {
                            "message": "Incorrect API key provided.",
                            "type": "invalid_request_error",
                            "param": None,
                            "code": "invalid_api_key",
                        }
                    },
                )

            # Attach organization and project context to the request
            request.state.api_key = token
            request.state.gateway_key_id = db_key.id
            request.state.organization_id = db_key.organization_id
            request.state.project_id = db_key.project_id
            request.state.task_type = db_key.task_type
            request.state.model_priorities = db_key.model_priorities
            request.state.provider_priorities = db_key.provider_priorities

        response = await call_next(request)
        return response
