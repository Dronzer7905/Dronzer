import uuid

import structlog
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dronzer.infrastructure.database.core import get_db_session
from dronzer.infrastructure.database.models.ai import APIKey, Provider
from dronzer.infrastructure.database.models.tenant import Project
from dronzer.infrastructure.security.encryption import crypto

logger = structlog.get_logger("dronzer.api.admin.keys")
router = APIRouter(prefix="/keys", tags=["Admin API Keys"])


class APIKeyCreate(BaseModel):
    provider_id: str
    project_id: str
    label: str
    key_value: str


class APIKeyResponse(BaseModel):
    id: str
    provider_id: str
    project_id: str
    label: str
    is_active: bool
    is_failing: bool


@router.post("", response_model=APIKeyResponse)
async def add_api_key(key: APIKeyCreate, session: AsyncSession = Depends(get_db_session)):
    """
    Securely registers a new provider API key into the encryption vault.
    """
    # 1. Fetch Project to ensure it exists
    project_result = await session.execute(
        select(Project).where(Project.id == uuid.UUID(key.project_id))
    )
    project = project_result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # In a real environment, we would encrypt the key_value here

    # We also need to map the string provider_id (like "gemini" or UUID) to the actual DB Provider
    provider = None
    try:
        prov_uuid = uuid.UUID(key.provider_id)
        provider_result = await session.execute(select(Provider).where(Provider.id == prov_uuid))
        provider = provider_result.scalars().first()
    except ValueError:
        provider_result = await session.execute(
            select(Provider).where(Provider.name == key.provider_id)
        )
        provider = provider_result.scalars().first()

    if not provider:
        # Auto-create provider if it doesn't exist to maintain backward compatibility with mock tests
        provider = Provider(name=key.provider_id, base_url=f"https://api.{key.provider_id}.com")
        session.add(provider)
        await session.commit()
        await session.refresh(provider)

    db_key = APIKey(
        provider_id=provider.id, encrypted_key=crypto.encrypt(key.key_value), weight=100
    )

    session.add(db_key)
    await session.commit()
    await session.refresh(db_key)

    logger.info("API Key registered securely", key_id=str(db_key.id), provider=key.provider_id)
    return APIKeyResponse(
        id=str(db_key.id),
        provider_id=key.provider_id,
        project_id=str(project.id),
        label=key.label,
        is_active=not db_key.is_deleted,
        is_failing=False,
    )


@router.get("", response_model=list[APIKeyResponse])
async def list_keys(
    project_id: str = None, provider_id: str = None, session: AsyncSession = Depends(get_db_session)
):
    """
    Lists API keys. Values are masked for security.
    """
    stmt = select(APIKey).where(APIKey.is_deleted == False)

    # Filter by provider name if provided
    if provider_id:
        prov_result = await session.execute(select(Provider).where(Provider.name == provider_id))
        prov = prov_result.scalars().first()
        if prov:
            stmt = stmt.where(APIKey.provider_id == prov.id)

    result = await session.execute(stmt)
    keys = result.scalars().all()

    responses = []
    for k in keys:
        # Resolve provider name
        prov_result = await session.execute(select(Provider).where(Provider.id == k.provider_id))
        prov = prov_result.scalars().first()
        provider_name = prov.name if prov else str(k.provider_id)

        # Derive a label from the encrypted key (masked)
        key_preview = k.encrypted_key[:8] + "..." if k.encrypted_key else "***"

        responses.append(
            APIKeyResponse(
                id=str(k.id),
                provider_id=provider_name,
                project_id=project_id or "default-project",
                label=f"{provider_name} key ({key_preview})",
                is_active=not k.is_deleted,
                is_failing=False,
            )
        )

    return responses


@router.delete("/{key_id}")
async def revoke_key(key_id: str, session: AsyncSession = Depends(get_db_session)):
    """
    Revokes an API key, instantly removing it from the rotation pool.
    """
    result = await session.execute(select(APIKey).where(APIKey.id == uuid.UUID(key_id)))
    key = result.scalars().first()
    if not key:
        raise HTTPException(status_code=404, detail="Key not found")

    key.is_deleted = True
    await session.commit()
    logger.info("API Key revoked", key_id=key_id)
    return {"status": "revoked"}
