from datetime import date, datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.comments.models import TaskComment
    from app.projects.models import Project
    from app.tags.models import TaskTag
    from app.users.models import User

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    project_id: int = Field(
        foreign_key="projects.id",
        index=True,
    )

    assigned_to: int | None = Field(
        default=None,
        foreign_key="users.id",
        index=True,
    )

    title: str = Field(max_length=200)

    description: str | None = None

    status: str = Field(
        default="pending",
        max_length=20,
    )

    priority: str = Field(
        default="medium",
        max_length=20,
    )

    due_date: date | None = None

    created_at: datetime | None = None

    updated_at: datetime | None = None

    project: "Project" = Relationship(
        back_populates="tasks",
    )

    assignee: "User" = Relationship(
        back_populates="assigned_tasks",
    )

    comments: list["TaskComment"] = Relationship(
        back_populates="task",
        cascade_delete=True,
    )

    task_tags: list["TaskTag"] = Relationship(
        back_populates="task",
        cascade_delete=True,
    )