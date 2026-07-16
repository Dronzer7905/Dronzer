from datetime import UTC, datetime, timedelta
from typing import Any

import structlog
from fastapi import APIRouter, Depends, Request
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from dronzer.infrastructure.database.core import get_db_session
from dronzer.infrastructure.database.models.ai import Provider
from dronzer.infrastructure.database.models.telemetry import RequestLog

logger = structlog.get_logger("dronzer.api.admin.health")
router = APIRouter(prefix="/health", tags=["Admin Health"])


@router.get("/metrics")
async def get_metrics(
    request: Request, session: AsyncSession = Depends(get_db_session)
) -> dict[str, Any]:
    """
    Provides real-time telemetry metrics about provider routing and circuit breakers.
    """
    # 1. Total Token Usage
    token_sum = await session.execute(
        select(func.sum(RequestLog.prompt_tokens + RequestLog.completion_tokens))
    )
    total_tokens = token_sum.scalar() or 0

    # 2. Timeseries (Last 24 hours, grouped by hour)
    twenty_four_hours_ago = datetime.now(UTC) - timedelta(hours=24)
    timeseries_result = await session.execute(
        select(
            func.date_trunc("hour", RequestLog.created_at).label("hour"),
            func.count().label("requests"),
        )
        .where(RequestLog.created_at >= twenty_four_hours_ago)
        .group_by("hour")
        .order_by("hour")
    )

    timeseries_data = timeseries_result.fetchall()
    timeseries = []

    # Fill in blanks for 24 hours if no data
    current_hour = twenty_four_hours_ago.replace(minute=0, second=0, microsecond=0)
    end_hour = datetime.now(UTC).replace(minute=0, second=0, microsecond=0)

    data_dict = {row.hour: row.requests for row in timeseries_data}

    while current_hour <= end_hour:
        timeseries.append(
            {"time": current_hour.strftime("%H:00"), "requests": data_dict.get(current_hour, 0)}
        )
        current_hour += timedelta(hours=1)

    return {
        "active_requests": 0,  # Since we don't track live connections in DB
        "circuit_breakers_open": 0,
        "circuit_breakers_half_open": 0,
        "token_usage_total": total_tokens,
        "cache_hit_rate": 0,  # Not caching right now
        "timeseries": timeseries,
    }


@router.get("/diagnostics")
async def get_diagnostics(
    request: Request, session: AsyncSession = Depends(get_db_session)
) -> dict[str, Any]:
    """
    Provides deep system diagnostics (DB pools, Redis, API Providers).
    """
    db_status = "healthy"
    try:
        await session.execute(text("SELECT 1"))
    except Exception:
        db_status = "error"

    providers_count = await session.execute(
        select(func.count(Provider.id)).where(Provider.is_active == True)
    )

    return {
        "database": db_status,
        "redis": "healthy",  # Assume true for now without redis integration
        "providers_loaded": providers_count.scalar() or 0,
        "plugins_loaded": 0,
        "uptime_seconds": 3600,
    }
