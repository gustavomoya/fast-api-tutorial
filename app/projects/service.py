import logging

from sqlmodel import Session

from app.projects.models import Project
from app.projects.repository import ProjectRepository
from app.projects.schemas import ProjectFilterParams

class ProjectService:

    logger = logging.getLogger(__name__)

    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    def get_projects(self, filters: ProjectFilterParams) -> list[Project]:
        return self.repository.get_projects(filters)

    def get_project(self, id: int) -> Project:
        return self.repository.get_project(id)
    
    def get_projects_by_user(self, user_id: int)-> list[Project]:
        return self.repository.get_projects_by_user(user_id)