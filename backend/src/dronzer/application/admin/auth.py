from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
import jwt
import structlog

logger = structlog.get_logger("dronzer.admin.auth")

class AuthService:
    """
    Handles JWT generation, password hashing, and session tokens for the admin dashboard.
    """

    def __init__(self, secret_key: str = "SUPER_SECRET_CHANGE_ME", algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = 30
        self.refresh_token_expire_days = 7

    def hash_password(self, password: str) -> str:
        """Hashes a password using bcrypt."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifies a plain password against a bcrypt hash."""
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        """Generates a short-lived JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(minutes=self.access_token_expire_minutes)

        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def create_refresh_token(self, subject: str) -> str:
        """Generates a long-lived JWT refresh token."""
        expire = datetime.now(UTC) + timedelta(days=self.refresh_token_expire_days)
        to_encode = {"sub": subject, "exp": expire, "type": "refresh"}
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_token(self, token: str) -> dict[str, Any]:
        """Decodes and validates a JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.PyJWTError as e:
            raise ValueError(f"Invalid token: {str(e)}")
