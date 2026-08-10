from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.tasks.models import Task
    from app.users.models import User


class TaskComment(SQLModel, table=True):
    __tablename__ = "task_comments"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    task_id: int = Field(
        foreign_key="tasks.id",
        index=True,
    )

    user_id: int = Field(
        foreign_key="users.id",
        index=True,
    )

    comment: str

    created_at: datetime | None = Field(default=None)

    task: "Task" = Relationship(
        back_populates="comments",
    )

    user: "User" = Relationship(
        back_populates="comments",
    )