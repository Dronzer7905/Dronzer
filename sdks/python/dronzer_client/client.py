import httpx
from typing import Dict, Any, Optional

class DronzerClient:
    """
    Official Python SDK for the Dronzer Enterprise Platform.
    Provides async-first access to LLMOps, Workflows, and Agents.
    """
    
    def __init__(self, api_key: str, base_url: str = "https://api.dronzer.io/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.api_key}"}
        )

    async def execute_prompt(self, prompt_id: str, variables: Dict[str, Any]) -> str:
        """
        Executes a Prompt Template using the Dronzer AI Gateway.
        Handles dynamic traffic routing (A/B testing) automatically server-side.
        """
        response = await self._client.post(
            f"/llmops/prompts/{prompt_id}/execute",
            json={"variables": variables}
        )
        response.raise_for_status()
        return response.json().get("output")
        
    async def close(self):
        await self._client.aclose()
