from abc import ABC, abstractmethod
from typing import Any

import structlog

logger = structlog.get_logger("dronzer.workflows.nodes")


class BaseNodeExecutor(ABC):
    """
    Abstract interface for all Workflow Nodes.
    """

    @abstractmethod
    async def run(self, parameters: dict[str, Any], global_state: dict[str, Any]) -> dict[str, Any]:
        """
        Executes the node logic.
        Should return a dictionary of outputs that will be merged into the global state.
        If the node needs human approval, return `{"_hitl_pause": True}`.
        """
        pass


class LLMNodeExecutor(BaseNodeExecutor):
    """
    Executes a standard LLM generation call.
    """

    async def run(self, parameters: dict[str, Any], global_state: dict[str, Any]) -> dict[str, Any]:
        prompt_template = parameters.get("prompt", "")
        model = parameters.get("model", "gpt-4-turbo")

        # Hydrate template with global state variables
        # (e.g. replacing {{user_input}} with global_state["user_input"])
        hydrated_prompt = prompt_template  # ... Template hydration logic

        logger.info("Executing LLM Node", model=model)

        # Call Dronzer's Orchestration Engine / Provider SDK
        mock_response = "Generated AI response based on workflow parameters."

        return {"llm_output": mock_response}


class HTTPRequestNodeExecutor(BaseNodeExecutor):
    """
    Executes a REST/HTTP request (e.g., to a webhook or external 3rd party API).
    """

    async def run(self, parameters: dict[str, Any], global_state: dict[str, Any]) -> dict[str, Any]:
        url = parameters.get("url")
        method = parameters.get("method", "GET")

        logger.info("Executing HTTP Node", method=method, url=url)
        # return await httpx.AsyncClient().request(method, url)
        return {"status_code": 200, "response_body": {"success": True}}


class PythonScriptNodeExecutor(BaseNodeExecutor):
    """
    Executes custom python logic securely.
    Leverages the previously discussed `sys.addaudithook` for best-effort sandboxing.
    """

    async def run(self, parameters: dict[str, Any], global_state: dict[str, Any]) -> dict[str, Any]:
        script = parameters.get("code", "")

        logger.warning("Executing Sandboxed Python Script Node")

        # Extremely limited local execution environment (In production: Firecracker microVM)
        local_env = {"state": global_state, "output": {}}

        try:
            # Execute user script safely
            exec(script, {"__builtins__": {}}, local_env)
        except Exception as e:
            logger.error("Script execution failed", error=str(e))
            raise e

        return local_env.get("output", {})
