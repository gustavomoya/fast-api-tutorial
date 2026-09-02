from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated

from app.projects.schemas import ProjectFilterParams, ProjectResponse
from app.projects.service import ProjectService
from app.projects.dependencies import get_project_service

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)

@router.get( "/",response_model=list[ProjectResponse],)
def get_projects(filters: Annotated[ProjectFilterParams, Query()], service: ProjectService = Depends(get_project_service)):    
    return service.get_projects(filters)

@router.get("/{id}", response_model=ProjectResponse)
def get_project(id: int, service: ProjectService = Depends(get_project_service)):
    project = service.get_project(id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return project