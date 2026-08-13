from fastapi import Depends
from sqlmodel import Session
from typing import Annotated

from app.core.database import get_session
from app.users.repository import UserRepository
from app.users.service import UserService

SessionDep = Annotated[Session, Depends(get_session)]

def get_user_repository(
    session:SessionDep,
) -> UserRepository:
    return UserRepository(session)


def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repository)
