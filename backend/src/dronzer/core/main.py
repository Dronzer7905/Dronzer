from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from redis.asyncio import Redis

from dronzer.api.middleware import SecurityHeadersMiddleware
from dronzer.api.v1.health import router as health_router
from dronzer.core.config import settings
from dronzer.core.exceptions import DronzerException
from dronzer.core.logging import configure_logging, get_logger
from dronzer.infrastructure.cache import DistributedCache

logger = get_logger("dronzer.startup")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """
    Application startup and shutdown lifecycle hooks.
    """
    # STARTUP
    logger.info(
        "Booting Dronzer AI Gateway...",
        version=settings.APP_VERSION,
        env=settings.ENVIRONMENT.value,
    )

    # Initialize dependency containers
    redis_client = Redis.from_url(
        settings.REDIS_URL if hasattr(settings, "REDIS_URL") else "redis://localhost:6379"
    )
    app.state.cache = DistributedCache(redis_client=redis_client)
    app.state.event_bus = None  # Future event bus integration
    app.state.redis = redis_client

    logger.info("Startup complete. Accepting connections.")

    yield

    # SHUTDOWN
    logger.info("Initiating graceful shutdown...")
    if hasattr(app.state, "redis"):
        await app.state.redis.close()
    logger.info("Shutdown complete.")


def create_app() -> FastAPI:
    """
    Application factory. Constructs and configures the FastAPI instance.
    """
    # 1. Configure structured logging first
    configure_logging()

    # 2. Build the app
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Enterprise-grade AI Gateway API",
        lifespan=lifespan,
        docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
        redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
    )

    # 3. Add middlewares
    app.add_middleware(SecurityHeadersMiddleware)

    # Strictly configure CORS based on environment
    allowed_origins = (
        [str(origin) for origin in settings.CORS_ORIGINS]
        if hasattr(settings, "CORS_ORIGINS") and settings.CORS_ORIGINS
        else []
    )
    if settings.ENVIRONMENT == "development":
        allowed_origins.append("*")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins if allowed_origins else ["https://dashboard.dronzer.ai"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],  # Limit methods to essentials
        allow_headers=["*"],
    )

    # 4. Register exception handlers
    @app.exception_handler(DronzerException)
    async def dronzer_exception_handler(request: Request, exc: DronzerException) -> JSONResponse:
        logger.warning(
            "Dronzer exception caught",
            path=request.url.path,
            status=exc.status_code,
            message=exc.message,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.message, "details": exc.details},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.error("Unhandled server exception", path=request.url.path, exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"},
        )

    # 5. Register routers
    app.include_router(health_router, prefix="/api/v1", tags=["System"])

    return app


app = create_app()
