from datetime import datetime, date

from pydantic import BaseModel, Field, ConfigDict, field_validator
from app.users.schemas import UserResponse
from app.projects.schemas import ProjectResponse
from app.tasks.models import TaskStatus, TaskPriority


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    assigned_to: int | None
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    due_date: date | None
    created_at: datetime
    updated_at: datetime
    assignee: UserResponse | None
    project: ProjectResponse


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: date | None = None
    project_id: int
    assigned_to: int | None = None