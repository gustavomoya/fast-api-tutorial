from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy import TIMESTAMP, text

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.projects.models import Project
    from app.tasks.models import Task



class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_type=BIGINT(unsigned=True),
    )

    name: str = Field(max_length=100)

    email: str = Field(
        max_length=255,
        unique=True,
    )

    password_hash: str = Field(max_length=255)

    is_active: bool = Field(default=True)

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

    projects: list["Project"] = Relationship(
        back_populates="owner",
    )

    assigned_tasks: list["Task"] = Relationship(
        back_populates="assignee",
    )