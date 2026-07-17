from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from dronzer.presentation.api.errors import register_error_handlers
from dronzer.presentation.api.middleware.auth import AuthenticationMiddleware
from dronzer.presentation.api.middleware.observability import ObservabilityMiddleware
from dronzer.presentation.api.middleware.rate_limit import RateLimitMiddleware


def create_app() -> FastAPI:
    """
    Factory to create the FastAPI application with all middleware, routes, and error handlers.
    Configured for maximum performance using ORJSONResponse.
    """
    app = FastAPI(
        title="Dronzer AI Gateway",
        description="Enterprise-grade AI Orchestration Engine and API Gateway",
        version="1.0.0",
        docs_url="/docs",
        redoc_url=None,
        default_response_class=ORJSONResponse,
    )

    # Global Middleware
    # Order matters: Observability (outermost) -> Rate Limit -> Auth -> Routing
    app.add_middleware(AuthenticationMiddleware)
    app.add_middleware(RateLimitMiddleware, max_requests=1000, window_seconds=60)
    app.add_middleware(ObservabilityMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    # Register Error Handlers
    register_error_handlers(app)

    # Health Endpoints
    @app.get("/api/v1/health")
    @app.get("/health")
    @app.get("/health/liveness")
    async def liveness():
        return {"status": "alive"}

    @app.get("/health/readiness")
    async def readiness():
        # In the future, check DB/Redis connections here
        return {"status": "ready"}

    # --- PROVIDER REGISTRY ---
    # Dynamically populate the ProviderRegistry from the real provider implementations
    # registered in the ProviderFactory.
    from dronzer.application.registry.provider import ProviderRegistry
    from dronzer.infrastructure.providers.factory import ProviderFactory

    registry = ProviderRegistry()
    ProviderFactory._initialize_registry()
    for provider_name in ProviderFactory._registry:
        try:
            provider_instance = ProviderFactory.get_provider(provider_name)
            registry.register(provider_instance)
        except Exception:
            pass  # Skip providers that fail to instantiate (e.g., missing optional deps)
    app.state.provider_registry = registry

    # --- PIPELINE WIRING ---
    # Wire the real decision engine, failover engine, and metrics tracker.
    from dronzer.application.orchestration.decision import DecisionIntelligenceEngine
    from dronzer.application.orchestration.failover import FailoverEngine
    from dronzer.application.orchestration.health import HealthEngine
    from dronzer.application.orchestration.pipeline import RequestPipeline
    from dronzer.application.orchestration.postgres_metrics import PostgresMetricsTracker

    decision_engine = DecisionIntelligenceEngine()
    health_engine = HealthEngine()
    failover_engine = FailoverEngine(health_engine)
    metrics_tracker = PostgresMetricsTracker()

    app.state.pipeline = RequestPipeline(
        decision_engine=decision_engine,
        failover_engine=failover_engine,
        metrics=metrics_tracker,
    )
    # -----------------------------------------------

    from dronzer.presentation.api.admin.router import admin_router
    from dronzer.presentation.api.router import v1_router

    app.include_router(v1_router)
    app.include_router(admin_router)

    return app
