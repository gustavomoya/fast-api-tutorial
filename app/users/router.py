from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import Annotated

from app.core.database import get_session
from app.users.schemas import UserResponse, UserFilterParams
from app.users.models import User
from app.users.service import UserService
from app.projects.service import ProjectService
from app.users.dependencies import get_user_service
from app.auth.dependencies import get_current_active_user
from app.projects.dependencies import get_project_service
from app.core.security import Security

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get( "/",response_model=list[UserResponse],)
def get_users(filters: Annotated[UserFilterParams, Query()], service: UserService = Depends(get_user_service)):    
    return service.list_users(filters)

@router.get("/me")
def read_users_me(
current_user: Annotated[User, Depends(get_current_active_user),],) -> User:
    return current_user

@router.get("/{id}")
def get_user(id: int, 
             service: UserService = Depends(get_user_service,),
             current_user: Annotated[User,Depends(get_current_active_user),] = None,):
    user =  service.find_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{id}/projects")
def get_user(id: int, 
             service: UserService = Depends(get_user_service,),
             project_service: ProjectService = Depends(get_project_service,),
             current_user: Annotated[User,Depends(get_current_active_user),] = None,):
    user =  service.find_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return project_service.get_projects_by_user(id)