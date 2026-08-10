from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.users.models import User
    from app.tasks.models import Task


class Project(SQLModel, table=True):
    __tablename__ = "projects"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    name: str = Field(max_length=150)

    description: str | None = None

    owner_id: int = Field(
        foreign_key="users.id",
        index=True,
    )

    created_at: datetime | None = Field(default=None)

    updated_at: datetime | None = Field(default=None)

    owner: "User" = Relationship(
        back_populates="projects",
    )

    tasks: list["Task"] = Relationship(
        back_populates="project",
        cascade_delete=True,
    )