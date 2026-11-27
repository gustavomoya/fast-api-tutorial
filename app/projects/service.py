import logging

from sqlmodel import Session

from app.projects.models import Project
from app.projects.repository import ProjectRepository
from app.projects.schemas import (
    ProjectFilterParams,
    ProjectCreate,
    ProjectPatch,
    ProjectUpdate,
)


class ProjectService:

    logger = logging.getLogger(__name__)

    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    def get_projects(self, filters: ProjectFilterParams) -> list[Project]:
        return self.repository.get_projects(filters)

    def get_projects_by_user(self, user_id: int) -> list[Project]:
        return self.repository.get_projects_by_user(user_id)

    def get_project(self, id: int) -> Project | None:
        return self.repository.get_project(id)

    def get_project_by_id_and_owner(
        self,
        project_id: int,
        owner_id: int,
    ) -> Project | None:
        return self.repository.get_project_by_id_and_owner(
            project_id,
            owner_id,
        )

    def create_project(
        self,
        project_data: ProjectCreate,
        user_id: int,
    ) -> Project:
        return self.repository.create_project(project_data, user_id)

    def patch_project(
        self,
        project_id: int,
        owner_id: int,
        project_data: ProjectPatch,
    ) -> Project | None:

        return self.repository.patch_project(project_id, owner_id, project_data)

    def update_project(
        self,
        project_id: int,
        owner_id: int,
        project_data: ProjectUpdate,
    ) -> Project | None:

        return self.repository.update_project(project_id, owner_id, project_data)

    def delete_project(
        self,
        project_id: int,
        owner_id: int,
    ) -> bool:

        return self.repository.delete_project(project_id, owner_id)
