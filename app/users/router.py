from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import Annotated

from app.core.database import get_session
from app.users.schemas import UserResponse, UserFilterParams
from app.users.models import User
from app.users.service import UserService
from app.users.dependencies import get_user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get( "/",response_model=list[UserResponse],)
def get_users(filters: Annotated[UserFilterParams, Query()], service: UserService = Depends(get_user_service)):
    return service.list_users(filters)

@router.get("/{id}")
def get_user(id: int, service: UserService = Depends(get_user_service)):
    user =  service.find_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user