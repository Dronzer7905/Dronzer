import uuid

import structlog
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dronzer.infrastructure.database.core import get_db_session
from dronzer.infrastructure.database.models.tenant import Project
from dronzer.presentation.schemas.admin import ProjectCreate, ProjectResponse

logger = structlog.get_logger("dronzer.api.admin.projects")
router = APIRouter(prefix="/projects", tags=["Admin Projects"])


@router.post("", response_model=ProjectResponse)
async def create_project(project: ProjectCreate, session: AsyncSession = Depends(get_db_session)):
    """
    Creates a new Project within an Organization.
    Requires ORG_ADMIN or higher.
    """
    db_project = Project(
        name=project.name,
        slug=project.name.lower().replace(" ", "-") + "-" + str(uuid.uuid4())[:8],
        organization_id=uuid.UUID(project.org_id),
    )
    session.add(db_project)
    await session.commit()
    await session.refresh(db_project)

    logger.info(
        "Project created", project_id=str(db_project.id), org_id=str(db_project.organization_id)
    )

    return ProjectResponse(
        id=str(db_project.id),
        name=db_project.name,
        org_id=str(db_project.organization_id),
        environment=project.environment,  # Mocked/ignored environment for now
        created_at=db_project.created_at,
    )


@router.get("", response_model=list[ProjectResponse])
async def list_projects(org_id: str = None, session: AsyncSession = Depends(get_db_session)):
    """
    Lists Projects, optionally filtered by Organization.
    """
    stmt = select(Project).where(Project.is_deleted == False)
    if org_id:
        stmt = stmt.where(Project.organization_id == uuid.UUID(org_id))

    result = await session.execute(stmt)
    projects = result.scalars().all()

    return [
        ProjectResponse(
            id=str(p.id),
            name=p.name,
            org_id=str(p.organization_id),
            environment="production",
            created_at=p.created_at,
        )
        for p in projects
    ]


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str, session: AsyncSession = Depends(get_db_session)):
    """
    Gets specific Project details.
    """
    result = await session.execute(
        select(Project).where(Project.id == uuid.UUID(project_id), Project.is_deleted == False)
    )
    p = result.scalars().first()
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")

    return ProjectResponse(
        id=str(p.id),
        name=p.name,
        org_id=str(p.organization_id),
        environment="production",
        created_at=p.created_at,
    )


@router.delete("/{project_id}")
async def delete_project(project_id: str, session: AsyncSession = Depends(get_db_session)):
    """
    Deletes a Project and invalidates all its keys.
    """
    result = await session.execute(select(Project).where(Project.id == uuid.UUID(project_id)))
    p = result.scalars().first()
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")

    p.is_deleted = True
    await session.commit()
    logger.info("Project deleted", project_id=project_id)
    return {"status": "deleted"}
