import time
from typing import Any

from fastapi import APIRouter

from dronzer.core.config import settings

router = APIRouter()
START_TIME = time.time()


@router.get("/health", response_model=dict[str, Any])
async def health_check() -> dict[str, Any]:
    """
    Core health check endpoint used by Kubernetes and load balancers.
    """
    uptime = time.time() - START_TIME
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT.value,
        "uptime_seconds": round(uptime, 2),
    }
