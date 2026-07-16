import asyncio
import json
import uuid
from collections.abc import Callable
from datetime import UTC, datetime

import structlog
from redis.asyncio import Redis

logger = structlog.get_logger("dronzer.worker.queue")


class BackgroundWorker:
    """
    Enterprise asynchronous background worker using Redis.
    Supports priorities, retries, delays, and a Dead Letter Queue (DLQ).
    """

    def __init__(self, redis_client: Redis, queue_name: str = "dronzer:jobs"):
        self.redis = redis_client
        self.queue_name = queue_name
        self.dlq_name = f"{queue_name}:dlq"
        self.registry: dict[str, Callable] = {}
        self._is_running = False

    def register(self, task_name: str, func: Callable):
        """Registers a function to be executed by the worker."""
        self.registry[task_name] = func
        logger.info("Task registered", task_name=task_name)

    async def enqueue(
        self,
        task_name: str,
        payload: dict,
        priority: int = 0,
        delay_seconds: int = 0,
        max_retries: int = 3,
    ):
        """Enqueues a job. High priority tasks (higher number) jump the line."""
        job_id = str(uuid.uuid4())
        job = {
            "id": job_id,
            "task": task_name,
            "payload": payload,
            "retries_left": max_retries,
            "max_retries": max_retries,
            "created_at": datetime.now(UTC).isoformat(),
        }

        if delay_seconds > 0:
            # Add to a sorted set for delayed execution
            execute_at = datetime.now(UTC).timestamp() + delay_seconds
            await self.redis.zadd(f"{self.queue_name}:delayed", {json.dumps(job): execute_at})
            logger.debug("Job delayed", job_id=job_id, delay=delay_seconds)
        else:
            # Add to priority queue
            await self.redis.zadd(self.queue_name, {json.dumps(job): priority})
            logger.debug("Job enqueued", job_id=job_id, priority=priority)

        return job_id

    async def _move_dlq(self, job: dict, error: str):
        """Moves a fatally failed job to the Dead Letter Queue."""
        job["error"] = error
        job["failed_at"] = datetime.now(UTC).isoformat()
        import typing

        await typing.cast(typing.Awaitable[Any], self.redis.lpush(self.dlq_name, json.dumps(job)))
        logger.error("Job moved to DLQ", job_id=job["id"], error=error)

    async def start(self):
        """Starts the worker polling loop."""
        self._is_running = True
        logger.info("Worker started", queue=self.queue_name)

        while self._is_running:
            try:
                # 1. Process Delayed Jobs
                now = datetime.now(UTC).timestamp()
                delayed_jobs = await self.redis.zrangebyscore(f"{self.queue_name}:delayed", 0, now)
                for dj in delayed_jobs:
                    await self.redis.zrem(f"{self.queue_name}:delayed", dj)
                    await self.redis.zadd(self.queue_name, {dj: 0})  # Move to active queue

                # 2. Process Active Jobs (Blocking pop highest priority)
                # BZPOPMAX blocks until an item is available or timeout hits
                job_data = await self.redis.bzpopmax(self.queue_name, timeout=1.0)
                if not job_data:
                    continue

                # bzpopmax returns a tuple: (queue_name, member, score)
                _, raw_job, score = job_data
                job = json.loads(raw_job)

                # Execute
                task_func = self.registry.get(job["task"])
                if not task_func:
                    await self._move_dlq(job, "Task not registered")
                    continue

                logger.info("Executing job", job_id=job["id"], task=job["task"])
                try:
                    if asyncio.iscoroutinefunction(task_func):
                        await task_func(**job["payload"])
                    else:
                        task_func(**job["payload"])
                    logger.info("Job completed", job_id=job["id"])
                except Exception as e:
                    logger.exception("Job failed", job_id=job["id"], error=str(e))
                    if job["retries_left"] > 0:
                        job["retries_left"] -= 1
                        # Exponential backoff retry
                        delay = (job["max_retries"] - job["retries_left"]) ** 2 * 5
                        await self.enqueue(
                            job["task"],
                            job["payload"],
                            priority=-1,
                            delay_seconds=delay,
                            max_retries=job["retries_left"],
                        )
                    else:
                        await self._move_dlq(job, str(e))

            except Exception as e:
                logger.error("Worker polling error", error=str(e))
                await asyncio.sleep(1)

    async def stop(self):
        """Gracefully shuts down the worker."""
        logger.info("Worker shutting down gracefully")
        self._is_running = False
