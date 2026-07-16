import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dronzer.application.admin.auth import AuthService
from dronzer.infrastructure.database.core import get_db_session
from dronzer.infrastructure.database.models.tenant import User

logger = structlog.get_logger("dronzer.api.admin.auth")
router = APIRouter(prefix="/auth", tags=["Admin Auth"])

# In reality, this would be injected globally via FastAPI Depends
auth_service = AuthService()


class LoginRequest(BaseModel):
    email: str
    password: str


class SetupRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class SetupStatusResponse(BaseModel):
    is_setup: bool


class RefreshRequest(BaseModel):
    refresh_token: str


@router.get("/setup-status", response_model=SetupStatusResponse)
async def check_setup_status(session: AsyncSession = Depends(get_db_session)):
    """
    Checks if the initial superuser has been created.
    """
    stmt = select(User).where(User.is_superuser == True).limit(1)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    return SetupStatusResponse(is_setup=user is not None)


@router.post("/setup", response_model=TokenResponse)
async def setup_initial_admin(
    request: SetupRequest, session: AsyncSession = Depends(get_db_session)
):
    """
    Creates the first superuser account. Can only be called once.
    """
    # Check if already setup
    stmt = select(User).where(User.is_superuser == True).limit(1)
    result = await session.execute(stmt)
    if result.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin user already exists. Initial setup is complete.",
        )

    # Create the user
    hashed_password = auth_service.hash_password(request.password)
    new_user = User(
        email=request.email,
        hashed_password=hashed_password,
        is_superuser=True,
        is_active=True,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    logger.info("Initial admin user created", email=request.email)

    # Automatically log them in
    access_token = auth_service.create_access_token(
        data={"sub": request.email, "role": "SUPER_ADMIN"}
    )
    refresh_token = auth_service.create_refresh_token(subject=request.email)

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, session: AsyncSession = Depends(get_db_session)):
    """
    Authenticates an admin user and issues JWT tokens.
    """
    logger.info("Admin login attempt", email=request.email)

    # Look up the user by email
    stmt = select(User).where(User.email == request.email).limit(1)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if user and user.is_active and auth_service.verify_password(request.password, user.hashed_password):
        # We assume if they're logging into the admin dashboard, they should be a superuser
        # or we check their roles here. For now, we just grant the SUPER_ADMIN role if they are a superuser.
        role = "SUPER_ADMIN" if user.is_superuser else "USER"

        if role != "SUPER_ADMIN":
            logger.warning("Non-admin user attempted admin login", email=request.email)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have admin privileges",
            )

        access_token = auth_service.create_access_token(
            data={"sub": request.email, "role": role}
        )
        refresh_token = auth_service.create_refresh_token(subject=request.email)

        logger.info("Admin login successful", email=request.email)
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    logger.warning("Admin login failed", email=request.email)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshRequest):
    """
    Issues a new access token given a valid refresh token.
    """
    try:
        payload = auth_service.decode_token(request.refresh_token)
        if payload.get("type") != "refresh":
            raise ValueError("Invalid token type")

        email = payload.get("sub")
        if not email:
            raise ValueError("Invalid token payload")

        # Issue new tokens
        access_token = auth_service.create_access_token(data={"sub": email, "role": "SUPER_ADMIN"})
        new_refresh_token = auth_service.create_refresh_token(subject=email)

        return TokenResponse(access_token=access_token, refresh_token=new_refresh_token)

    except ValueError as e:
        logger.warning("Token refresh failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
