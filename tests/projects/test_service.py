
from unittest.mock import Mock

from app.projects.models import Project
from app.projects.repository import ProjectRepository
from app.projects.schemas import (
    ProjectCreate,
    ProjectFilterParams,
    ProjectPatch,
    ProjectUpdate,
)
from app.projects.service import ProjectService


def test_get_projects():
    repository = Mock(spec=ProjectRepository)
    expected_projects = [Mock(spec=Project), Mock(spec=Project)]
    repository.get_projects.return_value = expected_projects

    service = ProjectService(repository)
    filters = ProjectFilterParams()

    result = service.get_projects(filters)

    assert result == expected_projects
    repository.get_projects.assert_called_once_with(filters)


def test_get_project():
    repository = Mock(spec=ProjectRepository)
    expected_project = Mock(spec=Project)
    repository.get_project.return_value = expected_project

    service = ProjectService(repository)

    result = service.get_project(1)

    assert result == expected_project
    repository.get_project.assert_called_once_with(1)


def test_get_projects_by_user():
    repository = Mock(spec=ProjectRepository)
    expected_projects = [Mock(spec=Project)]
    repository.get_projects_by_user.return_value = expected_projects

    service = ProjectService(repository)

    result = service.get_projects_by_user(1)

    assert result == expected_projects
    repository.get_projects_by_user.assert_called_once_with(1)


def test_create_project():
    repository = Mock(spec=ProjectRepository)
    project_data = ProjectCreate(name="Test Project")
    expected_project = Mock(spec=Project)
    repository.create_project.return_value = expected_project

    service = ProjectService(repository)

    result = service.create_project(project_data, 1)

    assert result == expected_project
    repository.create_project.assert_called_once_with(project_data, 1)


def test_patch_project():
    repository = Mock(spec=ProjectRepository)
    project_data = ProjectPatch(name="Updated name")
    expected_project = Mock(spec=Project)
    repository.patch_project.return_value = expected_project

    service = ProjectService(repository)

    result = service.patch_project(1, 1, project_data)

    assert result == expected_project
    repository.patch_project.assert_called_once_with(1, 1, project_data)


def test_update_project():
    repository = Mock(spec=ProjectRepository)
    project_data = ProjectUpdate(
        name="Updated name",
        description="Updated description",
    )
    expected_project = Mock(spec=Project)
    repository.update_project.return_value = expected_project

    service = ProjectService(repository)

    result = service.update_project(1, 1, project_data)

    assert result == expected_project
    repository.update_project.assert_called_once_with(1, 1, project_data)


def test_delete_project():
    repository = Mock(spec=ProjectRepository)
    repository.delete_project.return_value = True

    service = ProjectService(repository)

    result = service.delete_project(1, 1)

    assert result is True
    repository.delete_project.assert_called_once_with(1, 1)
