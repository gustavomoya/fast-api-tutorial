import logging

from datetime import timedelta
from fastapi import HTTPException, status
from app.core.config import settings
from app.core.security import Security
from app.users.models import User
from app.users.repository import UserRepository

logger = logging.getLogger(__name__)

class AuthService:

    def __init__(
        self,
        user_repository: UserRepository,
        security: Security,
    ):
        self.user_repository = user_repository
        self.security = security

    def authenticate_user(
        self,
        username: str,
        password: str,
    ) -> User:

        user = self.user_repository.get_by_email(username)
        
        if not user:
            logger.warning(
                "Login failed: user not found, email=%s",
                username,
            )
            self.security.verify_password(password, "")
            return False
        if not self.security.verify_password(password, user.password_hash):
            logger.warning(
               "Login failed: invalid password, email=%s",
                username,
            )
            return False
        
        return user

    def create_access_token(
        self,
        user: User,
    ) -> str:

        expires_delta = timedelta(
            minutes=settings.access_token_expire_minutes
        )

        return self.security.create_access_token(
            data={"sub": str(user.id)},
            expires_delta=expires_delta,
        )
