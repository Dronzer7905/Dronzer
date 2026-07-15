import uuid

import structlog
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dronzer.infrastructure.database.core import get_db_session
from dronzer.infrastructure.database.models.ai import Model, Provider
from dronzer.presentation.schemas.admin import ModelConfigResponse, ModelCreate

logger = structlog.get_logger("dronzer.api.admin.models")
router = APIRouter(prefix="/models", tags=["Admin Models"])


@router.get("", response_model=list[ModelConfigResponse])
async def list_models(
    provider_id: str = None,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Lists all models from the database, optionally filtered by provider.
    """
    stmt = select(Model).where(Model.is_deleted == False)

    if provider_id:
        # provider_id from the frontend can be a name or a UUID
        try:
            prov_uuid = uuid.UUID(provider_id)
            stmt = stmt.where(Model.provider_id == prov_uuid)
        except ValueError:
            # It's a name string — resolve to UUID first
            prov_result = await session.execute(
                select(Provider).where(Provider.name == provider_id.lower())
            )
            prov = prov_result.scalars().first()
            if prov:
                stmt = stmt.where(Model.provider_id == prov.id)
            else:
                return []  # Provider not found → no models

    result = await session.execute(stmt)
    models = result.scalars().all()

    responses = []
    for m in models:
        # Resolve provider name for display
        prov_result = await session.execute(select(Provider).where(Provider.id == m.provider_id))
        prov = prov_result.scalars().first()
        provider_display = prov.name if prov else str(m.provider_id)

        responses.append(
            ModelConfigResponse(
                id=str(m.id),
                provider_id=provider_display,
                name=m.name,
                is_enabled=m.is_active,
                context_window=m.context_window,
                capabilities=m.capabilities if m.capabilities else {},
            )
        )

    return responses


@router.post("", response_model=ModelConfigResponse)
async def create_model(
    model: ModelCreate,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Creates a new model configuration, persisted to PostgreSQL.
    """
    # Resolve provider_id: could be a name or UUID
    provider = None
    try:
        prov_uuid = uuid.UUID(model.provider_id)
        prov_result = await session.execute(select(Provider).where(Provider.id == prov_uuid))
        provider = prov_result.scalars().first()
    except ValueError:
        prov_result = await session.execute(
            select(Provider).where(Provider.name == model.provider_id.lower())
        )
        provider = prov_result.scalars().first()

    if not provider:
        raise HTTPException(
            status_code=400,
            detail=f"Provider '{model.provider_id}' not found. Register the provider first.",
        )

    # Check if a model with the same name already exists for this provider
    existing = await session.execute(
        select(Model).where(
            Model.name == model.name,
            Model.provider_id == provider.id,
            Model.is_deleted == False,
        )
    )
    if existing.scalars().first():
        raise HTTPException(
            status_code=400,
            detail=f"Model '{model.name}' already exists for provider '{provider.name}'.",
        )

    db_model = Model(
        name=model.name,
        provider_id=provider.id,
        context_window=model.context_window,
        capabilities={"chat": True},
        is_active=True,
    )
    session.add(db_model)
    await session.flush()
    await session.commit()
    await session.refresh(db_model)

    logger.info("Model created", model_id=str(db_model.id), provider=provider.name)

    return ModelConfigResponse(
        id=str(db_model.id),
        provider_id=provider.name,
        name=db_model.name,
        is_enabled=db_model.is_active,
        context_window=db_model.context_window,
        capabilities=db_model.capabilities if db_model.capabilities else {},
    )


@router.patch("/{model_id}")
async def update_model_config(
    model_id: str,
    is_enabled: bool = None,
    context_window: int = None,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Updates the configuration of a specific model in the database.
    """
    try:
        m_uuid = uuid.UUID(model_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid model ID format")

    result = await session.execute(select(Model).where(Model.id == m_uuid))
    db_model = result.scalars().first()
    if not db_model:
        raise HTTPException(status_code=404, detail="Model not found")

    if is_enabled is not None:
        db_model.is_active = is_enabled
    if context_window is not None:
        db_model.context_window = context_window

    await session.commit()
    await session.refresh(db_model)

    # Resolve provider name
    prov_result = await session.execute(select(Provider).where(Provider.id == db_model.provider_id))
    prov = prov_result.scalars().first()

    logger.info("Model config updated", model_id=model_id, is_enabled=db_model.is_active)

    return ModelConfigResponse(
        id=str(db_model.id),
        provider_id=prov.name if prov else str(db_model.provider_id),
        name=db_model.name,
        is_enabled=db_model.is_active,
        context_window=db_model.context_window,
        capabilities=db_model.capabilities if db_model.capabilities else {},
    )
