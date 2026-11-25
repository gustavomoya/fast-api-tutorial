from datetime import date, datetime
from enum import Enum
from typing import TYPE_CHECKING
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy import TIMESTAMP, text
from sqlalchemy import Enum as SAEnum

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.projects.models import Project
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
        sa_type=BIGINT(unsigned=True),
    )

    project_id: int = Field(
        foreign_key="projects.id",
        index=True,
        sa_type=BIGINT(unsigned=True),
    )

    assigned_to: int | None = Field(
        default=None,
        foreign_key="users.id",
        index=True,
        sa_type=BIGINT(unsigned=True),
    )

    title: str = Field(max_length=200)

    description: str | None = None

    status: TaskStatus = Field(
        default=TaskStatus.PENDING,
        max_length=20,
        sa_type=SAEnum(
            TaskStatus,
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
            native_enum=True,
        ),
    )

    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM,
        max_length=20,
        sa_type=SAEnum(
            TaskPriority,
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
            native_enum=True,
        ),
    )

    due_date: date | None = None

    created_at: datetime = Field(
        sa_type=TIMESTAMP,
        nullable=False,
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
        },
    )

    updated_at: datetime = Field(
        sa_type=TIMESTAMP,
        nullable=False,
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        },
    )

    project: "Project" = Relationship(
        back_populates="tasks",
    )

    assignee: "User" = Relationship(
        back_populates="assigned_tasks",
    )
