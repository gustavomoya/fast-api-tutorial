
from fastapi import Depends
from sqlmodel import Session
from typing import Annotated

from app.core.database import get_session
from app.projects.member_repository import ProjectMemberRepository
from app.projects.member_service import ProjectMemberService
from app.projects.dependencies import get_project_service
from app.projects.service import ProjectService
from app.users.dependencies import get_user_service
from app.users.service import UserService


SessionDep = Annotated[Session, Depends(get_session)]


def get_project_member_repository(
    session: SessionDep,
) -> ProjectMemberRepository:
    return ProjectMemberRepository(session)


def get_project_member_service(
    repository: Annotated[
        ProjectMemberRepository,
        Depends(get_project_member_repository),
    ],
    project_service: Annotated[
        ProjectService,
        Depends(get_project_service),
    ],
    user_service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
) -> ProjectMemberService:
    return ProjectMemberService(
        repository,
        project_service,
        user_service,
    )
