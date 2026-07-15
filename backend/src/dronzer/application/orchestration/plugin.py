from typing import Any, Protocol

from dronzer.application.orchestration.context import DecisionContext, RequestContext


class IPluginHook(Protocol):
    """
    Interface for external Python plugins to intercept the orchestration lifecycle.
    """

    async def before_routing(self, context: RequestContext) -> RequestContext:
        """Called before the Decision Engine begins evaluating candidates."""
        return context

    async def before_provider_selection(self, context: DecisionContext) -> DecisionContext:
        """Called immediately before candidates are scored."""
        return context

    async def after_response(self, response: dict[str, Any], context: DecisionContext) -> dict[str, Any]:
        """Called after a successful upstream LLM response is received."""
        return response

    async def after_failure(self, error: Exception, context: DecisionContext) -> None:
        """Called if all retries and failovers are exhausted."""
        pass
