import asyncio
from collections.abc import Awaitable, Callable
from typing import Any

import structlog

logger = structlog.get_logger("dronzer.orchestration.retry")


class RetryEngine:
    """
    Executes a callable with exponential backoff and jitter.
    """

    @staticmethod
    async def execute_with_retry(
        func: Callable[..., Awaitable[Any]],
        max_attempts: int = 3,
        base_delay_ms: int = 1000,
        retryable_exceptions: tuple = (Exception,),
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Executes the provided async function.
        Retries upon encountering exceptions listed in retryable_exceptions.
        """
        attempt = 1
        while True:
            try:
                return await func(*args, **kwargs)
            except retryable_exceptions as e:
                if attempt >= max_attempts:
                    logger.error(
                        "Max retry attempts exhausted",
                        attempt=attempt,
                        max=max_attempts,
                        exc_info=e,
                    )
                    raise e

                # Exponential backoff: 1s, 2s, 4s, etc.
                delay = (base_delay_ms * (2 ** (attempt - 1))) / 1000.0

                logger.warning(
                    "Upstream call failed, retrying", attempt=attempt, delay_sec=delay, error=str(e)
                )
                await asyncio.sleep(delay)
                attempt += 1
