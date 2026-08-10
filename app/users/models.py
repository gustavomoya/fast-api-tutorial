from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.projects.models import Project
    from app.tasks.models import Task
    from app.comments.models import TaskComment


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    name: str = Field(max_length=100)

    email: str = Field(
        max_length=255,
        unique=True,
    )

    password_hash: str = Field(max_length=255)

    is_active: bool = Field(default=True)

    created_at: datetime | None = Field(default=None)

    updated_at: datetime | None = Field(default=None)

    projects: list["Project"] = Relationship(
        back_populates="owner",
    )

    assigned_tasks: list["Task"] = Relationship(
        back_populates="assignee",
    )

    comments: list["TaskComment"] = Relationship(
        back_populates="user",
    )