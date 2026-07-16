import time
import uuid
from collections.abc import Awaitable, Callable

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from structlog.contextvars import bind_contextvars, clear_contextvars

logger = structlog.get_logger("dronzer.api.observability")


class ObservabilityMiddleware(BaseHTTPMiddleware):
    """
    Injects Trace IDs, tracks request execution time, and provides structured logging context.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        clear_contextvars()

        # Extract or generate Trace ID
        trace_id = request.headers.get("x-request-id", str(uuid.uuid4()))
        bind_contextvars(trace_id=trace_id, path=request.url.path, method=request.method)

        # Attach to request state for downstream use
        request.state.trace_id = trace_id

        start_time = time.perf_counter()

        try:
            response = await call_next(request)

            process_time = time.perf_counter() - start_time
            response.headers["x-request-id"] = trace_id
            response.headers["x-process-time"] = f"{process_time:.4f}"

            logger.info(
                "Request completed", status_code=response.status_code, duration_s=process_time
            )

            return response

        except Exception as e:
            process_time = time.perf_counter() - start_time
            logger.exception("Unhandled request exception", duration_s=process_time, error=str(e))
            raise
