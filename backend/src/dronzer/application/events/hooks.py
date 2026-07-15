from collections.abc import Callable
from enum import Enum
from typing import Any

import structlog

logger = structlog.get_logger("dronzer.events.hooks")

class HookPoint(str, Enum):
    """
    Standard lifecycle points where extensions can inject logic.
    """
    BEFORE_STARTUP = "before_startup"
    AFTER_STARTUP = "after_startup"
    BEFORE_SHUTDOWN = "before_shutdown"
    BEFORE_REQUEST = "before_request"
    AFTER_REQUEST = "after_request"
    BEFORE_ROUTING = "before_routing"
    AFTER_ROUTING = "after_routing"
    BEFORE_PROVIDER = "before_provider"
    AFTER_PROVIDER = "after_provider"

class HookManager:
    """
    Manages synchronous and asynchronous lifecycle hooks for extensions.
    Unlike the Event Bus, Hooks are executed sequentially and can mutate the payload.
    """
    def __init__(self):
        self._hooks: dict[HookPoint, list[Callable]] = {point: [] for point in HookPoint}

    def register(self, point: HookPoint, callback: Callable):
        """Registers a hook callback for a specific lifecycle point."""
        self._hooks[point].append(callback)
        logger.debug(f"Hook registered for {point.value}")

    async def execute_async(self, point: HookPoint, payload: Any = None) -> Any:
        """
        Executes all hooks registered at this point sequentially.
        If a hook returns a mutated payload, it is passed to the next hook.
        """
        current_payload = payload

        for hook in self._hooks[point]:
            try:
                result = await hook(current_payload)
                # If the hook returns data, assume it's mutating the payload
                if result is not None:
                    current_payload = result
            except Exception as e:
                logger.error(f"Hook execution failed at {point.value}", error=str(e))
                # Depending on strictness, we might want to re-raise or continue.
                # For v1.0, we log and continue to prevent brittle extensions from crashing the gateway.
                continue

        return current_payload
