import asyncio
import uuid
from collections.abc import Awaitable, Callable
from datetime import UTC, datetime
from typing import Any

import structlog

logger = structlog.get_logger("dronzer.events.bus")

class AsyncEventBus:
    """
    In-memory Pub/Sub Event Bus for extension communication.
    Supports asynchronous event emission and subscription.
    """
    def __init__(self):
        # Maps event topics to a list of async callbacks
        self._subscribers: dict[str, list[Callable[[dict[str, Any]], Awaitable[None]]]] = {}

    def subscribe(self, topic: str, callback: Callable[[dict[str, Any]], Awaitable[None]]):
        """Registers a callback to be triggered when an event is published to the topic."""
        if topic not in self._subscribers:
            self._subscribers[topic] = []
        self._subscribers[topic].append(callback)
        logger.debug(f"Subscribed to topic: {topic}")

    def unsubscribe(self, topic: str, callback: Callable):
        """Removes a previously registered callback."""
        if topic in self._subscribers and callback in self._subscribers[topic]:
            self._subscribers[topic].remove(callback)

    async def publish(self, topic: str, payload: dict[str, Any]):
        """
        Publishes an event to a topic asynchronously.
        Does not block the publisher waiting for subscribers to finish.
        """
        if topic not in self._subscribers or not self._subscribers[topic]:
            return

        event_envelope = {
            "id": str(uuid.uuid4()),
            "topic": topic,
            "timestamp": datetime.now(UTC).isoformat(),
            "payload": payload
        }

        callbacks = self._subscribers[topic]

        # Fire and forget execution for all subscribers
        for callback in callbacks:
            asyncio.create_task(self._safe_execute(topic, callback, event_envelope))

    async def _safe_execute(self, topic: str, callback: Callable, event: dict[str, Any]):
        """Wraps callback execution to prevent a single failing subscriber from crashing the bus."""
        try:
            await callback(event)
        except Exception as e:
            logger.error(f"Event subscriber failed for topic {topic}", error=str(e), event_id=event["id"])
