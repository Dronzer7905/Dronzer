import structlog
from fastapi import APIRouter, Request

from dronzer.presentation.schemas.openai import EmbeddingRequest

logger = structlog.get_logger("dronzer.api.v1.embeddings")
router = APIRouter(prefix="/embeddings", tags=["Embeddings"])

@router.post("")
async def create_embeddings(
    request: Request,
    body: EmbeddingRequest
):
    """
    OpenAI-compatible /v1/embeddings endpoint.
    Routes the request through the Orchestration Engine.
    """
    # This acts as a stub pointing to the orchestration pipeline.
    # In full phase, pipeline.execute_embeddings() would be called here.
    body.model_dump(exclude_unset=True)
    logger.info("Received embeddings request", model=body.model)

    # Fake response for foundation testing
    return {
        "object": "list",
        "data": [
            {
                "object": "embedding",
                "embedding": [0.0023, -0.0093, 0.0123], # truncated
                "index": 0
            }
        ],
        "model": body.model,
        "usage": {
            "prompt_tokens": 8,
            "total_tokens": 8
        }
    }
