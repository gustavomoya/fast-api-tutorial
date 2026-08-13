from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import Annotated

from app.core.database import get_session
from app.users.schemas import UserResponse
from app.users.models import User
from app.users.service import UserService
from app.users.dependencies import get_user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get( "/",response_model=list[UserResponse],)
def get_users(offset: int = 0, limit: Annotated[int, Query(le=100)] = 100, service: UserService = Depends(get_user_service)):
    return service.list_users(offset, limit)

@router.get("/{id}")
def get_user(id: int, service: UserService = Depends(get_user_service)):
    user =  service.find_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user