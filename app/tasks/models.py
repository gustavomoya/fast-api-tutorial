
from datetime import date, datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import (
    TIMESTAMP,
    Column,
    ForeignKey,
    Index,
    Text,
    text,
)
from sqlalchemy.dialects.mysql import BIGINT
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

    __table_args__ = (
        Index("idx_tasks_project", "project_id"),
        Index("idx_tasks_assigned_to", "assigned_to"),
        Index("idx_tasks_status", "status"),
        Index("idx_tasks_priority", "priority"),
        Index("idx_tasks_due_date", "due_date"),
    )

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_type=BIGINT(unsigned=True),
    )

    project_id: int = Field(
        sa_column=Column(
            BIGINT(unsigned=True),
            ForeignKey(
                "projects.id",
                name="fk_tasks_project",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
    )

    assigned_to: int | None = Field(
        default=None,
        sa_column=Column(
            BIGINT(unsigned=True),
            ForeignKey(
                "users.id",
                name="fk_tasks_user",
                ondelete="SET NULL",
            ),
            nullable=True,
        ),
    )

    title: str = Field(max_length=200)

    description: str | None = Field(
        default=None,
        sa_type=Text,
    )

    status: TaskStatus = Field(
        default=TaskStatus.PENDING,
        max_length=20,
        sa_type=SAEnum(
            TaskStatus,
            values_callable=lambda enum_cls: [
                member.value for member in enum_cls
            ],
            native_enum=True,
        ),
    )

    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM,
        max_length=20,
        sa_type=SAEnum(
            TaskPriority,
            values_callable=lambda enum_cls: [
                member.value for member in enum_cls
            ],
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
            "server_default": text(
                "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"
            ),
        },
    )

    project: "Project" = Relationship(
        back_populates="tasks",
    )

    assignee: "User" = Relationship(
        back_populates="assigned_tasks",
    )
