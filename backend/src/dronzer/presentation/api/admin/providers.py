import uuid
import structlog
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from dronzer.application.registry.provider import ProviderRegistry
from dronzer.infrastructure.database.core import get_db_session
from dronzer.infrastructure.database.models.ai import Provider, Model
from dronzer.presentation.schemas.admin import ProviderConfigResponse

logger = structlog.get_logger("dronzer.api.admin.providers")
router = APIRouter(prefix="/providers", tags=["Admin Providers"])

class ProviderCreate(BaseModel):
    name: str
    priority: int = 100
    weight: float = 1.0
    models: list[str] = []

@router.post("", response_model=ProviderConfigResponse)
async def create_provider(data: ProviderCreate, request: Request, session: AsyncSession = Depends(get_db_session)):
    """
    Dynamically registers a new provider in the Gateway DB and memory registry.
    """
    from dronzer.infrastructure.providers.factory import ProviderFactory

    # Check DB if it exists
    existing = await session.execute(select(Provider).where(Provider.name == data.name.lower()))
    if existing.scalars().first():
        raise HTTPException(status_code=400, detail="Provider already exists")

    # Save to DB
    db_prov = Provider(
        name=data.name.lower(),
        base_url=f"https://api.{data.name.lower()}.com",
        is_active=True
    )
    session.add(db_prov)
    await session.flush()
    
    # Save models
    for m_name in data.models:
        db_model = Model(
            name=m_name,
            provider_id=db_prov.id,
            is_active=True
        )
        session.add(db_model)
        
    await session.commit()
    await session.refresh(db_prov)

    # Register in memory registry
    registry: ProviderRegistry = request.app.state.provider_registry
    if not registry.get(data.name.lower()):
        try:
            real_provider = ProviderFactory.get_provider(data.name.lower())
            registry.register(real_provider)
        except ValueError:
            pass  # No SDK available for this provider name — DB-only registration
    
    logger.info("New provider created via admin API", provider_name=data.name)
    
    return ProviderConfigResponse(
        id=str(db_prov.id),
        name=db_prov.name.capitalize(),
        is_enabled=db_prov.is_active,
        priority=data.priority,
        weight=data.weight,
        models=data.models
    )

@router.get("", response_model=list[ProviderConfigResponse])
async def list_providers(request: Request, session: AsyncSession = Depends(get_db_session)):
    """
    Lists all loaded AI providers from the DB.
    """
    result = await session.execute(select(Provider).where(Provider.is_deleted == False))
    providers = result.scalars().all()

    response = []
    for p in providers:
        # Load models
        models_result = await session.execute(select(Model).where(Model.provider_id == p.id))
        models = [m.name for m in models_result.scalars().all()]
        
        response.append(ProviderConfigResponse(
            id=str(p.id),
            name=p.name.capitalize(),
            is_enabled=p.is_active,
            priority=100,
            weight=100,
            models=models,
        ))

    return response

@router.post("/{provider_id}/disable")
async def disable_provider(provider_id: str, request: Request, session: AsyncSession = Depends(get_db_session)):
    """
    Dynamically disables a provider globally across all tenants.
    """
    # Try UUID lookup first, then fall back to name
    p = None
    try:
        prov_uuid = uuid.UUID(provider_id)
        result = await session.execute(select(Provider).where(Provider.id == prov_uuid))
        p = result.scalars().first()
    except ValueError:
        pass
    if not p:
        result = await session.execute(select(Provider).where(Provider.name == provider_id))
        p = result.scalars().first()
    if not p:
        raise HTTPException(status_code=404, detail="Provider not found in DB")
        
    p.is_active = False
    await session.commit()
    logger.warning("Provider disabled by admin", provider_id=provider_id)
    return {"status": "disabled", "provider_id": provider_id}

@router.post("/{provider_id}/enable")
async def enable_provider(provider_id: str, request: Request, session: AsyncSession = Depends(get_db_session)):
    """
    Re-enables a provider globally.
    """
    # Try UUID lookup first, then fall back to name
    p = None
    try:
        prov_uuid = uuid.UUID(provider_id)
        result = await session.execute(select(Provider).where(Provider.id == prov_uuid))
        p = result.scalars().first()
    except ValueError:
        pass
    if not p:
        result = await session.execute(select(Provider).where(Provider.name == provider_id))
        p = result.scalars().first()
    if not p:
        raise HTTPException(status_code=404, detail="Provider not found in DB")
        
    p.is_active = True
    await session.commit()
    logger.info("Provider enabled by admin", provider_id=provider_id)
    return {"status": "enabled", "provider_id": provider_id}
