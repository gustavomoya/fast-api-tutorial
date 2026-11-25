from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Annotated

from app.projects.schemas import (
    ProjectFilterParams,
    ProjectResponse,
    ProjectCreate,
    ProjectPatch,
    ProjectUpdate,
)
from app.projects.service import ProjectService
from app.projects.dependencies import get_project_service
from app.auth.dependencies import get_current_active_user
from app.users.models import User

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.get(
    "/",
    response_model=list[ProjectResponse],
)
def get_projects(
    filters: Annotated[ProjectFilterParams, Query()],
    service: ProjectService = Depends(get_project_service),
):
    return service.get_projects(filters)


@router.get("/{id}", response_model=ProjectResponse)
def get_project(id: int, service: ProjectService = Depends(get_project_service)):
    project = service.get_project(id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    project_data: ProjectCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    service: ProjectService = Depends(get_project_service),
):
    return service.create_project(
        project_data,
        current_user.id,
    )


@router.patch("/{id}", response_model=ProjectResponse)
def patch_project(
    id: int,
    project_data: ProjectPatch,
    current_user: Annotated[User, Depends(get_current_active_user)],
    service: ProjectService = Depends(get_project_service),
):

    project = service.patch_project(
        id,
        current_user.id,
        project_data,
    )

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    return project

@router.put("/{id}", response_model=ProjectResponse)
def update_project(
    id: int,
    project_data: ProjectUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    service: ProjectService = Depends(get_project_service),
):

    project = service.update_project(
        id,
        current_user.id,
        project_data,
    )

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    return project

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT,)
def delete_project(
    id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    service: ProjectService = Depends(get_project_service),
):

    deleted = service.delete_project(
        id,
        current_user.id,
    )

    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")
