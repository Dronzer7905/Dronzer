import structlog
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from dronzer.application.admin.auth import AuthService

logger = structlog.get_logger("dronzer.api.admin.auth")
router = APIRouter(prefix="/auth", tags=["Admin Auth"])

# In reality, this would be injected globally via FastAPI Depends
auth_service = AuthService()

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """
    Authenticates an admin user and issues JWT tokens.
    """
    logger.info("Admin login attempt", email=request.email)

    # MOCK DB LOOKUP (Foundation Phase 15 logic mapping)
    mock_user_hash = auth_service.hash_password("admin123")

    if request.email == "admin@dronzer.ai" and auth_service.verify_password(request.password, mock_user_hash):
        access_token = auth_service.create_access_token(data={"sub": request.email, "role": "SUPER_ADMIN"})
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
