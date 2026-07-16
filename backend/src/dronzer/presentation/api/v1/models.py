import time

import structlog
from fastapi import APIRouter, Request

from dronzer.application.registry.provider import ProviderRegistry
from dronzer.presentation.schemas.openai import ModelCard, ModelListResponse

logger = structlog.get_logger("dronzer.api.v1.models")
router = APIRouter(prefix="/models", tags=["Models"])


@router.get("", response_model=ModelListResponse)
async def list_models(request: Request):
    """
    OpenAI-compatible /v1/models endpoint.
    Returns all models available through the loaded AI Providers.
    """
    # Grab the provider registry from app state
    registry: ProviderRegistry = request.app.state.provider_registry

    cards = []
    # For Phase 14 foundation, we mock the dynamic model list from DB
    # In full implementation, we'd query the DB for models where is_active=True

    for provider in registry.get_all():
        # Fake cards for demonstration of gateway routing capabilities
        cards.append(
            ModelCard(
                id=f"{provider.provider_name}-default",
                created=int(time.time()),
                owned_by=provider.provider_name,
            )
        )

    return ModelListResponse(data=cards)


@router.get("/{model_id}", response_model=ModelCard)
async def get_model(request: Request, model_id: str):
    """
    OpenAI-compatible /v1/models/{model_id} endpoint.
    """
    return ModelCard(id=model_id, created=int(time.time()), owned_by="dronzer-gateway")
