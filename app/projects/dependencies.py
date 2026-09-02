from fastapi import Depends
from sqlmodel import Session
from typing import Annotated

from app.core.database import get_session
from app.projects.repository import ProjectRepository
from app.projects.service import ProjectService

SessionDep = Annotated[Session, Depends(get_session)]

def get_project_repository(
    session:SessionDep,
) -> ProjectRepository:
    return ProjectRepository(session)


def get_project_service(
    repository: ProjectRepository = Depends(get_project_repository),
) -> ProjectService:
    return ProjectService(repository)