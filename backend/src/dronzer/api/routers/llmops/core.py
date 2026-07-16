from typing import Any

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(
    prefix="/v1/llmops",
    tags=["LLMOps Platform"],
)


class PromptCreateRequest(BaseModel):
    name: str
    template_text: str  # Jinja2 syntax
    variables_schema: dict[str, Any]
    default_model: str = "openai/gpt-4o"


@router.post("/prompts", status_code=status.HTTP_201_CREATED)
async def create_prompt(req: PromptCreateRequest):
    """
    Registers a new Prompt in the registry and creates an initial 'v1.0.0-draft' version.
    """
    return {"prompt_id": "prmpt_123", "version_tag": "v1.0.0-draft", "status": "created"}


@router.get("/prompts/{prompt_id}/analytics")
async def get_prompt_analytics(prompt_id: str, days: int = 7):
    """
    Fetches aggregated telemetry (Cost, Latency, Token Usage) for the Dashboard.
    """
    return {
        "metrics": {
            "total_executions": 45000,
            "average_latency_ms": 850,
            "error_rate_pct": 1.2,
            "total_cost_usd": 125.50,
        }
    }


class CompareRequest(BaseModel):
    prompt_text: str
    variables: dict[str, Any]
    models: list[str]


@router.post("/experiments/compare")
async def run_side_by_side_comparison(req: CompareRequest):
    """
    Executes a prompt across multiple models concurrently.
    Used by the PromptOps Lab UI to visually inspect output differences.
    """
    if len(req.models) > 4:
        raise HTTPException(status_code=400, detail="Maximum 4 models allowed per comparison")

    return {
        "openai/gpt-4o": {"success": True, "output": "Output from GPT-4o", "latency_ms": 500},
        "anthropic/claude-3-5-sonnet": {
            "success": True,
            "output": "Output from Claude",
            "latency_ms": 450,
        },
        "meta/llama-3-70b": {"success": True, "output": "Output from Llama 3", "latency_ms": 600},
    }
