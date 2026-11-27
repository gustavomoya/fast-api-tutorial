from typing import Any

from sqlmodel import Session, select
from sqlalchemy.orm import joinedload

from app.projects.models import Project
from app.projects.schemas import (
    ProjectFilterParams,
    ProjectCreate,
    ProjectPatch,
    ProjectUpdate,
)


class ProjectRepository:

    def __init__(self, session: Session):
        """Initialize the repository with a database session."""
        self.session = session

    def get_projects(self, filters: ProjectFilterParams) -> list[Project]:
        """Return the projects matching the filters, with pagination."""
        statement = select(Project).options(joinedload(Project.owner))

        if filters.name is not None:
            statement = statement.where(Project.name == filters.name)

        if filters.created_at is not None:
            statement = statement.where(Project.created_at == filters.created_at)

        if filters.updated_at is not None:
            statement = statement.where(Project.updated_at == filters.updated_at)

        statement = statement.offset(filters.offset).limit(filters.limit)

        return list(self.session.exec(statement).all())

    def get_projects_by_user(self, user_id: int) -> list[Project]:
        """Return up to 100 projects owned by a user."""
        statement = (
            select(Project)
            .options(joinedload(Project.owner))
            .where(Project.owner_id == user_id)
            .offset(0)
            .limit(100)
        )

        return list(self.session.exec(statement).all())

    def get_project(self, project_id: int) -> Project | None:
        """Return a project by ID with its owner loaded, or None."""
        statement = (
            select(Project)
            .options(joinedload(Project.owner))
            .where(Project.id == project_id)
        )

        return self.session.exec(statement).first()

    def get_project_by_id_and_owner(
        self,
        project_id: int,
        owner_id: int,
    ) -> Project | None:

        statement = select(Project).where(
            Project.id == project_id,
            Project.owner_id == owner_id,
        )
        return self.session.exec(statement).first()

    def create_project(
        self,
        project_data: ProjectCreate,
        owner_id: int,
    ) -> Project:
        """Create a project for the given owner and persist it."""
        project = Project(
            **project_data.model_dump(),
            owner_id=owner_id,
        )

        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)

        return project

    def patch_project(
        self,
        project_id: int,
        owner_id: int,
        project_data: ProjectPatch,
    ) -> Project | None:
        """Partially update an owned project, or None if it does not exist."""
        project = self._get_project_by_id_and_user(project_id, owner_id)

        if project is None:
            return None

        update_data = project_data.model_dump(exclude_unset=True)

        return self._apply_update(project, update_data)

    def update_project(
        self,
        project_id: int,
        owner_id: int,
        project_data: ProjectUpdate,
    ) -> Project | None:
        """Update the data of an owned project, or None if it does not exist."""
        project = self._get_project_by_id_and_user(project_id, owner_id)

        if project is None:
            return None

        update_data = project_data.model_dump()

        return self._apply_update(project, update_data)

    def delete_project(
        self,
        project_id: int,
        owner_id: int,
    ) -> bool:
        """Delete a project."""

        statement = select(Project).where(
            Project.id == project_id,
            Project.owner_id == owner_id,
        )

        project = self.session.exec(statement).first()

        if project is None:
            return False

        self.session.delete(project)
        self.session.commit()

        return True

    def _get_project_by_id_and_user(
        self,
        project_id: int,
        owner_id: int,
    ) -> Project | None:
        """Fetch a project by ID ensuring it belongs to the given owner."""
        statement = (
            select(Project)
            .options(joinedload(Project.owner))
            .where(
                Project.id == project_id,
                Project.owner_id == owner_id,
            )
        )

        project = self.session.exec(statement).first()

        return project

    def _apply_update(
        self,
        project: Project,
        update_data: dict[str, Any],
    ) -> Project:
        """Apply the given fields to the project and commit the changes."""
        for key, value in update_data.items():
            setattr(project, key, value)

        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)

        return project
