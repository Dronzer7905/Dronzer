import asyncio
from typing import Any

import structlog

logger = structlog.get_logger("dronzer.llmops.compare")


class ModelComparisonEngine:
    """
    Executes a specific Prompt concurrently across multiple Foundation Models.
    Used by Prompt Engineers in the UI to visually inspect side-by-side differences
    in output quality, tone, and formatting.
    """

    def __init__(self, ai_gateway: Any = None):
        self.gateway = ai_gateway

    async def execute_side_by_side(
        self, prompt_text: str, variables: dict[str, Any], target_models: list[str]
    ) -> dict[str, Any]:
        """
        Dispatches concurrent execution requests to the Gateway.
        """
        logger.info(f"Initiating side-by-side comparison for models: {target_models}")

        # Compile prompt
        # compiled_prompt = compiler.render(prompt_text, variables)

        async def _execute_model(model_name: str):
            # mock gateway execution
            await asyncio.sleep(0.5)  # simulate network latency
            return {
                "model": model_name,
                "output": f"[{model_name}] Hello, here is my reasoning...",
                "latency_ms": 500,
                "cost_usd": 0.001,
            }

        # Execute all models concurrently
        tasks = [_execute_model(model) for model in target_models]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Format results, handling potential failures from individual providers
        comparison_results = {}
        for i, model_name in enumerate(target_models):
            res = results[i]
            if isinstance(res, Exception):
                comparison_results[model_name] = {"error": str(res), "success": False}
            else:
                import typing

                success_res = typing.cast(dict[str, Any], res)
                success_res["success"] = True
                comparison_results[model_name] = success_res

        logger.info("Side-by-side execution complete")
        return comparison_results
