from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Annotated

from app.tasks.schemas import TaskResponse, TaskCreate
from app.tasks.service import TaskService
from app.tasks.dependencies import get_task_service
from app.auth.dependencies import get_current_active_user
from app.users.models import User

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_tasks(
    task_data: TaskCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    service: TaskService = Depends(get_task_service),
):

    try:
        task = service.create_task(
            task_data,
            current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return task
