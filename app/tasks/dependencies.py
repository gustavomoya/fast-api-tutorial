from fastapi import Depends
from sqlmodel import Session
from typing import Annotated

from app.core.database import get_session
from app.tasks.repository import TaskRepository
from app.tasks.service import TaskService
from app.projects.service import ProjectService
from app.projects.dependencies import get_project_service
from app.users.service import UserService
from app.users.dependencies import get_user_service

SessionDep = Annotated[Session, Depends(get_session)]


def get_task_repository(
    session: SessionDep,
) -> TaskRepository:
    return TaskRepository(session)


def get_task_service(
    repository: Annotated[
        TaskRepository,
        Depends(get_task_repository),
    ],
    project_service: Annotated[
        ProjectService,
        Depends(get_project_service),
    ],
    user_service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
) -> TaskService:
    return TaskService(repository, project_service, user_service)
