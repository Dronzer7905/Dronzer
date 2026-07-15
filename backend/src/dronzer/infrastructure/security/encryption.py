import structlog
from cryptography.fernet import Fernet

from dronzer.core.config import settings

logger = structlog.get_logger("dronzer.security")


class EncryptionManager:
    """
    Handles encryption/decryption of sensitive database fields 
    (like API keys and plugin secrets) using Fernet symmetric encryption.
    """
    def __init__(self) -> None:
        try:
            self._fernet = Fernet(settings.SECRET_KEY.encode())
        except ValueError as e:
            logger.error("FATAL: SECRET_KEY is not a valid 32-byte base64-encoded Fernet key. Server cannot start.")
            raise ValueError("Invalid SECRET_KEY format. Must be a valid Fernet key.") from e

    def encrypt(self, plain_text: str) -> str:
        """Encrypts a string and returns a URL-safe base64-encoded encrypted string."""
        if not plain_text:
            return plain_text
        return self._fernet.encrypt(plain_text.encode()).decode()

    def decrypt(self, encrypted_text: str) -> str:
        """Decrypts a URL-safe base64-encoded encrypted string."""
        if not encrypted_text:
            return encrypted_text
        return self._fernet.decrypt(encrypted_text.encode()).decode()


# Singleton instance
crypto = EncryptionManager()
