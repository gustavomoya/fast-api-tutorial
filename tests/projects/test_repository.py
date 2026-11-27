
from sqlmodel import Session

from app.users.models import User
from app.projects.models import Project
from app.projects.repository import ProjectRepository
from app.projects.schemas import ProjectCreate, ProjectFilterParams, ProjectPatch, ProjectUpdate


def create_test_user(session: Session) -> User:
    user = User(
        name="Test User",
        email="test@example.com",
        password_hash="fake-password-hash",
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def test_create_project(db_session: Session):
    # Arrange
    user = create_test_user(db_session)
    repository = ProjectRepository(db_session)

    project_data = ProjectCreate(
        name="Test Project",
        description="Project created during testing",
    )

    # Act
    project = repository.create_project(project_data, user.id)

    # Assert
    assert project.id is not None
    assert project.name == "Test Project"
    assert project.description == "Project created during testing"
    assert project.owner_id == user.id


def test_get_project(db_session: Session):
    # Arrange
    user = create_test_user(db_session)
    repository = ProjectRepository(db_session)

    project = repository.create_project(
        ProjectCreate(name="Project to find"),
        user.id,
    )

    # Act
    result = repository.get_project(project.id)

    # Assert
    assert result is not None
    assert result.id == project.id
    assert result.name == "Project to find"
    assert result.owner.id == user.id


def test_get_projects(db_session: Session):
    # Arrange
    user = create_test_user(db_session)
    repository = ProjectRepository(db_session)

    repository.create_project(
        ProjectCreate(name="Project A"),
        user.id,
    )

    repository.create_project(
        ProjectCreate(name="Project B"),
        user.id,
    )

    filters = ProjectFilterParams()

    # Act
    projects = repository.get_projects(filters)

    # Assert
    assert len(projects) == 2
    assert {project.name for project in projects} == {
        "Project A",
        "Project B",
    }

def test_patch_project(db_session: Session):
    # Arrange
    user = create_test_user(db_session)
    repository = ProjectRepository(db_session)

    project = repository.create_project(
        ProjectCreate(
            name="Original name",
            description="Original description",
        ),
        user.id,
    )

    project_data = ProjectPatch(name="Updated name")

    # Act
    updated_project = repository.patch_project(
        project.id,
        user.id,
        project_data,
    )

    # Assert
    assert updated_project is not None
    assert updated_project.name == "Updated name"
    assert updated_project.description == "Original description"
    
def test_patch_project_clear_description(db_session: Session):
    user = create_test_user(db_session)
    repository = ProjectRepository(db_session)

    project = repository.create_project(
        ProjectCreate(
            name="Test project",
            description="Description to remove",
        ),
        user.id,
    )

    project_data = ProjectPatch(description=None)

    updated_project = repository.patch_project(
        project.id,
        user.id,
        project_data,
    )

    assert updated_project is not None
    assert updated_project.description is None   
    
def test_patch_project_not_owned_by_user(db_session: Session):
    owner = create_test_user(db_session)

    another_user = User(
        name="Another User",
        email="another@example.com",
        password_hash="fake-password-hash",
    )
    db_session.add(another_user)
    db_session.commit()
    db_session.refresh(another_user)

    repository = ProjectRepository(db_session)

    project = repository.create_project(
        ProjectCreate(name="Owner project"),
        owner.id,
    )

    updated_project = repository.patch_project(
        project.id,
        another_user.id,
        ProjectPatch(name="Unauthorized change"),
    )

    assert updated_project is None

    original_project = repository.get_project(project.id)
    assert original_project.name == "Owner project"     
    

def test_update_project(db_session: Session):
    user = create_test_user(db_session)
    repository = ProjectRepository(db_session)

    project = repository.create_project(
        ProjectCreate(
            name="Original name",
            description="Original description",
        ),
        user.id,
    )

    project_data = ProjectUpdate(
        name="New name",
        description="New description",
    )

    updated_project = repository.update_project(
        project.id,
        user.id,
        project_data,
    )

    assert updated_project is not None
    assert updated_project.name == "New name"
    assert updated_project.description == "New description"


def test_update_project_clear_description(db_session: Session):
    user = create_test_user(db_session)
    repository = ProjectRepository(db_session)

    project = repository.create_project(
        ProjectCreate(
            name="Original name",
            description="Original description",
        ),
        user.id,
    )

    project_data = ProjectUpdate(
        name="Updated name",
        description=None,
    )

    updated_project = repository.update_project(
        project.id,
        user.id,
        project_data,
    )

    assert updated_project is not None
    assert updated_project.name == "Updated name"
    assert updated_project.description is None



def test_update_project_not_owned_by_user(db_session: Session):
    owner = create_test_user(db_session)

    another_user = User(
        name="Another User",
        email="another@example.com",
        password_hash="fake-password-hash",
    )
    db_session.add(another_user)
    db_session.commit()
    db_session.refresh(another_user)

    repository = ProjectRepository(db_session)

    project = repository.create_project(
        ProjectCreate(name="Owner project"),
        owner.id,
    )

    updated_project = repository.update_project(
        project.id,
        another_user.id,
        ProjectUpdate(name="Unauthorized change"),
    )

    assert updated_project is None

    original_project = repository.get_project(project.id)
    assert original_project.name == "Owner project"


def test_delete_project(db_session: Session):
    user = create_test_user(db_session)
    repository = ProjectRepository(db_session)

    project = repository.create_project(
        ProjectCreate(name="Project to delete"),
        user.id,
    )

    deleted = repository.delete_project(project.id, user.id)

    assert deleted is True
    assert repository.get_project(project.id) is None



def test_delete_project_not_owned_by_user(db_session: Session):
    owner = create_test_user(db_session)

    another_user = User(
        name="Another User",
        email="another@example.com",
        password_hash="fake-password-hash",
    )
    db_session.add(another_user)
    db_session.commit()
    db_session.refresh(another_user)

    repository = ProjectRepository(db_session)

    project = repository.create_project(
        ProjectCreate(name="Owner project"),
        owner.id,
    )

    deleted = repository.delete_project(
        project.id,
        another_user.id,
    )

    assert deleted is False

    existing_project = repository.get_project(project.id)
    assert existing_project is not None


def test_delete_nonexistent_project(db_session: Session):
    repository = ProjectRepository(db_session)

    deleted = repository.delete_project(
        project_id=99999,
        owner_id=1,
    )

    assert deleted is False

    