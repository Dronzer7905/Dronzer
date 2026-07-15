import hashlib
import secrets
import uuid

import structlog
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dronzer.infrastructure.database.core import get_db_session
from dronzer.infrastructure.database.models.gateway import GatewayKey

logger = structlog.get_logger("dronzer.api.admin.gateway_keys")
router = APIRouter(prefix="/gateway-keys", tags=["Admin Gateway Keys"])


class GatewayKeyCreate(BaseModel):
    label: str
    organization_id: str
    project_id: str | None = None
    task_type: str = "chat"
    model_priorities: list[str] = []
    provider_priorities: list[str] = []


class GatewayKeyResponse(BaseModel):
    id: str
    key_value: str | None = None
    label: str
    organization_id: str
    project_id: str | None = None
    task_type: str
    model_priorities: list[str]
    provider_priorities: list[str]
    is_active: bool
    created_at: str


def _hash_key(raw_key: str) -> str:
    """SHA-256 hash for storing the gateway key securely."""
    return hashlib.sha256(raw_key.encode()).hexdigest()


def _mask_key(raw_or_hash: str) -> str:
    """Returns a masked representation for display purposes."""
    if raw_or_hash.startswith("dz-sk-"):
        return raw_or_hash[:9] + "..." + raw_or_hash[-4:]
    # For hashed keys, show first/last 4 chars of hash
    return raw_or_hash[:4] + "..." + raw_or_hash[-4:]


@router.post("", response_model=GatewayKeyResponse)
async def create_gateway_key(
    key: GatewayKeyCreate,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Generates a new Dronzer Gateway API Key (dz-sk-...).
    The raw key is returned only once at creation time.
    """
    raw_key = f"dz-sk-{secrets.token_urlsafe(32)}"
    hashed = _hash_key(raw_key)

    org_uuid = uuid.UUID(key.organization_id)
    proj_uuid = uuid.UUID(key.project_id) if key.project_id else None

    db_key = GatewayKey(
        hashed_key=hashed,
        label=key.label,
        organization_id=org_uuid,
        project_id=proj_uuid,
        task_type=key.task_type,
        model_priorities=key.model_priorities,
        provider_priorities=key.provider_priorities,
        is_active=True,
    )
    session.add(db_key)
    await session.flush()
    await session.commit()
    await session.refresh(db_key)

    logger.info("Gateway Key generated", key_id=str(db_key.id), label=key.label)

    return GatewayKeyResponse(
        id=str(db_key.id),
        key_value=raw_key,  # Only shown once
        label=db_key.label,
        organization_id=str(db_key.organization_id),
        project_id=str(db_key.project_id) if db_key.project_id else None,
        task_type=db_key.task_type,
        model_priorities=db_key.model_priorities,
        provider_priorities=db_key.provider_priorities,
        is_active=db_key.is_active,
        created_at=db_key.created_at.isoformat() if db_key.created_at else "",
    )


@router.get("", response_model=list[GatewayKeyResponse])
async def list_gateway_keys(
    organization_id: str = None,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Lists Gateway API keys from the database. Full keys are not returned after creation.
    """
    stmt = select(GatewayKey).where(GatewayKey.is_deleted == False)

    if organization_id:
        try:
            org_uuid = uuid.UUID(organization_id)
            stmt = stmt.where(GatewayKey.organization_id == org_uuid)
        except ValueError:
            return []

    result = await session.execute(stmt)
    keys = result.scalars().all()

    return [
        GatewayKeyResponse(
            id=str(k.id),
            key_value=_mask_key(k.hashed_key),  # Masked — never return raw
            label=k.label,
            organization_id=str(k.organization_id),
            project_id=str(k.project_id) if k.project_id else None,
            task_type=k.task_type,
            model_priorities=k.model_priorities,
            provider_priorities=k.provider_priorities,
            is_active=k.is_active,
            created_at=k.created_at.isoformat() if k.created_at else "",
        )
        for k in keys
    ]


@router.delete("/{key_id}")
async def revoke_gateway_key(
    key_id: str,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Revokes a Gateway API key via soft-delete.
    """
    try:
        k_uuid = uuid.UUID(key_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid key ID format")

    result = await session.execute(select(GatewayKey).where(GatewayKey.id == k_uuid))
    db_key = result.scalars().first()
    if not db_key:
        raise HTTPException(status_code=404, detail="Key not found")

    db_key.soft_delete()
    await session.commit()

    logger.info("Gateway Key revoked", key_id=key_id)
    return {"status": "revoked"}
