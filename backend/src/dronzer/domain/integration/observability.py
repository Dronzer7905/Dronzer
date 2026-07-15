import time
from contextlib import contextmanager
from typing import Any

import structlog

logger = structlog.get_logger("dronzer.integration.observability")

class ToolExecutionObserver:
    """
    Middleware that tracks the performance, latency, and failure rates of all Tools.
    Data collected here is shipped to Prometheus/Grafana or the Dronzer Admin Dashboard.
    """

    def __init__(self, metrics_engine: Any = None):
        self.metrics = metrics_engine

    @contextmanager
    def track_execution(self, tool_name: str, tenant_id: str):
        """
        Context manager to track execution time and errors.
        """
        start_time = time.perf_counter()
        status = "success"
        error_msg = None

        try:
            yield
        except Exception as e:
            status = "failed"
            error_msg = str(e)
            raise e
        finally:
            duration_ms = (time.perf_counter() - start_time) * 1000
            self._record_metric(tool_name, tenant_id, duration_ms, status, error_msg)

    def _record_metric(self, tool_name: str, tenant_id: str, duration_ms: float, status: str, error: str):
        """
        Ships the metric to the telemetry backend.
        """
        logger.info(
            "Tool Execution Metric Recorded",
            tool=tool_name,
            tenant_id=tenant_id,
            duration_ms=round(duration_ms, 2),
            status=status
        )

        if self.metrics:
            # Pseudo:
            # self.metrics.histogram("tool_duration_ms", duration_ms, tags={"tool": tool_name})
            # self.metrics.increment("tool_calls_total", tags={"tool": tool_name, "status": status})
            pass
