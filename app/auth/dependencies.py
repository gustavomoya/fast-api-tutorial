from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.dependencies import get_security
from app.core.security import Security
from app.users.dependencies import get_user_repository
from app.users.models import User
from app.users.repository import UserRepository
from app.auth.service import AuthService
from jwt.exceptions import InvalidTokenError

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token"
)

def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
    security: Security = Depends(get_security),
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        security=security,
    )
    
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], security: Security = Depends(get_security),
    user_repository: UserRepository = Depends(get_user_repository),) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = security.decode_access_token(token)

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user_id = int(user_id)

    except InvalidTokenError:
        raise credentials_exception

    user = user_repository.get_user(user_id)

    if user is None:
        raise credentials_exception

    return user

def get_current_active_user(current_user: Annotated[User,Depends(get_current_user),],) -> User:

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    return current_user