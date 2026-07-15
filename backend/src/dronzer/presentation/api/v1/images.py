import time

import structlog
from fastapi import APIRouter, Request

from dronzer.presentation.schemas.openai import ImageGenerationRequest

logger = structlog.get_logger("dronzer.api.v1.images")
router = APIRouter(prefix="/images", tags=["Images"])

@router.post("/generations")
async def create_image(
    request: Request,
    body: ImageGenerationRequest
):
    """
    OpenAI-compatible /v1/images/generations endpoint.
    Routes the request through the Orchestration Engine.
    """
    logger.info("Received image generation request", prompt=body.prompt)

    # Fake response for foundation testing
    return {
        "created": int(time.time()),
        "data": [
            {
                "url": "https://example.com/generated-image.png"
            }
        ]
    }
