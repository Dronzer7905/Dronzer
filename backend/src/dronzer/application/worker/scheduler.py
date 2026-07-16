import asyncio
from datetime import UTC, datetime

import croniter
import structlog

logger = structlog.get_logger("dronzer.worker.scheduler")


class CronScheduler:
    """
    Enterprise cron scheduler for periodic background tasks.
    Evaluates cron expressions and dispatches jobs to the Worker Queue.
    """

    def __init__(self, worker_queue):
        self.queue = worker_queue
        self.jobs = []
        self._is_running = False

    def schedule(self, cron_expr: str, task_name: str, payload: dict = None):
        """Schedules a recurring task using a cron expression."""
        if not croniter.croniter.is_valid(cron_expr):
            raise ValueError(f"Invalid cron expression: {cron_expr}")

        self.jobs.append(
            {
                "cron": cron_expr,
                "task": task_name,
                "payload": payload or {},
                "next_run": croniter.croniter(cron_expr, datetime.now(UTC)).get_next(datetime),
            }
        )
        logger.info("Scheduled cron job", task=task_name, cron=cron_expr)

    async def start(self):
        """Starts the scheduler polling loop."""
        self._is_running = True
        logger.info("Scheduler started")

        while self._is_running:
            now = datetime.now(UTC)
            for job in self.jobs:
                if now >= job["next_run"]:
                    # Dispatch to queue
                    await self.queue.enqueue(job["task"], job["payload"])
                    logger.debug("Dispatched scheduled job", task=job["task"])

                    # Calculate next run
                    job["next_run"] = croniter.croniter(job["cron"], now).get_next(datetime)

            # Sleep until next minute check or similar resolution
            await asyncio.sleep(10)

    async def stop(self):
        """Stops the scheduler."""
        logger.info("Scheduler shutting down")
        self._is_running = False
