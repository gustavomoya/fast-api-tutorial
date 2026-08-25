from fastapi import Depends

from app.core.config import settings
from app.core.security import Security


def get_security() -> Security:
    return Security(
        secret_key=settings.secret_key,
        algorithm=settings.algorithm,
    )
