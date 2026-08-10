from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.database import get_session
from app.users.schemas import UserResponse
from app.users.models import User
from app.users.service import list_users


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/",
    response_model=list[UserResponse],
)
def get_users(
    session: Session = Depends(get_session),
):
    return list_users(session)
