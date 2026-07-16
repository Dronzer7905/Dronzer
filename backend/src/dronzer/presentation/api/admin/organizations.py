import uuid

import structlog
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dronzer.infrastructure.database.core import get_db_session
from dronzer.infrastructure.database.models.tenant import Organization
from dronzer.presentation.schemas.admin import OrganizationCreate, OrganizationResponse

logger = structlog.get_logger("dronzer.api.admin.organizations")
router = APIRouter(prefix="/organizations", tags=["Admin Organizations"])


@router.post("", response_model=OrganizationResponse)
async def create_organization(
    org: OrganizationCreate, session: AsyncSession = Depends(get_db_session)
):
    """
    Creates a new multi-tenant Organization.
    Requires SUPER_ADMIN.
    """
    db_org = Organization(
        name=org.name,
        slug=org.name.lower().replace(" ", "-") + "-" + str(uuid.uuid4())[:8],
        # If schema requires stripe_customer_id, settings, etc. they have defaults or are nullable
    )
    session.add(db_org)
    await session.commit()
    await session.refresh(db_org)

    logger.info("Organization created", org_id=str(db_org.id), name=db_org.name)
    return OrganizationResponse(
        id=str(db_org.id),
        name=db_org.name,
        billing_email=org.billing_email,
        created_at=db_org.created_at,
        is_active=not db_org.is_deleted,
    )


@router.get("", response_model=list[OrganizationResponse])
async def list_organizations(session: AsyncSession = Depends(get_db_session)):
    """
    Lists all Organizations.
    """
    result = await session.execute(select(Organization).where(Organization.is_deleted == False))
    orgs = result.scalars().all()

    return [
        OrganizationResponse(
            id=str(org.id),
            name=org.name,
            billing_email="admin@dronzer.ai",  # Mocked billing email
            created_at=org.created_at,
            is_active=not org.is_deleted,
        )
        for org in orgs
    ]


@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(org_id: str, session: AsyncSession = Depends(get_db_session)):
    """
    Gets specific Organization details.
    """
    result = await session.execute(
        select(Organization).where(
            Organization.id == uuid.UUID(org_id), Organization.is_deleted == False
        )
    )
    org = result.scalars().first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    return OrganizationResponse(
        id=str(org.id),
        name=org.name,
        billing_email="admin@dronzer.ai",
        created_at=org.created_at,
        is_active=not org.is_deleted,
    )


@router.delete("/{org_id}")
async def delete_organization(org_id: str, session: AsyncSession = Depends(get_db_session)):
    """
    Soft deletes an Organization.
    """
    result = await session.execute(select(Organization).where(Organization.id == uuid.UUID(org_id)))
    org = result.scalars().first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    org.is_deleted = True
    await session.commit()

    logger.info("Organization deactivated", org_id=org_id)
    return {"status": "deleted"}
